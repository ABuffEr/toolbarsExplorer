# ToolbarsExplorer
# A global plugin for NVDA
# Copyright 2018 Alberto Buffolino, released under GPL

# Add-on to facilitate toolbar management.
# Partially inspired by ObjNav add-on, of Joseph Lee and others.

#from NVDAObjects.window import Window as getNVDAObjectFromHandle
from NVDAObjects.IAccessible import WindowRoot, getNVDAObjectFromEvent
from globalCommands import commands, SCRCAT_OBJECTNAVIGATION
from globalVars import desktopObject
from logHandler import log
from msg import message as NVDALocale
from scriptHandler import findScript, executeScript
import addonHandler
import api
import controlTypes as ct
import ctypes
import globalPluginHandler
import review
import speech
import ui
import winUser

addonHandler.initTranslation()

# to enable logging
DEBUG = False

def debugLog(message):
	if DEBUG:
		log.info(message)

# for testing performances
import time
from contextlib import contextmanager
@contextmanager
def timeblock(label):
	start = time.clock()
	try:
		yield
	finally:
		end = time.clock()
		debugLog("%s: %.3f s"%(label, end-start))

# Modified version of windowUtils.findDescendantWindow.
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def findAllDescendantWindows(parent, visible=None, className=None):
	"""Find all descendant windows, optionally matching specified visibility or className."""
	results = []
	@WNDENUMPROC
	def callback(window, data):
		if (
			(visible is None or winUser.isWindowVisible(window) == visible)
			and (not className or className in winUser.getClassName(window))
		):
			results.append(window)
		return True
	# call previous func until it returns True,
	# thus always, getting all windows
	ctypes.windll.user32.EnumChildWindows(parent, callback, 0)
	return results

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# roles of objects that could contain a toolbar
	# splitted in two tuples for probability/performance reasons
	promisingRoles = (ct.ROLE_APPLICATION, ct.ROLE_WINDOW, ct.ROLE_DIALOG, ct.ROLE_FRAME, ct.ROLE_PAGE, ct.ROLE_PROPERTYPAGE,)
	lessPromisingRoles = (ct.ROLE_PANE, ct.ROLE_OPTIONPANE, ct.ROLE_BOX, ct.ROLE_GROUPING, ct.ROLE_DIRECTORYPANE, ct.ROLE_GLASSPANE, ct.ROLE_INPUTWINDOW, ct.ROLE_LAYEREDPANE, ct.ROLE_ROOTPANE, ct.ROLE_EDITBAR, ct.ROLE_TERMINAL, ct.ROLE_RICHEDIT, ct.ROLE_SCROLLPANE, ct.ROLE_SPLITPANE, ct.ROLE_VIEWPORT, ct.ROLE_TEXTFRAME, ct.ROLE_INTERNALFRAME, ct.ROLE_DESKTOPPANE, ct.ROLE_PANEL,)

	def configVars(self):
		"""collects and initializes starting variables."""
		# the object used as root (may be not the real root)
		self.root = None
		# current application name
		self.curAppName = None
		# a backup of review mode, focus and navigator objects, prior exploration starting
		self.startSnap = {}.fromkeys(["focus", "nav", "reviewMode"])
		# toolbars found after search
		self.bars = []
		# index of current toolbar in exploration
		self.barIndex = 0
		# items of current toolbar
		self.barItems = []
		# index of selected item
		self.barItemIndex = None

	def findToolbars(self):
		"""the core method to find and filter toolbar objects."""
		self.getRoot()
		if not self.root:
			debugLog("No root found")
			return
		debugLog("root is: %s"%self.root)
		# launch search
		self.searchLauncher()
		# launch filters
		self.filterToolbars()
		debugLog("Found %d toolbars"%len(self.bars))

	def getRoot(self):
		"""selects or adjusts root object for search."""
		for ancestor in api.getFocusAncestors():
			if isinstance(ancestor, WindowRoot): # or ancestor.simpleParent == desktopObject:
				self.root = ancestor
				break
		curFocus = api.getFocusObject()
		self.curAppName = curFocus.appModule.appName if curFocus.appModule else None
		debugLog("%s toolbars session"%self.curAppName)
		# root adjustments
		if self.curAppName in ("calibre",):
			while curFocus.role != ct.ROLE_WINDOW:
				curFocus = curFocus.simpleParent
			self.root = curFocus.simpleParent
		elif self.curAppName == "explorer" and curFocus.simpleParent.simpleParent == desktopObject:
			debugLog("Desktop list detected, root adjustment")
			# set root as desktopObject
			self.root = curFocus.simpleParent.simpleParent
			# adjust appName as specified in desktopObject above (see condition later)
			self.curAppName = "csrss"

	def searchLauncher(self):
		"""chooses and launch appropriate search method."""
		# for applications where children sometimes disappear going to parent
		if self.curAppName in ("soffice",):
			debugLog("Try bottom-up search")
			curFocus = api.getFocusObject()
			self.bottomUpRecursiveSearch(curFocus, ct.ROLE_TOOLBAR)
		# for browsers and other apps where expressSearch regularly fails
		elif self.curAppName in ("chrome", "calibre",) or self.root.windowClassName in ("MozillaWindowClass",):
			# use slowSearch for these apps, for now
			debugLog("Use slow method directly")
			self.slowSearch()
		else:
			# best case, expressSearch works
			debugLog("Try expressSearch")
			self.expressSearch()
			# ...oterwise, try slow method
			if not self.bars:
				debugLog("Try slow method")
				self.slowSearch()

	def expressSearch(self):
		"""search toolbars using windows handles."""
		barHandles = findAllDescendantWindows(api.getForegroundObject().windowHandle, visible=True) #, className="Toolbar") 
		debugLog("Found %d handles"%len(barHandles))
		for handle in barHandles:
			bar = getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
			if bar:
				if bar.role == ct.ROLE_TOOLBAR:
					self.bars.append(bar)
				# some handles carry to invisible simpleParent
				# i.e. in Windows explorer
				elif not bar.isFocusable and (bar.role in self.promisingRoles or bar.role in self.lessPromisingRoles):
					# indeed, here child may be a toolbar, and bar its parent
					for child in bar.children:
						if child.role == ct.ROLE_TOOLBAR:
							self.bars.append(child)

	def slowSearch(self):
		"""search toolbars using object navigation."""
		self.recursiveSearch(self.root, ct.ROLE_TOOLBAR, outRoot=True)
		# search gives bars in reverse order, so...
		self.bars.reverse()

	def recursiveSearch(self, obj, matchRole, outRoot=True):
		"""performs a recursive search on object hierarchy."""
		debugLog("Analyzing %s: %s"%(obj.name,obj))
		if obj.role in self.promisingRoles or obj.role in self.lessPromisingRoles:
			childObj = obj.simpleLastChild
			if childObj:
				debugLog("Go down")
				self.recursiveSearch(childObj, matchRole)
		elif obj.role == matchRole:
			self.bars.append(obj)
		# outRoot on False limits out-of-root search in first recursion
		if not outRoot:
			return
		prevObj = obj.simplePrevious
		if prevObj:
			prevAppName = prevObj.appModule.appName if prevObj.appModule else None
			if (
				(prevObj.simpleParent != desktopObject)
				or
				# LibreOffice use a non-relative dialog in certain configurations
				(prevObj.role == ct.ROLE_DIALOG and prevAppName == self.curAppName)
				or
				# try to manage starting from desktop list
				(prevObj.simpleParent == self.root == desktopObject and (prevAppName, self.curAppName) == ("explorer", "csrss"))
			):
				debugLog("Go previous")
				self.recursiveSearch(prevObj, matchRole)

	def nonrecursiveSearch(self, obj, matchRole):
		"""performs a nonrecursive search on object hierarchy.
			WARNING: this method is outdated (some condition checks lack), see recursiveSearch instead."""
		# objects to analyze in each loop iteration
		objList = [obj]
		# breadth first search loop
		while objList:
			newObjList = []
			for obj in objList:
				if obj.role in self.promisingRoles or obj.role in self.lessPromisingRoles:
					obj = obj.simpleLastChild
					while obj and (obj.simpleParent != desktopObject or obj.role == ct.ROLE_DIALOG):
						newObjList.append(obj)
						obj = obj.simplePrevious
				elif obj.role == matchRole:
					self.bars.append(obj)
			objList = newObjList

	def bottomUpRecursiveSearch(self, obj, matchRole, lastDirection="up"):
		"""performs a object search starting from passed object, exploring current level and climbing back to root.""" 
		debugLog("Analyzing %s: %s"%(obj.name,obj))
		if lastDirection != "up" and (obj.role in self.promisingRoles or obj.role in self.lessPromisingRoles):
			# we use another search to analyzing down
			# reversing bars before and after to have them ordered
			self.bars.reverse()
			debugLog("Launching recursive search")
			self.recursiveSearch(obj, matchRole, outRoot=False)
			debugLog("recursiveSearch finished")
			self.bars.reverse()
		elif obj.role == ct.ROLE_TOOLBAR:
			self.bars.append(obj)
		if lastDirection in ("next", "up"):
			nextObj = obj.simpleNext
			nextAppName = nextObj.appModule.appName if (nextObj and nextObj.appModule) else None
			if nextObj and nextAppName == self.curAppName:
				debugLog("Go next")
				self.bottomUpRecursiveSearch(nextObj, matchRole, "next")
		if lastDirection in ("prev", "up"):
			prevObj = obj.simplePrevious
			prevAppName = prevObj.appModule.appName if (prevObj and prevObj.appModule) else None
			if prevObj and prevAppName == self.curAppName:
				debugLog("Go previous")
				self.bottomUpRecursiveSearch(prevObj, matchRole, "prev")
		if lastDirection == "up":
			parentObj = obj.simpleParent
			if parentObj and parentObj != desktopObject:
				debugLog("Go up")
				self.bottomUpRecursiveSearch(parentObj, matchRole, "up")

	def filterToolbars(self):
		"""removes empty, duplicate or unwanted, assign numbers to anonymous toolbars."""
		fixedBars = []
		for bar in self.bars:
			# remove duplicates
			if bar in fixedBars:
				# show warning: duplicate must be rare, not the usual
				debugLog("WARNING: duplicate toolbar found, %s: %s"%(bar.name, bar))
				continue
			child = bar.simpleFirstChild
			# Mozilla apps have a toolbar with menubar as first child, purge out
			if child and child.role != ct.ROLE_MENUBAR:
				fixedBars.append(bar)
				# if bar has no or useless name, rename it
				if not bar.name or bar.name.lower() in ("toolbar", "tool bar", NVDALocale("tool bar"),):
					bar.name = ' '.join([NVDALocale("tool bar"), str(len(fixedBars))])
		self.bars = fixedBars

	def script_startExploration(self, gesture):
		self.configVars()
		# a initial objects backup
		self.startSnap["focus"] = api.getFocusObject()
		self.startSnap["nav"] = api.getNavigatorObject()
		self.startSnap["reviewMode"] = review.getCurrentMode()
		# set object navigation active
		review.setCurrentMode("object", updateReviewPosition=False)
		# for testing performances
		with timeblock("Toolbars found in"):
			self.findToolbars()
		if not self.bars:
			# Translators: message in applications without toolbars
			ui.message(_("No toolbar found"))
			return
		# see script_explore for gesture explanation
		for direction in ("up", "right", "down", "left"):
			self.bindGesture("kb:%sArrow"%direction, "explore")
		self.bindGesture("kb:escape", "finish")
		self.bindGesture("kb:enter", "objActivate")
		self.bindGesture("kb:space", "objLeftClick")
		self.bindGesture("kb:applications", "objRightClick")
		bar = self.bars[self.barIndex]
		self.populateBarItems(bar)
		api.setNavigatorObject(bar)
		speech.speakObject(bar, reason=ct.REASON_FOCUS)
	# Translators: input help mode message for ToolbarsExplorer start command.
	script_startExploration.__doc__ = _("Starts exploration of toolbars, if present in current application")
	script_startExploration.category = SCRCAT_OBJECTNAVIGATION

	def populateBarItems(self, bar):
		"""populates self.barItems, excluding  unwanted objects."""
		# TODO: dinamically get barItems, without barItemIndex and barItems
		for child in bar.children:
			if (
				# exclude invisible objects
				(ct.STATE_INVISIBLE in child.states)
				or
				# exclude separators and unknown objects
				(child.role in (ct.ROLE_SEPARATOR, ct.ROLE_UNKNOWN,))
				or
				# exclude empty panes and sub-toolbars
				# but not in Eclipse, where sub-toolbars are buttons
				(self.curAppName != "eclipse" and child.role in (ct.ROLE_PANE, ct.ROLE_TOOLBAR,) and not child.simpleFirstChild)
			):
				continue
			self.barItems.append(child)

	def script_finish(self, gesture, restoreMode=True, restoreObjects=True):
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		# restore initial objects and review mode
		if restoreMode:
			review.setCurrentMode(self.startSnap["reviewMode"], updateReviewPosition=False)
		if restoreObjects:
			api.setFocusObject(self.startSnap["focus"])
			api.setNavigatorObject(self.startSnap["nav"])
			speech.speakObject(self.startSnap["focus"], reason=ct.REASON_FOCUS)

	def shouldTerminate(self):
		"""Tries to establish whether we are still exploring toolbars."""
		curNav = api.getNavigatorObject()
		curFocus = api.getFocusObject()
		if (
			# navigator is out of toolbars
			(curNav not in self.bars and curNav not in self.barItems)
			or
			# focus is changed
			(curFocus != self.startSnap["focus"])
		):
			return True

	def getBar(self, increment):
		"""provides toolbars circularly."""
		self.barIndex = (self.barIndex+increment)%len(self.bars)
		bar = self.bars[self.barIndex]
		# reset index and items for new bar
		self.barItemIndex = None
		self.barItems = []
		self.populateBarItems(bar)
		return bar

	def getBarItem(self, increment):
		"""provides toolbar items circularly."""
		# after filters, there may be no items
		if not self.barItems:
			return
		# checks to avoid initial undesired skip
		# scrolling toolbar items
		if self.barItemIndex is None and increment > 0:
			self.barItemIndex = 0
		elif self.barItemIndex is None and increment < 0:
			self.barItemIndex = -1
		else:
			self.barItemIndex = (self.barItemIndex+increment)%len(self.barItems)
		return self.barItems[self.barItemIndex]

	def script_explore(self, gesture):
		# when you execute a non-mapped action and focus/navigator object changes
		if self.shouldTerminate():
			debugLog("Out-of-exploration gesture: %s"%gesture.mainKeyName)
			self.script_finish(gesture, restoreObjects=False)
			script = findScript(gesture)
			if not script:
				gesture.send()
			else:
				debugLog("Execute script %s"%script)
				executeScript(script, gesture)
			return
		arrow = gesture.mainKeyName
		# left and right to change toolbar,
		# down and up to scroll its items
		if arrow == "leftArrow":
			newObj = self.getBar(-1)
		elif arrow == "rightArrow":
			newObj = self.getBar(+1)
		elif arrow == "upArrow":
			newObj = self.getBarItem(-1)
		elif arrow == "downArrow":
			newObj = self.getBarItem(+1)
		if not newObj:
			# Translators: message presented when filtered toolbar has no elements
			ui.reviewMessage(_("No toolbar item"))
			return
		api.setNavigatorObject(newObj)
		speech.speakObject(newObj, reason=ct.REASON_FOCUS)

	def script_objActivate(self, gesture):
		# we have finished, regardless action result
		self.script_finish(gesture, restoreObjects=False)
		# invoke activate action on current toolbar item
		commands.script_review_activate(gesture)

	def script_objLeftClick(self, gesture):
		# move mouse to current toolbar item
		commands.script_moveMouseToNavigatorObject(gesture)
		# we have finished, regardless action result
		self.script_finish(gesture, restoreObjects=False)
		# click!
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)

	def script_objRightClick(self, gesture):
		# move mouse to current toolbar item
		commands.script_moveMouseToNavigatorObject(gesture)
		# we have finished, regardless action result
		self.script_finish(gesture, restoreObjects=False)
		# click!
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)

	__gestures = {
	"kb:alt+applications": "startExploration"
	}

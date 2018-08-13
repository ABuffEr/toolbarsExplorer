# ToolbarsExplorer
# A global plugin for NVDA
# Copyright 2018 Alberto Buffolino, released under GPL

# Add-on to facilitate toolbar management.
# Partially inspired by ObjNav add-on, of Joseph Lee and others.

import globalPluginHandler
from globalCommands import commands, SCRCAT_OBJECTNAVIGATION
from NVDAObjects.IAccessible import WindowRoot, getNVDAObjectFromEvent
#from NVDAObjects.window import Window as getNVDAObjectFromHandle
import winUser
from globalVars import desktopObject
from msg import message as NVDALocale
import api
import speech
import controlTypes as ct
import ui
from logHandler import log
import addonHandler

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# roles of objects that can contain a toolbar
	promisingRoles = (ct.ROLE_WINDOW, ct.ROLE_PANE, ct.ROLE_DIALOG, ct.ROLE_FRAME, ct.ROLE_APPLICATION, ct.ROLE_BOX, ct.ROLE_GROUPING, ct.ROLE_PROPERTYPAGE, ct.ROLE_DIRECTORYPANE, ct.ROLE_GLASSPANE, ct.ROLE_INPUTWINDOW, ct.ROLE_PAGE, ct.ROLE_LAYEREDPANE, ct.ROLE_ROOTPANE, ct.ROLE_EDITBAR, ct.ROLE_TERMINAL, ct.ROLE_RICHEDIT, ct.ROLE_SCROLLPANE, ct.ROLE_SPLITPANE, ct.ROLE_VIEWPORT, ct.ROLE_TEXTFRAME, ct.ROLE_INTERNALFRAME, ct.ROLE_DESKTOPPANE, ct.ROLE_PANEL)

	def findToolbars(self):
		"""the core method to find and filter toolbar objects."""
		# search root object
		for ancestor in api.getFocusAncestors():
			if isinstance(ancestor, WindowRoot): # or ancestor.simpleParent == desktopObject:
				root = ancestor
				break
		if not root:
			return
		app = root.appModule.appName
		if app and (app in ("chrome", "soffice") or root.windowClassName == u'MozillaWindowClass'):
			# use slowSearch for tese apps, for now
#			log.info("Use slow method directly")
			self.slowSearch(root)
		else:
			# best case, expressSearch works
#			log.info("Try expressSearch")
			self.expressSearch(root)
			# ...oterwise, try slow method
			if not self.bars:
#				log.info("Try slow method")
				self.slowSearch(root)
		self.fixToolbars()
#		log.info("Found %d toolbars"%len(self.bars))

	def expressSearch(self, root):
		"""search toolbars using windows handles."""
		barHandles = findAllDescendantWindows(api.getForegroundObject().windowHandle, visible=True) #, className="Toolbar") 
#		log.info("Found %d handles"%len(barHandles))
		# for testing
#		promisingObjCount = 0
		for handle in barHandles:
			bar = getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
			if bar:
				if bar.role == ct.ROLE_TOOLBAR: # and bar not in self.bars:
					self.bars.append(bar)
				# some handles carry to invisible simpleParent
				# i.e. in Windows explorer
				elif not bar.isFocusable and bar.role in self.promisingRoles:
#					promisingObjCount += 1
					self.bars.extend(filter(lambda obj: obj.role == ct.ROLE_TOOLBAR, bar.children))
#		log.info("Analyzed %d promising objects"%promisingObjCount)

	def slowSearch(self, root):
		"""search toolbars using object navigation."""
		# for testing
#		self.objCount = 0
		self.recursiveSearch(root, ct.ROLE_TOOLBAR)
#		log.info("objCount=%d"%self.objCount)
		# search gives bars in reverse order, so...
		self.bars.reverse()

	def fixToolbars(self):
		"""removes empty or unwanted, assign numbers to anonymous toolbars."""
		fixedBars = []
		for bar in self.bars:
			child = bar.simpleFirstChild
			# Mozilla apps have a toolbar with menubar as first child, purge out
			if child and child.role != ct.ROLE_MENUBAR:
				fixedBars.append(bar)
				if not bar.name:
					bar.name = ' '.join([NVDALocale("tool bar"), str(len(fixedBars))])
		self.bars = fixedBars

	def recursiveSearch(self, obj, matchRole):
		"""performs a recursive search on object hierarchy."""
		if obj.role in self.promisingRoles:
			childObj = obj.simpleLastChild
			if childObj:
				self.recursiveSearch(childObj, matchRole)
		elif obj.role == matchRole: # and obj not in self.bars:
			self.bars.append(obj)
		prevObj = obj.simplePrevious
		# LibreOffice use a non-relative dialog
		if prevObj and (prevObj.simpleParent != desktopObject or prevObj.role == ct.ROLE_DIALOG):
			self.recursiveSearch(prevObj, matchRole)
		# for testing
#		self.objCount += 1

	def nonrecursiveSearch(self, obj, matchRole):
		"""performs a nonrecursive search on object hierarchy."""
		objList = [obj]
		# breadth first search loop
		while objList:
			newObjList = []
			for obj in objList:
				# for testing
#				self.objCount += 1
				if obj.role in self.promisingRoles:
					obj = obj.simpleLastChild
					while obj and (obj.simpleParent != desktopObject or obj.role == ct.ROLE_DIALOG):
						newObjList.append(obj)
						obj = obj.simplePrevious
				elif obj.role == matchRole:
					self.bars.append(obj)
			objList = newObjList

	def script_startExploration(self, gesture):
		self.bars = []
		# for testing
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
		# a initial object backup
		self.startObj = api.getNavigatorObject()
		self.barIndex = 0
		# TODO: dinamically get barItems, without barItemIndex and barItems
		self.barItemIndex = None
		bar = self.bars[self.barIndex]
		# get toolbar items, excluding separators
		self.barItems = filter(lambda obj: obj.role != ct.ROLE_SEPARATOR, bar.children)
		api.setNavigatorObject(bar)
		speech.speakObject(bar, reason=ct.REASON_FOCUS)
	# Translators: input help mode message for ToolbarsExplorer start command.
	script_startExploration.__doc__ = _("Starts exploration of toolbars, if present in current application")
	script_startExploration.category = SCRCAT_OBJECTNAVIGATION

	def script_finish(self, gesture, restoreFocus=True):
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		# restore initial object
		if restoreFocus:
			api.setNavigatorObject(self.startObj)
			speech.speakObject(self.startObj, reason=ct.REASON_FOCUS)

	def shouldTerminate(self):
		"""Tries to establish whether we are still exploring toolbars (i.e., after an action)."""
		curObj = api.getNavigatorObject()
		if curObj not in self.bars and curObj not in self.barItems:
			return True

	def getBar(self, increment):
		"""provides toolbars circularly."""
		self.barIndex = (self.barIndex+increment)%len(self.bars)
		bar = self.bars[self.barIndex]
		# reset items for new bar
		self.barItemIndex = None
		self.barItems = filter(lambda obj: obj.role != ct.ROLE_SEPARATOR, bar.children)
		return bar

	def getBarItem(self, increment):
		"""provides toolbar items circularly."""
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
		if self.shouldTerminate():
			self.script_finish(gesture, restoreFocus=False)
			# TODO: last gesture should be processed by other object
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
		api.setNavigatorObject(newObj)
		speech.speakObject(newObj, reason=ct.REASON_FOCUS)

	def script_objActivate(self, gesture):
		# invoke activate action on current toolbar item
		commands.script_review_activate(gesture)
		# we have finished, regardless action result
		self.script_finish(gesture, restoreFocus=False)

	def script_objLeftClick(self, gesture):
		# move mouse to current toolbar item
		commands.script_moveMouseToNavigatorObject(gesture)
		# click it
		commands.script_leftMouseClick(gesture)
		# we have finished, regardless action result
		self.script_finish(gesture, restoreFocus=False)

	def script_objRightClick(self, gesture):
		# move mouse to current toolbar item
		commands.script_moveMouseToNavigatorObject(gesture)
		# click it
		commands.script_rightMouseClick(gesture)
		# we have finished, regardless action result
		self.script_finish(gesture, restoreFocus=False)

	__gestures = {
	"kb:alt+applications": "startExploration"
	}

# for testing
from contextlib import contextmanager
import time

@contextmanager
def timeblock(label):
	start = time.clock()
	try:
		yield
	finally:
		end = time.clock()
		log.info("%s: %.3f s"%(label, end-start))

import ctypes

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

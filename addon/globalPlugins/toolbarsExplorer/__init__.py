# ToolbarsExplorer
# A global plugin for NVDA
# Copyright 2018 Alberto Buffolino, released under GPL

# Add-on to facilitate toolbar management.
# Partially inspired by ObjNav add-on, of Joseph Lee and others.

from NVDAObjects.IAccessible import WindowRoot, getNVDAObjectFromEvent
from globalCommands import commands, SCRCAT_OBJECTNAVIGATION
from globalVars import desktopObject
from logHandler import log
from .msg import message as NVDALocale
import addonHandler
import api
import controlTypes as ct
import core
import globalPluginHandler
import os
import review
import speech
import ui
import winUser

addonHandler.initTranslation()

# for compatibility
REASON_FOCUS = ct.OutputReason.FOCUS if hasattr(ct, "OutputReason") else ct.REASON_FOCUS
# for pre-2022.1 compatibility
STATE_INVISIBLE = ct.State.INVISIBLE if hasattr(ct, "State") else ct.STATE_INVISIBLE
if hasattr(ct, 'Role'):
	roles = ct.Role
else:
	roles = type('Enum', (), dict([(x.split("ROLE_")[1], getattr(ct, x)) for x in dir(ct) if x.startswith("ROLE_")]))

# to enable logging
DEBUG = False

def debugLog(message):
	if DEBUG:
		log.info(message)

# for testing performances
import time
from contextlib import contextmanager
@contextmanager
def measureTime(label):
	start = time.time()
	try:
		yield
	finally:
		end = time.time()
		debugLog("%s: %.3f s"%(label, end-start))

import ctypes
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def findAllDescendantWindows(parent, visible=None, controlID=None, className=None):
	"""See windowUtils.findDescendantWindow for parameters documentation."""
	results = []
	@WNDENUMPROC
	def callback(window, data):
		if (
			(visible is None or winUser.isWindowVisible(window) == visible)
			and (not controlID or winUser.getControlID(window) == controlID)
			and (not className or winUser.getClassName(window) == className)
		):
			results.append(window)
		return True
	# call previous func until it returns True,
	# thus always, getting all windows
	ctypes.windll.user32.EnumChildWindows(parent, callback, 0)
	# return all results
	return results

# to avoid code copying to exclude ui.message
def runWithoutUiMessage(func, *args, **kwargs):
	import config
	from versionInfo import version_year as mainVersion
	curSpeechMode = speech.speechMode if mainVersion<2021 else speech.getState().speechMode
	msgTimeout = config.conf["braille"]["messageTimeout"] if mainVersion<2023 else config.conf["braille"]["showMessages"]
	configBackup = {"voice": curSpeechMode, "braille": msgTimeout}
	if mainVersion<2021:
		speech.speechMode = speech.speechMode_off
	else:
		speech.setSpeechMode(speech.SpeechMode.off)
	if mainVersion<2023:
		config.conf["braille"]._cacheLeaf("messageTimeout", None, 0)
	else:
		config.conf["braille"]._cacheLeaf("showMessages", None, 0)
	try:
		func(*args, **kwargs)
	finally:
		if mainVersion<2021:
			speech.speechMode = configBackup["voice"]
		else:
			speech.setSpeechMode(configBackup["voice"])
		if mainVersion<2023:
			config.conf["braille"]._cacheLeaf("messageTimeout", None, configBackup["braille"])
		else:
			config.conf["braille"]._cacheLeaf("showMessages", None, configBackup["braille"])

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = SCRCAT_OBJECTNAVIGATION
	# roles of objects that could contain a toolbar
	# splitted in two tuples for probability/performance reasons
	promisingRoles = (roles.APPLICATION, roles.WINDOW, roles.DIALOG, roles.FRAME, roles.PAGE, roles.PROPERTYPAGE,)
	lessPromisingRoles = (roles.PANE, roles.OPTIONPANE, roles.BOX, roles.GROUPING, roles.DIRECTORYPANE, roles.GLASSPANE, roles.INPUTWINDOW, roles.LAYEREDPANE, roles.ROOTPANE, roles.EDITBAR, roles.TERMINAL, roles.RICHEDIT, roles.SCROLLPANE, roles.SPLITPANE, roles.VIEWPORT, roles.TEXTFRAME, roles.INTERNALFRAME, roles.DESKTOPPANE, roles.PANEL,)
	# toggle about exploration status
	exploring = False

	def configVars(self):
		"""collects and initializes starting variables."""
		# the object used as root (may be not the real root)
		self.root = None
		# current application name
		self.curAppName = None
		# a backup of review mode, focus and navigator objects, prior exploration starting
		self.startSnap = {}.fromkeys(("focus", "nav", "foreground", "pid", "reviewMode"))
		# toolbars found after search
		self.bars = []
		# index of current toolbar in exploration
		self.barIndex = 0
		# items of current toolbar
		self.barItems = []
		# index of selected item
		self.barItemIndex = None

	def findToolbars(self):
		"""the starting method to find toolbar objects."""
		self.getRoot()
		if not self.root:
			debugLog("No root found")
			return
		debugLog("root is: %s"%self.root)
		# launch search
		self.searchLauncher()
		debugLog("Found %d toolbars"%len(self.bars))

	def getRoot(self):
		"""selects or adjusts root object for search."""
		ancestors = api.getFocusAncestors()
		for ancestor in ancestors:
			if isinstance(ancestor, WindowRoot):
				self.root = ancestor
				debugLog("Use WindowRoot instance for root")
				break
		curFocus = api.getFocusObject()
		self.curAppName = curFocus.appModule.appName if curFocus.appModule else None
		debugLog("%s toolbars session"%self.curAppName)
		# root adjustments
		if self.curAppName in ("calibre",):
			while curFocus.role != roles.WINDOW:
				curFocus = curFocus.simpleParent
			self.root = curFocus.simpleParent
		elif self.curAppName in ("thunderbird",):
			# to get only toolbars for actual context
			self.root = api.getForegroundObject()
		elif self.curAppName == "explorer" and curFocus.simpleParent.simpleParent == desktopObject:
			debugLog("Desktop list detected, root adjustment")
			# set root as desktopObject
			self.root = curFocus.simpleParent.simpleParent
			# adjust appName as specified in desktopObject above (see condition later)
			self.curAppName = "csrss"
		# try a generic solution
		if (
			(not self.root)
			and
			(ancestors[0] == desktopObject)
			and
			(ancestors[1].appModule and ancestors[1].appModule.appName == self.curAppName)
		):
			debugLog("Use ancestors[1] for root")
			self.root = ancestors[1]


	def searchLauncher(self):
		"""chooses and launch appropriate search method."""
		# for applications where children sometimes disappear going to parent
		if self.curAppName in ("soffice",):
			debugLog("Try bottom-up search")
			curFocus = api.getFocusObject()
			self.bottomUpRecursiveSearch(curFocus, roles.TOOLBAR)
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
		barHandles = findAllDescendantWindows(api.getForegroundObject().windowHandle, visible=True)
		debugLog("Found %d handles"%len(barHandles))
		for handle in barHandles:
			bar = getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
			if not bar:
				continue
			if bar.role == roles.TOOLBAR:
				self.bars.append(bar)
			# some handles carry to invisible simpleParent
			# i.e. in Windows explorer
			elif not bar.isFocusable and (bar.role in self.promisingRoles or bar.role in self.lessPromisingRoles):
				# indeed, here child may be a toolbar, and bar its parent
				for child in bar.children:
					if child.role == roles.TOOLBAR:
						self.bars.append(child)

	def slowSearch(self):
		"""search toolbars using object navigation."""
		if self.curAppName in ("thunderbird","firefox","chrome",):
			outRoot = False
		else:
			outRoot = True
		if self.curAppName in ("chrome",):
			rtl = False
		else:
			rtl = True
		debugLog("Launching search with rtl=%s, outRoot=%s"%(rtl,outRoot))
		self.recursiveSearch(self.root, roles.TOOLBAR, rtl=rtl, outRoot=outRoot)
		# search gives bars in reverse order, so...
		self.bars.reverse()

	def recursiveSearch(self, obj, matchRole, rtl=True, outRoot=True):
		"""performs a filtered depth-first, right-to-left, recursive search on object hierarchy."""
		debugLog("Analyzing %s: %s"%(obj.name,obj))
		if obj.role in self.promisingRoles or obj.role in self.lessPromisingRoles:
			childObj = obj.simpleLastChild if rtl else obj.simpleFirstChild
			if childObj:
				debugLog("Go down")
				self.recursiveSearch(childObj, matchRole, rtl)
		elif obj.role == matchRole:
			self.bars.append(obj)
		# outRoot on False limits out-of-root search in first recursion
		if not outRoot:
			return
		newObj = obj.simplePrevious if rtl else obj.simpleNext
		if newObj:
			newAppName = newObj.appModule.appName if newObj.appModule else None
			if (
				(newObj.simpleParent != desktopObject)
				or
				# LibreOffice use a non-relative dialog in certain configurations
				(newObj.role == roles.DIALOG and newAppName == self.curAppName)
				or
				# try to manage starting from desktop list
				(newObj.simpleParent == self.root == desktopObject and (newAppName, self.curAppName) == ("explorer", "csrss"))
			):
				debugLog("Go previous" if rtl else "Go next")
				self.recursiveSearch(newObj, matchRole, rtl)

	def nonrecursiveSearch(self, obj, matchRole):
		"""performs a filtered breadth-first, nonrecursive search on object hierarchy.
			WARNING: this method is outdated (some condition checks lack), see recursiveSearch instead."""
		# objects to analyze in each loop iteration
		objList = [obj]
		# breadth-first search loop
		while objList:
			newObjList = []
			for obj in objList:
				if obj.role in self.promisingRoles or obj.role in self.lessPromisingRoles:
					obj = obj.simpleLastChild
					while obj and (obj.simpleParent != desktopObject or obj.role == roles.DIALOG):
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
		elif obj.role == roles.TOOLBAR:
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

	def script_startExploration(self, gesture):
		self.configVars()
		with measureTime("Toolbars found in"):
			self.findToolbars()
		self.initialFilterBars()
		if self.bars:
			self.populateBar(self.bars[self.barIndex])
		if not self.bars:
			# Translators: message in applications without toolbars
			ui.message(_("No toolbar found"))
			return
		# a backup of various info, useful later
		self.startSnap["focus"] = api.getFocusObject()
		self.startSnap["nav"] = api.getNavigatorObject()
		self.startSnap["foreground"] = api.getForegroundObject()
		self.startSnap["pid"] = api.getFocusObject().processID
		self.startSnap["reviewMode"] = review.getCurrentMode()
		# declare exploration started
		self.exploring = True
		# set object navigation active
		review.setCurrentMode("object", updateReviewPosition=False)
		# see script_explore for gesture explanation
		for direction in ("up", "right", "down", "left"):
			self.bindGesture("kb:%sArrow"%direction, "explore")
		self.bindGesture("kb:escape", "finish")
		self.bindGesture("kb:enter", "objActivate")
		self.bindGesture("kb:space", "objLeftClick")
		self.bindGesture("kb:applications", "objRightClick")
		self.bindGesture("kb:shift+f10", "objRightClick")
		bar = self.bars[self.barIndex]
		api.setNavigatorObject(bar)
		speech.speakObject(bar, reason=REASON_FOCUS)
	# Translators: input help mode message for ToolbarsExplorer start command.
	script_startExploration.__doc__ = _("Starts exploration of toolbars, if present in current application")

	def initialFilterBars(self):
		"""removes empty, duplicate or surely unwanted toolbars."""
		fixedBars = []
		for bar in self.bars:
			# remove duplicates
			if bar in fixedBars:
				# show warning: duplicate must be rare, not the usual
				debugLog("WARNING: duplicate toolbar found, %s: %s"%(bar.name, bar))
				continue
			child = bar.simpleFirstChild
			if (
				(not child)
				or
				# Mozilla apps have a toolbar with menubar as first child, purge out
				(child.role == roles.MENUBAR)
				or
				# remove Office ribbon menubar
				(len(bar.children) == 1 and child.name == "Ribbon" and child.role == roles.PROPERTYPAGE)
			):
				continue
			fixedBars.append(bar)
		debugLog("%d toolbars after initial filter"%len(fixedBars))
		self.bars = fixedBars

	def populateBar(self, bar):
		"""add toolbar children to self.barItems, excluding  unwanted objects."""
		# TODO: dinamically get barItems, without barItemIndex and barItems
		debugLog("Populate bar %s"%bar.name)
		children = bar.children
		if len(children) == 1:
			child = bar.simpleFirstChild
			# useful for Office status toolbar
			if child.role == roles.PROPERTYPAGE:
				debugLog("Integrate propertypage items")
				children = child.children
		for child in children:
			if (
				# exclude invisible and not focusable objects
				(STATE_INVISIBLE in child.states and not child.isFocusable)
				or
				# exclude separators and unknown objects
				(child.role in (roles.SEPARATOR, roles.UNKNOWN,))
				or
				# exclude tab control in Mozilla apps
				(child.role == roles.TABCONTROL and child.windowClassName == "MozillaWindowClass")
				or
				# exclude empty panes and sub-toolbars
				# but not in Eclipse, where sub-toolbars are buttons
				(self.curAppName != "eclipse" and child.role in (roles.PANE, roles.TOOLBAR,) and not child.simpleFirstChild)
			):
				debugLog("Exclude bar item name: %s; role: %d; obj: %s"%(child.name, child.role, child))
				continue
			self.barItems.append(child)
		if not self.barItems:
			debugLog("Remove bar %s at index %d"%(bar.name, self.barIndex))
			self.bars.remove(bar)
			if not self.barIndex:
				self.getBar(0)
			else:
				self.getBar(-1)
			return
		# if bar has no or useless name, rename it
		if not bar.name or bar.name.lower() in ("toolbar", "tool bar", NVDALocale("tool bar"),):
			bar.name = ' '.join([NVDALocale("tool bar"), str(self.barIndex+1)])

	def getBar(self, increment):
		"""provides toolbars circularly."""
		self.barIndex = (self.barIndex+increment)%len(self.bars)
		bar = self.bars[self.barIndex]
		# reset index and items for new bar
		self.barItemIndex = None
		self.barItems = []
		self.populateBar(bar)
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

	def script_finish(self, gesture):
		self.finish(restoreMode=True, restoreObjects=True)
#	script_finish.__doc__ = _("terminates toolbars exploration")

	def finish(self, restoreMode=False, restoreObjects=False):
		self.exploring = False
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		# restore initial objects and review mode
		if restoreMode:
			review.setCurrentMode(self.startSnap["reviewMode"], updateReviewPosition=False)
		if restoreObjects:
			api.setFocusObject(self.startSnap["focus"])
			api.setNavigatorObject(self.startSnap["nav"])
			speech.speakObject(self.startSnap["focus"], reason=REASON_FOCUS)

	def terminateIfNecessary(self, lastGesture):
		"""Tries to establish whether we are still exploring toolbars."""
		# a bit too extended, maybe, but more secure
		curFocus = api.getFocusObject()
		curNav = api.getNavigatorObject()
		curForeground = api.getForegroundObject()
		curPid = curFocus.processID
		nvdaPid = os.getpid()
		if (
			# navigator is out of toolbars
			(curNav not in self.bars and curNav not in self.barItems)
			or
			# focus is changed
			(curFocus != self.startSnap["focus"])
			or
			# foreground window is changed
			(curForeground != self.startSnap["foreground"])
			or
			# process is changed, or is NVDA (log viewer, console...)
			(curPid != self.startSnap["pid"] or curPid == nvdaPid)
			or
			# user invoked menu start
			(lastGesture.mainKeyName in ("leftWindows", "rightWindows"))
		):
			self.finish(restoreMode=True)

	def script_explore(self, gesture):
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
		# it should never happen, but, in case...
		if not newObj:
			# Translators: message presented when filtered toolbar has no elements
			ui.reviewMessage(_("No toolbar item"))
			return
		api.setNavigatorObject(newObj)
		speech.speakObject(newObj, reason=REASON_FOCUS)
#	script_explore.__doc__ = _("moves between toolbars and their items")

	def script_objActivate(self, gesture):
		# we have finished, regardless action result
		self.finish(restoreMode=True)
		# invoke activate action on current toolbar item
		runWithoutUiMessage(commands.script_review_activate, gesture)
#	script_objActivate.__doc__ = _("performs default action on selected toolbar or its item")

	def script_objLeftClick(self, gesture):
		# move mouse to current toolbar item
		runWithoutUiMessage(commands.script_moveMouseToNavigatorObject, gesture)
		# we have finished, regardless action result
		self.finish(restoreMode=True)
		# click!
		runWithoutUiMessage(commands.script_leftMouseClick, gesture)
#	script_objLeftClick.__doc__ = _("performs mouse left click on selected toolbar or its item")

	def script_objRightClick(self, gesture):
		# move mouse to current toolbar item
		runWithoutUiMessage(commands.script_moveMouseToNavigatorObject, gesture)
		# we have finished, regardless action result
		self.finish(restoreMode=True)
		# click!
		runWithoutUiMessage(commands.script_rightMouseClick, gesture)
#	script_objRightClick.__doc__ = _("performs mouse right click on selected toolbar or its item")

	def getScript(self, gesture):
		if not self.exploring:
			# return scripts mapped in __gestures
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		# find script defined here as active during exploration
		script = globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		if script:
			return script
		else:
			# then script may exist, but it's *not* defined here
			identifiers = set(gesture.identifiers[1][3:].split("+"))
			allowed = set(("NVDA", "leftAlt", "alt", "leftWindows", "rightWindows", "windows", "tab"))
			# suppress all gestures not containing allowed items
			# as system command control+z, char web navigation, etc
			# Note: numpad is to allow review gestures
			if identifiers.isdisjoint(allowed) and "numpad" not in gesture.identifiers[1]:
				# suppress execution returning a fake function
				debugLog("Suppress gesture %s"%gesture.identifiers[1])
				return lambda f: None
			else:
				# otherwise, allow execution and terminate if necessary
				# (when script action brings NVDA out of toolbars)
				debugLog("Execute gesture %s"%gesture.identifiers[1])
				core.callLater(150, self.terminateIfNecessary, gesture)
				return

	__gestures = {
	"kb:alt+applications": "startExploration",
	}

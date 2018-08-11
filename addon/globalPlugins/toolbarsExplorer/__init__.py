# ToolbarsExplorer
# A global plugin for NVDA
# Copyright 2018 Alberto Buffolino, released under GPL

# Add-on to facilitate toolbar management.
# Partially inspired by ObjNav add-on, of Joseph Lee and others.

import globalPluginHandler
from globalCommands import commands, SCRCAT_OBJECTNAVIGATION
from NVDAObjects.IAccessible import WindowRoot
from msg import message as NVDALocale
import api
import speech
import controlTypes as ct
import ui
from logHandler import log
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def findToolbars(self):
		"""the core method to find and filter toolbar objects."""
		# search root object
		for ancestor in api.getFocusAncestors():
			if isinstance(ancestor, WindowRoot):
				root = ancestor
				break
		bars = []
		# roles of objects that can contain a toolbar
		promisingRoles = [ct.ROLE_WINDOW, ct.ROLE_PANE, ct.ROLE_DIALOG, ct.ROLE_FRAME, ct.ROLE_APPLICATION, ct.ROLE_BOX, ct.ROLE_GROUPING, ct.ROLE_PROPERTYPAGE, ct.ROLE_DIRECTORYPANE, ct.ROLE_GLASSPANE, ct.ROLE_INPUTWINDOW, ct.ROLE_PAGE, ct.ROLE_LAYEREDPANE, ct.ROLE_ROOTPANE, ct.ROLE_EDITBAR, ct.ROLE_TERMINAL, ct.ROLE_RICHEDIT, ct.ROLE_SCROLLPANE, ct.ROLE_SPLITPANE, ct.ROLE_VIEWPORT, ct.ROLE_TEXTFRAME, ct.ROLE_INTERNALFRAME, ct.ROLE_DESKTOPPANE, ct.ROLE_PANEL]
		# for testing
#		self.objCount = 0
		with timeblock("recursiveSearch performed in"):
			self.recursiveSearch(root, ct.ROLE_TOOLBAR, promisingRoles, bars)
#		log.info("objCount=%d"%self.objCount)
		# search gives bars in reverse order, so...
		bars.reverse()
		# we remove toolbars without children,
		# or with menubar as first child, as in Mozilla applications,
		# and assign numbered names to anonymous toolbars
		fixedBars = []
		for bar in bars:
			child = bar.simpleFirstChild
			if child and child.role != ct.ROLE_MENUBAR:
				fixedBars.append(bar)
				if not bar.name:
					bar.name = ' '.join([NVDALocale("tool bar"), str(len(fixedBars))])
		return fixedBars

	# more efficient, used (see below)
	def recursiveSearch(self, obj, matchRole, promisingRoles, resList):
		"""performs a recursive search on object hierarchy."""
		if obj.role == matchRole and obj not in resList:
			resList.append(obj)
		childObj = obj.simpleLastChild
		if obj.role in promisingRoles and childObj:
			self.recursiveSearch(childObj, matchRole, promisingRoles, resList)
		prevObj = obj.simplePrevious
		if prevObj and prevObj.appModule == obj.appModule:
			self.recursiveSearch(prevObj, matchRole, promisingRoles, resList)
		# for testing
#		self.objCount += 1

	# less efficient, not used
	def nonrecursiveSearch(self, obj, matchRole, promisingRoles, resList):
		"""performs a nonrecursive search on object hierarchy."""
		objList = [obj]
		rootAppModule = obj.appModule
		stop = False
		# breadth first search loop
		while not stop:
			newObjList = []
			for obj in objList:
				# for testing
#				self.objCount += 1
				if obj.role == matchRole:
					resList.append(obj)
				elif obj.role in promisingRoles:
					obj = obj.simpleLastChild
					while obj and obj.appModule == rootAppModule:
						newObjList.append(obj)
						obj = obj.simplePrevious
			if newObjList:
				objList = newObjList
			else:
				stop = True

	def script_startExploration(self, gesture):
		# for testing
		with timeblock("Toolbars found in"):
			self.bars = self.findToolbars()
		if not self.bars:
			# Translators: message in applications without toolbars
			ui.message(_("No toolbar found"))
			return
		# see script_explore for gesture explanation
		for direction in ["up", "right", "down", "left"]:
			self.bindGesture("kb:%sArrow"%direction, "explore")
		self.bindGesture("kb:escape", "finish")
		self.bindGesture("kb:space", "objActivate")
		self.bindGesture("kb:enter", "objActivate")
		# a initial object backup
		self.startObj = api.getNavigatorObject()
		self.barIndex = 0
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
		if curObj in self.bars or curObj in self.barItems:
			return False
		else:
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
		log.info("{}: {}".format(label, end-start))

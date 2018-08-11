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
#from logHandler import log
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
		objList = [root]
		bars = []
		# some roles excluded to speed up toolbars searching
		# we include ROLE_TOOLBAR under assumption that nested toolbar never occurs
		excludedRoles = [ct.ROLE_MENUBAR, ct.ROLE_TOOLBAR, ct.ROLE_LIST, ct.ROLE_TREEVIEW, ct.ROLE_TABLE, ct.ROLE_DOCUMENT, ct.ROLE_DATAGRID]
		stop = False
		# breadth first search loop
		while not stop:
			newBars = filter(lambda obj: obj.role == ct.ROLE_TOOLBAR, objList)
			bars.extend(newBars)
			newObjList = []
			for obj in objList:
				if obj.role not in excludedRoles:
					newObjList.extend(obj.children)
			if newObjList:
				objList = newObjList
			else:
				stop = True
		# especially in Mozilla applications, first toolbar contains standard menubar,
		# but we don't want it, so check and remove
		if bars and bars[0].children:
			obj = bars[0].children[0]
			if obj.role == ct.ROLE_MENUBAR:
				bars.pop(0)
		# remove empty toolbars
		bars = filter(lambda bar: bar.children, bars)
		# assign numbered name to anonymous toolbars
		for x in xrange(len(bars)):
			bar = bars[x]
			if not bar.name:
				bar.name = ' '.join([NVDALocale("toolbar"), str(x+1)])
		return bars

	def script_startExploration(self, gesture):
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

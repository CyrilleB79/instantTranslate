#interface.py
# Copyright (C) 2012-2016 Aleksey Sadovoy AKA Lex <lex@progger.ru>,
#ruslan <ru2020slan@yandex.ru>,
#beqa <beqaprogger@gmail.com>
#other nvda contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import gui.guiHelper
from gui.settingsDialogs import SettingsPanel
from .langslist import getLangData
import addonHandler
from copy import deepcopy
from locale import strxfrm

addonHandler.initTranslation()

class InstantTranslateSettingsPanel(SettingsPanel):
	# Translators: name of the dialog.
	title = _("Instant Translate")

	def makeSettings(self, sizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=sizer)
		
		# Translators: Help message for a dialog.
		helpLabel = wx.StaticText(self, label=_("Select translation source and target language:"))
		sizer.Add(helpLabel)
		
		# Translators: A setting in addon settings dialog.
		fromLabelText = _("Source language:")
		# list of choices, in alphabetical order but with auto in first position
		targetChoices = self.prepareChoices(source=False)
		sourceChoices = self.prepareChoices(source=True)
		self._fromChoice = helper.addLabeledControl(fromLabelText, wx.Choice, choices=sourceChoices)
		
		# Translators: A setting in addon settings dialog.
		intoLabelText = _("Target language:")
		self._intoChoice = helper.addLabeledControl(intoLabelText, wx.Choice, choices=targetChoices)
		
		# Translators: A setting in addon settings dialog, shown if source language is on auto.
		swapLabelText = _("Language for swapping:")
		self._swapChoice = helper.addLabeledControl(swapLabelText, wx.Choice, choices=targetChoices)
		self._fromChoice.Bind(wx.EVT_CHOICE, self.onFromSelect)
		
		# Translators: A setting in addon settings dialog, shown if source language is on auto.
		self.autoSwapChk = helper.addItem(wx.CheckBox(self, label=_("Activate the auto-swap if recognized source is equal to the target (experimental)")))
		self.autoSwapChk.SetValue(self.addonConf['autoswap'])
		
		# Translators: A setting in addon settings dialog.
		self.copyTranslationChk = helper.addItem(wx.CheckBox(self, label=_("Copy translation result to clipboard")))
		self.copyTranslationChk.SetValue(self.addonConf['copytranslatedtext'])
				
		# Translators: A setting in addon settings dialog.
		self.replaceUnderscores = helper.addItem(wx.CheckBox(self, label=_("Replace underscores with spaces (May provide better translation results depending on context)")))
		self.replaceUnderscores.SetValue(self.addonConf['replaceUnderscores'])
		# Translators: A setting in addon settings dialog.
		self.useMirror = helper.addItem(wx.CheckBox(self, label=_("Use mirror (Mainly for chinese users)")))
		self.useMirror.SetValue(self.addonConf['useMirror'])
		# Translators: A setting in addon settings dialog.
		self.donateBtn = helper.addItem(wx.Button(self, label=_("Support an author...")))
		self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)

		iLang_from = self._fromChoice.FindString(getLangData()['sl'][self.addonConf['from']])
		iLang_to = self._intoChoice.FindString(getLangData()['tl'][self.addonConf['into']])
		iLang_swap = self._swapChoice.FindString(getLangData()['tl'][self.addonConf['swap']])
		
		self._fromChoice.Select(iLang_from)
		self._intoChoice.Select(iLang_to)
		self._swapChoice.Select(iLang_swap)
		if iLang_from != 0:
		 	self._swapChoice.Disable()
		 	self.autoSwapChk.Disable()

	def postInit(self):
		self._fromChoice.SetFocus()

	def onDonate(self, evt):
		from .donate_dialog import requestDonations
		requestDonations(self)

	def prepareChoices(self, source=True):
		if source:
			dic = getLangData()['sl']
		else:
			dic = getLangData()['tl']
		values = list(dic.values())
		try:
			values.remove(dic["auto"])
		except KeyError:
			pass
		values.sort(key=strxfrm)
		choices=[]
		if source:
			choices.append(dic["auto"])
		choices.extend(values)
		return choices
		
	def onFromSelect(self, event):
		if event.GetString() == getLangData()['sl']["auto"]:
			self._swapChoice.Enable()
			self.autoSwapChk.Enable()
		else:
			self._swapChoice.Disable()
			self.autoSwapChk.Disable()

	def onSave(self):
		self.addonConf['from'] = self.getDictKey(getLangData()['sl' ], self._fromChoice.GetStringSelection())
		self.addonConf['into'] = self.getDictKey(dicTargetLang, self._intoChoice.GetStringSelection())
		self.addonConf['swap'] = self.getDictKey(dicTargetLang, self._swapChoice.GetStringSelection())
		self.addonConf['copytranslatedtext'] = self.copyTranslationChk.GetValue()
		self.addonConf['autoswap'] = self.autoSwapChk.GetValue()
		self.addonConf['replaceUnderscores'] = self.replaceUnderscores.GetValue()
		self.addonConf['useMirror'] = self.useMirror.GetValue()

	def getDictKey(self, dicLang, currentValue):
		for (key, value) in dicLang.items():
			if value == currentValue:
				return key
		# set English if search fails
		return dicLang["en"]

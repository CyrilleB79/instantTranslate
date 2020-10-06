#interface.py
# Copyright (C) 2012-2016 Aleksey Sadovoy AKA Lex <lex@progger.ru>,
#ruslan <ru2020slan@yandex.ru>,
#beqa <beqaprogger@gmail.com>
#other nvda contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os.path
import sys
import wx
import gui
from .langslist import langslist, extendedLangsList
from . import langslist as lngModule
import globalVars
import config
import addonHandler
from locale import strxfrm

addonHandler.initTranslation()

class InstantTranslateSettingsPanel(gui.SettingsPanel):
	# Translators: name of the dialog.
	title = _("Instant Translate")

	def __init__(self, parent):
		super(InstantTranslateSettingsPanel, self).__init__(parent)

	def makeSettings(self, sizer):
		# Translators: Help message for a dialog.
		helpLabel = wx.StaticText(self, label=_("Select translation source and target language:"))
		helpLabel.Wrap(self.GetSize()[0])
		sizer.Add(helpLabel)
		fromSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: A setting in addon settings dialog.
		fromLabel = wx.StaticText(self, label=_("Source language:"))
		fromSizer.Add(fromLabel)
		# list of choices, in alphabetical order but with auto in first position
		fromChoiceList = self.prepareChoices(addAuto=True)
		# zh-TW is not present in sources, on site
		fromChoiceList.remove(lngModule.g("zh-TW"))
		self._fromChoice = wx.Choice(self, choices=fromChoiceList)
		fromSizer.Add(self._fromChoice)
		intoSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: A setting in addon settings dialog.
		intoLabel = wx.StaticText(self, label=_("Target language:"))
		intoSizer.Add(intoLabel)
		intoList = self.prepareChoices()
		self._intoChoice = wx.Choice(self, choices=intoList)
		intoSizer.Add(self._intoChoice)
		sizer.Add(fromSizer)
		sizer.Add(intoSizer)
		# Translators: A setting in addon settings dialog.
		self.copyTranslationChk = wx.CheckBox(self, label=_("Copy translation result to clipboard"))
		self.copyTranslationChk.SetValue(config.conf['instanttranslate']['copytranslatedtext'])
		sizer.Add(self.copyTranslationChk)
		self.swapSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: A setting in addon settings dialog, shown if source language is on auto.
		swapLabel = wx.StaticText(self, label=_("Language for swapping:"))
		self.swapSizer.Add(swapLabel)
		swapChoiceList = self.prepareChoices(addLastLang=True)
		self._swapChoice = wx.Choice(self, choices=swapChoiceList)
		self._fromChoice.Bind(wx.EVT_CHOICE, lambda event, sizer=sizer: self.onFromSelect(event, sizer))
		self.swapSizer.Add(self._swapChoice)
		sizer.Add(self.swapSizer)
		# Translators: A setting in addon settings dialog, shown if source language is on auto.
		self.autoSwapChk = wx.CheckBox(self, label=_("Activate the auto-swap if recognized source is equal to the target (experimental)"))
		self.autoSwapChk.SetValue(config.conf['instanttranslate']['autoswap'])
		sizer.Add(self.autoSwapChk)
		iLang_from = self._fromChoice.FindString(self.getDictKey(config.conf['instanttranslate']['from']))
		iLang_to = self._intoChoice.FindString(self.getDictKey(config.conf['instanttranslate']['into']))
		iLang_swap = self._swapChoice.FindString(self.getDictKey(config.conf['instanttranslate']['swap']))
		self._fromChoice.Select(iLang_from)
		self._intoChoice.Select(iLang_to)
		self._swapChoice.Select(iLang_swap)
		if iLang_from != 0:
			sizer.Hide(self.swapSizer)
			sizer.Hide(self.autoSwapChk)

	def postInit(self):
		self._fromChoice.SetFocus()

	def prepareChoices(self, addAuto=False, addLastLang=False):
		keys=list(langslist.keys())
		if sys.version_info[0] >= 3:
			keys.sort(key=strxfrm)
		else:
			# Python 2: strxfrm does not seem to work correctly, so do not use locale rules for sorting.
			keys.sort()
		if addAuto:
			auto=lngModule.g("auto")
			keys.insert(0, auto)
		if addLastLang:
			last=lngModule.g("last")
			keys.insert(0, last)
		return keys

	def onFromSelect(self, event, sizer):
		if event.GetString() == lngModule.g("auto"):
			sizer.Show(self.swapSizer)
			sizer.Show(self.autoSwapChk)
		else:
			sizer.Hide(self.swapSizer)
			sizer.Hide(self.autoSwapChk)

	def onSave(self):
		# Update Configuration
		config.conf['instanttranslate']['from'] = extendedLangsList[self._fromChoice.GetStringSelection()]
		config.conf['instanttranslate']['into'] = extendedLangsList[self._intoChoice.GetStringSelection()]
		config.conf['instanttranslate']['swap'] = extendedLangsList[self._swapChoice.GetStringSelection()]
		config.conf['instanttranslate']['copytranslatedtext'] = self.copyTranslationChk.GetValue()
		config.conf['instanttranslate']['autoswap'] = self.autoSwapChk.GetValue()

	def getDictKey(self, currentValue):
		for key, value in langslist.items():
			if value == currentValue:
				return key
		# set English if search fails
		return lngModule.g("en")

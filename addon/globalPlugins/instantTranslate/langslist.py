#langslist.py
# Copyright (C) 2012-2016 Aleksey Sadovoy AKA Lex <lex@progger.ru>,
#ruslan <ru2020slan@yandex.ru>,
#beqa <beqaprogger@gmail.com>
#other nvda contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import json
import urllib.request

from languageHandler import getLanguageDescription, getLanguage
from logHandler import log
import addonHandler
addonHandler.initTranslation()

LANG_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "langData")

def old_g(code, short=False):
	"""Return a description for the language code passed as parameter. The first found code is returned.
	The check order is the following:
	- the code in the forced codes list, i.e. codes for which NVDA/Windows do not return a satisfactory description
	- the code is in NVDA/Windows language description
	- the code in the list of needed codes, i.e. codes not available in some versions of Windows
	If all these checks fail, return the code.
	If short is True, returns a more compact description for the "auto" special code.
	"""
	if short and code == "auto":
		# Translators: A short description for "Automatically detect language" language choice, reported when
		# the user requests or swaps the current configuration.
		return _("Automatic")
	if code in forced_codes:
		return forced_codes[code]
	res = getLanguageDescription(code)
	if res is not None: return res
	if code in needed_codes:
		return needed_codes[code]
	return code

forced_codes = {
	# Translators: The name of a language supported by this add-on.
	"ckb": _("Kurdish (Sorani)"),
}

needed_codes = {
	# Translators: An option to automatically detect source language for translation.
	"auto":_("Automatically detect language"),
	# Translators: The name of a language supported by this add-on.
	"ak": _("Twi (Akan)"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"ay": _("Aymara"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"bho": _("Bhojpuri"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"bm":_("Bambara"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"ceb":_("Cebuano"),
	# Translators: The name of a language supported by this add-on.
	"doi": _("Dogri"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"ee": _("Ewe"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"eo":_("Esperanto"),
	# Translators: The name of a language supported by this add-on.
	"gom": _("Konkani"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"haw":_("Hawaiian"),
	# Translators: The name of a language supported by this add-on.
	"hmn":_("Hmong"),
	# Translators: The name of a language supported by this add-on.
	"ht":_("Creole Haiti"),
	# Translators: The name of a language supported by this add-on.
	"ilo": _("Ilocano"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"jv":_("Javanese"),
	# Translators: The name of a language supported by this add-on.
	"kri": _("Krio"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"ku":_("Kurdish"),
	# Translators: The name of a language supported by this add-on.
	"la":_("Latin"),
	# Translators: The name of a language supported by this add-on.
	"lg":  _("Luganda"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"ln": _("Lingala"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"lus": _("Mizo"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"mai": _("Maithili"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"mg":_("Malagasy"),
	# Translators: The name of a language supported by this add-on.
	"mni-Mtei": _("Meiteilon (Manipuri)"),  # Missing, tested on Windows 10 22H2
	# Translators: The name of a language supported by this add-on.
	"my":_("Myanmar (Burmese)"),
	# Translators: The name of a language supported by this add-on.
	"ny":_("Chichewa"),
	# Translators: The name of a language supported by this add-on.
	"sd":_("Sindhi"),
	# Translators: The name of a language supported by this add-on.
	"sm":_("Samoan"),
	# Translators: The name of a language supported by this add-on.
	"sn":_("Shona"),
	# Translators: The name of a language supported by this add-on.
	"so":_("Somali"),
	# Translators: The name of a language supported by this add-on.
	"st":_("Sesotho"),
	# Translators: The name of a language supported by this add-on.
	"su":_("Sundanese"),
	# Translators: The name of a language supported by this add-on.
	"tl":_("Tagalog"),
	# Translators: The name of a language supported by this add-on.
	"yi":_("Yiddish"),
}

def saveLangJson(lang, filePath):
	url = f"https://translate.googleapis.com/translate_a/l?client=gtx&hl={lang}"
	headers = {"User-Agent": "Mozilla/5.0"}
	req = urllib.request.Request(url, headers=headers)
	
	with urllib.request.urlopen(req) as response:
		data = json.loads(response.read().decode("utf-8"))

	with open(filePath, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

def loadLangJson(filePath):
	with open(filePath, "r", encoding="utf-8") as f:
		data = json.load(f)
		return data

def updateLangsList(lang=None):
	if not lang:
		lang = getLanguage()
	fileName = os.path.join(LANG_DATA_DIR, f"{lang}.json")
	saveLangJson(lang, filePath=fileName)
	
		

def langNameToReport(code, source=True):
	"""Return a description for the language code passed as parameter, to be used in the commands
	"Identify language", "Swap source and target", etc.

	The first found description is returned in the following check order:
	- for "auto", a shorter description than the one provided by Google
	- the description returned by Google
	If all these checks fail, return the code.
	"""
	
	if code == "auto":
		# Translators: A short description for "Automatically detect language" language choice, reported when
		# the user requests or swaps the current configuration.
		return _("Automatic")
	if source:
		dic = getLangData()['sl']
	else:
		dic = getLangData()['tl']
	try:
		return dic[code]
	except KeyError:
		log.debugWarning(f"Unknown language code: '{code}'")
		pass
	desc = getLanguageDescription(code)
	if desc:
		return desc
	if code in needed_codes:
		return needed_codes[code]
	return code

_langData = None
def getLangData():
	global _langData
	if _langData is None:
		_langData = loadLangJson(os.path.join(LANG_DATA_DIR, f"{getLanguage()}.json"))
	return _langData

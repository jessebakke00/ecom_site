# Komodo Haml language service.

import logging
from koXMLLanguageBase import koHTMLLanguageBase


log = logging.getLogger("koHamlLanguage")
#log.setLevel(logging.DEBUG)


def registerLanguage(registry):
    log.debug("Registering language Haml")
    registry.registerLanguage(KoHamlLanguage())


class KoHamlLanguage(koHTMLLanguageBase):
    name = "Haml"
    lexresLangName = "Haml"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" % name
    _reg_clsid_ = "{6B22D713-D6C2-4B2A-91E6-DED7C833C6ED}"
    _reg_categories_ = [("komodo-language", name)]
    None

    lang_from_udl_family = {'SSL': 'Ruby', 'M': 'HTML'}


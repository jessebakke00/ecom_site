# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# 
# The Original Code is Komodo code.
# 
# The Initial Developer of the Original Code is ActiveState Software Inc.
# Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
# ActiveState Software Inc. All Rights Reserved.
# 
# Contributor(s):
#   ActiveState Software Inc
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

# Komodo Mason language service.
#
# Generated by 'luddite.py' on Thu Jul  5 12:35:21 2007.
#

import re
import logging
from xpcom import components
from xpcom.server import UnwrapObject
from koXMLLanguageBase import koHTMLLanguageBase

from koLintResult import KoLintResult
from koLintResults import koLintResults

import scimozindent

log = logging.getLogger("koMasonLanguage")
#log.setLevel(logging.DEBUG)


def registerLanguage(registry):
    log.debug("Registering language Mason")
    registry.registerLanguage(KoMasonLanguage())


class KoMasonLanguage(koHTMLLanguageBase):
    name = "Mason"
    lexresLangName = "Mason"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" % name
    _reg_clsid_ = "{5e69ecf0-525e-11db-82d8-000d935d3368}"
    _reg_categories_ = [("komodo-language", name)]
    defaultExtension = '.mason.html'
    searchURL = "http://masonhq.com"

    lang_from_udl_family = {'CSL': 'JavaScript', 'TPL': 'Mason', 'M': 'HTML', 'CSS': 'CSS', 'SSL': 'Perl'}

    samples = """
<html>
<body>
  <%class>
  use Date::Format;
  my $date_fmt = "%A, %B %d, %Y  %I:%M %p";
  </%class>
  
  <%args>
  $.article => (required => 1)
  </%args>
  
  <div class="article">
    <h3><% $.article->title %></h3>
    <h4><% time2str($date_fmt, $.article->create_time) %></h4>
    <% $.article->content %>
  </div>
</body>
</html>
"""

    def __init__(self):
        koHTMLLanguageBase.__init__(self)
        self.matchingSoftChars[" "] = ("%", self.softchar_accept_bracket_percent_space)

    def softchar_accept_bracket_percent_space(self, scimoz, pos, style_info, candidate):
        """Look for |<%_, where these three chars are styled to indicate
        a start-perl tag, and if we find them provide the closing part.
        """
        return self.softchar_accept_styled_chars(
            scimoz, pos, style_info, candidate,
            {'curr_style' : scimoz.SCE_UDL_TPL_DEFAULT,
             'styled_chars' : [
                    (scimoz.SCE_UDL_TPL_OPERATOR, ord("%")),
                    (scimoz.SCE_UDL_TPL_OPERATOR, ord("<"))
                ]
            })

    def computeIndent(self, scimoz, indentStyle, continueComments):
        return self._computeIndent(scimoz, indentStyle, continueComments, self._style_info)

    def _computeIndent(self, scimoz, indentStyle, continueComments, style_info):
        res = self._doIndentHere(scimoz, indentStyle, continueComments, style_info)
        if res is None:
            return koHTMLLanguageBase.computeIndent(self, scimoz, indentStyle, continueComments)
        return res

    def _keyPressed(self, ch, scimoz, style_info):
        res = self._doKeyPressHere(ch, scimoz, style_info)
        if res is None:
            return koHTMLLanguageBase._keyPressed(self, ch, scimoz, style_info)
        return res

    _startWords = "init perl args".split(" ")
    def _doIndentHere(self, scimoz, indentStyle, continueComments, style_info):
        # Returns either None or an indent string
        pos = scimoz.positionBefore(scimoz.currentPos)
        startPos = scimoz.currentPos
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != ">":
            return None
        pos -= 1
        curLineNo = scimoz.lineFromPosition(pos)
        lineStartPos = scimoz.positionFromLine(curLineNo)
        delta, numTags = self._getTagDiffDelta(scimoz, lineStartPos, startPos)
        if delta < 0 and numTags == 1 and curLineNo > 0:
            didDedent, dedentAmt = self.dedentThisLine(scimoz, curLineNo, startPos)
            if didDedent:
                return dedentAmt
            else:
                # Since Mason tags end with a ">", keep the
                # HTML auto-indenter out of here.
                return self._getRawIndentForLine(scimoz, curLineNo)
        indentWidth = self._getIndentWidthForLine(scimoz, curLineNo)
        indent = scimoz.indent
        if not indent:
            indent = scimoz.tabWidth # if 0, Scintilla uses tabWidth
        newIndentWidth = indentWidth + delta * indent
        if newIndentWidth < 0:
            newIndentWidth = 0
        return scimozindent.makeIndentFromWidth(scimoz, newIndentWidth)

    def _getTagDiffDelta(self, scimoz, lineStartPos, startPos):
        data = scimoz.getStyledText(lineStartPos, startPos)
        chars = data[0::2]
        styles = [ord(x) for x in data[1::2]]
        lim = len(styles)
        delta = 0
        numTags = 0
        i = 0
        limSub1 = lim - 1
        sawSlash = False
        while i < limSub1:
            if styles[i] == scimoz.SCE_UDL_TPL_OPERATOR and chars[i] == '<':
                i += 1
                if styles[i] == scimoz.SCE_UDL_TPL_OPERATOR:
                    if chars[i] == '/':
                        sawSlash = True
                        i += 1
                if styles[i] != scimoz.SCE_UDL_TPL_OPERATOR or chars[i] != '%':
                    i += 1
                    continue
                i += 1
                while (i < lim
                       and styles[i] == scimoz.SCE_UDL_TPL_DEFAULT):
                    i += 1
                if styles[i] != scimoz.SCE_UDL_TPL_WORD:
                    return None
                wordStart = i
                while (i < lim
                       and styles[i] == scimoz.SCE_UDL_TPL_WORD):
                    i += 1
                word = chars[wordStart:i]
                if word in self._startWords:
                    numTags += 1
                    if sawSlash:
                        delta -= 1
                    else:
                        delta += 1
            else:
                i += 1
        return delta, numTags

    def _doKeyPressHere(self, ch, scimoz, style_info):
        # Returns either None or an indent string
        pos = scimoz.positionBefore(scimoz.currentPos)
        startPos = scimoz.currentPos
        style = scimoz.getStyleAt(pos)
        if style != scimoz.SCE_UDL_TPL_OPERATOR:
            return None
        if scimoz.getWCharAt(pos) != ">":
            return None
        pos -= 1
        curLineNo = scimoz.lineFromPosition(pos)
        lineStartPos = scimoz.positionFromLine(curLineNo)
        delta, numTags = self._getTagDiffDelta(scimoz, lineStartPos, startPos)
        if delta < 0 and numTags == 1 and curLineNo > 0:
            didDedent, dedentAmt = self.dedentThisLine(scimoz, curLineNo, startPos)
            if didDedent:
                return dedentAmt
        # Assume the tag's indent level is fine, so don't let the
        # HTML auto-indenter botch things up.
        return self._getRawIndentForLine(scimoz, curLineNo)

class KoMasonLinter(object):
    _com_interfaces_ = [components.interfaces.koILinter]
    _reg_desc_ = "Mason Template Linter"
    _reg_clsid_ = "{cf3671e8-6981-468c-90d1-9f77ed22b7cd}"
    _reg_contractid_ = "@activestate.com/koLinter?language=Mason;1"
    _reg_categories_ = [
        ("category-komodo-linter", 'Mason'),
    ]


    def __init__(self):
        self._koLintService = components.classes["@activestate.com/koLintService;1"].getService(components.interfaces.koILintService)
        self._perl_linter = None
        self._html_linter = UnwrapObject(self._koLintService.getLinterForLanguage("HTML"))
        
    @property
    def perl_linter(self):
        if self._perl_linter is None:
            self._perl_linter = UnwrapObject(self._koLintService.getLinterForLanguage("Perl"))
        return self._perl_linter
    
    _masonMatcher = re.compile(r'''(
                                (?:</?%\w+\s*.*?>)
        |(?:<%\s+.*?%>)   # Anything in <%...%>
        |(?:^%%?\s[^\n]+)
        |(?:\r?\n)               # Newline
        |(?:<&.*?&>)
        |[^<%\n]+ # Most other non-Perl
        |.)''',                  # Catchall
                                re.MULTILINE|re.VERBOSE|re.DOTALL)

    _blockTagRE = re.compile(r'<(/?)%(\w+).*?>')
    _exprRE = re.compile(r'(<%\s*)(.*?)(%>)', re.DOTALL)
    _perlLineRE = re.compile(r'^(%%?\s)(.*)')

    def _fixPerlPart(self, text):
        parts = self._masonMatcher.findall(text)
        if not parts:
            return "", []
        i = 0
        lim = len(parts)
        perlTextParts = []
        masonLintResults = []
        eols = ("\n", "\r\n")
        
        # states
        currTags = []
        perlTags = ('init', 'perl', 'once') # drop code for other tags.
        lineNo = i
        while i < lim:
            part = parts[i]
            if part in eols:
                perlTextParts.append(part)
            elif part.startswith("%") and (i == 0 or parts[i - 1].endswith("\n")):
                m = self._perlLineRE.match(part)
                if not m:
                    perlTextParts.append(self._spaceOutNonNewlines(part))
                else:
                    perlTextParts.append(self._spaceOutNonNewlines(m.group(1)))
                    perlTextParts.append(m.group(2))
            elif part.startswith("<"):
                m = self._blockTagRE.match(part)
                if m:
                    payload = m.group(2)
                    if m.group(1):
                        unexpectedEndTag = None
                        if currTags:
                            currTag = currTags[-1]
                            if currTag == payload:
                                currTags.pop()
                            else:
                                # Recover by removing everything up to and including the tag
                                unexpectedEndTag = currTags[-1]
                                for idx in range(len(currTags) - 1, -1, -1):
                                    if currTags[idx] == payload:
                                        del currTags[idx:-1]
                                        break
                        else:
                            unexpectedEndTag = "not in a tag block"
                        if unexpectedEndTag is not None:
                            lr = KoLintResult()
                            lr.lineStart = lr.lineEnd = lineNo + 1
                            lr.columnStart = 1
                            lr.columnEnd = 1 + len(text.splitlines()[lineNo])
                            if unexpectedEndTag == "not in a tag block":
                                lr.description = "Got end tag %s, not in a tag" % part
                            else:
                                lr.description = "Expected </%%%s>, got %s" % (
                                    unexpectedEndTag, part)
                            lr.encodedDescription = lr.description
                            lr.severity = lr.SEV_WARNING
                            masonLintResults.append(lr)
                    else:
                        currTags.append(payload)
                    perlTextParts.append(self._spaceOutNonNewlines(part))
                else:
                    m = self._exprRE.match(part)
                    if not m:
                        perlTextParts.append(self._spaceOutNonNewlines(part))
                    else:
                        perlTextParts.append(self._spaceOutNonNewlines(m.group(1)))
                        payload = m.group(2)
                        if payload.startswith("#"):
                            perlTextParts.append(payload) # One big comment
                        elif "|" not in payload:
                            perlTextParts.append("print " + payload + ";");
                        else:
                            # Filters aren't perl syntax, so punt
                            perlTextParts.append(self._spaceOutNonNewlines(m.group(2)))
                        perlTextParts.append(self._spaceOutNonNewlines(m.group(3)))
            else:
                # We only copy things out under certain circumstances
                if not currTags or currTags[-1] not in perlTags:
                    perlTextParts.append(self._spaceOutNonNewlines(part))
                else:
                    perlTextParts.append(part)
            i += 1
            lineNo += part.count("\n")
        return "".join(perlTextParts), masonLintResults
        
    _nonNewlineMatcher = re.compile(r'[^\r\n]')
    def _spaceOutNonNewlines(self, markup):
        return self._nonNewlineMatcher.sub(' ', markup)

    _markupMatcher = re.compile(r'\A<%(#|={0,2})(.*?)(=?)(?:%>)?\Z', re.DOTALL)
    def _fixTemplateMarkup(self, markup):
        m = self._markupMatcher.match(markup)
        if not m:
            return markup
        finalText = '  '
        leadingControlText = m.group(1)
        payload = m.group(2)
        trailingControlText = m.group(3)
        if leadingControlText == '#':
            finalText += '#' + payload.replace("\n", "\n#")
        elif leadingControlText.startswith("="):
            finalText += "print " + payload + ";"
        else:
            finalText += payload + ";"
        return finalText

    _tplPatterns = ("Mason", re.compile('<%'), re.compile(r'%>\s*\Z', re.DOTALL))
    def lint(self, request):
        return self._html_linter.lint(request, udlMapping={"Perl":"Mason"},
                                                    TPLInfo=self._tplPatterns)

    def lint_with_text(self, request, text):
        perlText, masonLintResults = self._fixPerlPart(text)
        if not perlText.strip():
            return
        perlLintResults = self._resetLines(self.perl_linter.lint_with_text(request, perlText),
                                            text)
        for lr in masonLintResults:
            perlLintResults.addResult(lr)
        return perlLintResults

    def _resetLines(self, lintResults, text):
        lines = text.splitlines()
        fixedResults = koLintResults()
        for res in lintResults.getResults():
            try:
                targetLine = lines[res.lineEnd - 1]
            except IndexError:
                log.exception("can't index %d lines at %d", len(lines), res.lineEnd - 1)
                pass # Keep the original lintResult
            else:
                if res.columnEnd > len(targetLine):
                    res.columnEnd = len(targetLine)
            fixedResults.addResult(res)
        return fixedResults
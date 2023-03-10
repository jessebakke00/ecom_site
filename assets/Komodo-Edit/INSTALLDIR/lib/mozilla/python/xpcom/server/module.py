# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python XPCOM language bindings.
#
# The Initial Developer of the Original Code is ActiveState Tool Corp.
# Portions created by ActiveState Tool Corp. are Copyright (C) 2000, 2001
# ActiveState Tool Corp.  All Rights Reserved.
#
# Contributor(s):
#   Mark Hammond <MarkH@ActiveState.com> (original author)
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

from xpcom import components, ServerException, nsError
from factory import Factory

class Module:
    _com_interfaces_ = components.interfaces.nsIModule
    def __init__(self, comps):
        # Build a map of classes we can provide factories for.
        c = self.components = {}
        for klass in comps:
            c[components.ID(klass._reg_clsid_)] = klass
        self.klassFactory = Factory

    def getClassObject(self, compMgr, clsid, iid):
        # Single retval result.
        try:
            klass = self.components[clsid]
        except KeyError:
            raise ServerException(nsError.NS_ERROR_FACTORY_NOT_REGISTERED)
        
        # We can ignore the IID - the auto-wrap process will automatically QI us.
        return self.klassFactory(klass)

    def registerSelf(self, compMgr, location, loaderStr, componentType):
        # No longer called by XPCOM.
        raise RuntimeError("Module::registerSelf should never get called")

    def unregisterSelf(self, compMgr, location, loaderStr):
        # No longer called by XPCOM.
        raise RuntimeError("Module::unregisterSelf should never get called")

    def canUnload(self, compMgr):
        # single bool result
        return 0 # we can never unload!

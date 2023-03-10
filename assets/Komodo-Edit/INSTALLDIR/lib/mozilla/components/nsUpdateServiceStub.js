/* -*- indent-tabs-mode: nil; js-indent-level: 2 -*- */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const Ci = Components.interfaces;
const Cc = Components.classes;
const Cu = Components.utils;

Cu.import("resource://gre/modules/XPCOMUtils.jsm");
Cu.import("resource://gre/modules/FileUtils.jsm");
Cu.import("resource://gre/modules/Services.jsm");

const DIR_UPDATES         = "updates";
const FILE_UPDATES_DB     = "updates.xml";
const FILE_UPDATE_ACTIVE  = "active-update.xml";
const FILE_LAST_LOG       = "last-update.log";
const FILE_BACKUP_LOG     = "backup-update.log";
const FILE_UPDATE_STATUS  = "update.status";

const KEY_UPDROOT         = "UpdRootD";

//@line 136 "/home/komodo-build/mozbuilds/release/edit-12.0/hg-ff-35.0.0/mozilla/toolkit/mozapps/update/nsUpdateServiceStub.js"

/**
 * Gets the specified directory at the specified hierarchy under the update root
 * directory without creating it if it doesn't exist.
 * @param   pathArray
 *          An array of path components to locate beneath the directory
 *          specified by |key|
 * @return  nsIFile object for the location specified.
 */
function getUpdateDirNoCreate(pathArray) {
  return FileUtils.getDir(KEY_UPDROOT, pathArray, false);
}

function UpdateServiceStub() {
//@line 166 "/home/komodo-build/mozbuilds/release/edit-12.0/hg-ff-35.0.0/mozilla/toolkit/mozapps/update/nsUpdateServiceStub.js"

  let statusFile = getUpdateDirNoCreate([DIR_UPDATES, "0"]);
  statusFile.append(FILE_UPDATE_STATUS);
  // If the update.status file exists then initiate post update processing.
  if (statusFile.exists()) {
    let aus = Components.classes["@mozilla.org/updates/update-service;1"].
              getService(Ci.nsIApplicationUpdateService).
              QueryInterface(Ci.nsIObserver);
    aus.observe(null, "post-update-processing", "");
  }
}
UpdateServiceStub.prototype = {
  observe: function(){},
  classID: Components.ID("{e43b0010-04ba-4da6-b523-1f92580bc150}"),
  QueryInterface: XPCOMUtils.generateQI([Ci.nsIObserver])
};

this.NSGetFactory = XPCOMUtils.generateNSGetFactory([UpdateServiceStub]);

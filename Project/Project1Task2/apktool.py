import subprocess
import os
from xml.etree import ElementTree as ET
from shutil import which, rmtree
from logger import dbg, err

TMP_APK_DIR = "apk_dec"
PERM_KEY = "{http://schemas.android.com/apk/res/android}name"

# Runs APK tool
def _run_apktool(app_path: str) -> bool:
    args = ["apktool", "d", app_path, "--output", TMP_APK_DIR]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    return True if p.returncode == 0 else False


# Cleans up any files created by apktool
def _cleanup():
    if os.path.isdir(TMP_APK_DIR):
        rmtree(TMP_APK_DIR)


# Extract from XML
def _extract_permissions():
    manifest_path = os.path.join(TMP_APK_DIR, "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        err("Could not locate the `AndroidManifest.xml` file")
        return []
    # File is present
    root = ET.parse(manifest_path).getroot()
    perms = root.findall("uses-permission")

    # Collect permissions and return them
    permList = []
    for perm in perms:
        permList.append(perm.attrib[PERM_KEY])

    return permList


# Check if apktool is present in PATH
_is_apktool_present = lambda: which("apktool") is not None


# Main method
def get_app_permissions(app_path: str) -> list:
    # Cleanup once before we start
    _cleanup()
    dbg(f"Extracting permissions for {app_path}")
    if not _is_apktool_present:
        err(f"Could not find `apktool` in PATH")
        return []
    if not _run_apktool(app_path):
        err(f"`apktool` encountered an error!")
        return []

    # Extract permissions
    permList = _extract_permissions()

    # Cleanup after
    _cleanup()

    # Return
    dbg("Done!")
    return permList

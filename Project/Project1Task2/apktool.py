import subprocess
import os
from xml.etree import ElementTree as ET
from shutil import which, rmtree
from logger import dbg, err

TMP_APK_DIR = "apk_dec"
PERM_KEY = "{http://schemas.android.com/apk/res/android}name"

# Runs APK tool
def _run_apktool(app_path: str, thread_num: int) -> bool:
    args = ["apktool", "d", app_path, "--output", f"{TMP_APK_DIR}_{thread_num}"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    return True if p.returncode == 0 else False


# Cleans up any files created by apktool
def _cleanup(thread_num: int):
    if os.path.isdir(f"{TMP_APK_DIR}_{thread_num}"):
        rmtree(f"{TMP_APK_DIR}_{thread_num}")


# Extract from XML
def _extract_permissions(thread_num: int):
    manifest_path = os.path.join(f"{TMP_APK_DIR}_{thread_num}", "AndroidManifest.xml")
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
def get_app_permissions(app_path: str, thread_num) -> list:
    # Cleanup once before we start
    _cleanup(thread_num)
    dbg(f"Extracting permissions for {app_path} on thread {thread_num}")
    if not _is_apktool_present:
        err(f"Could not find `apktool` in PATH")
        return []
    if not _run_apktool(app_path, thread_num):
        err(f"`apktool` encountered an error!")
        return []

    # Extract permissions
    permList = _extract_permissions(thread_num)

    # Cleanup after
    _cleanup(thread_num)

    # Return
    dbg("Done!")
    return permList

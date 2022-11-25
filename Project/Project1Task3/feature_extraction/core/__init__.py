from dataclasses import dataclass
from zipfile import ZipFile
from os import path, walk
from shutil import which
from androguard.core.bytecodes.axml import AXMLPrinter
from lxml.etree import _Element
from logging import getLogger

import subprocess

logger = getLogger("FE.CORE")

HTTP_REGEX = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
EMAIL_REGEX = "[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

@dataclass
class RawApkData:
    """
    An object of all the data collected from an APK

    mainfest: AndroidManifest.xml
    """

    apk_name: str
    manifest: _Element
    implicit_intents: list[str]
    urls: list[str]
    emails: list[str]


def extract_source_code(zf: ZipFile, member_name: str, file_path: str):
    
    # This will only happen on the first run for feature extractions
    dest_dir = "extracted_code" + file_path[file_path.rfind("/") :]
    
    if not path.exists(dest_dir):
        zf.extract(member_name, dest_dir)

        jadx_installed = which("jadx")
        if jadx_installed is None:
            logger.error("JADX is not installed, but is required for feature extraction!")
            return

        cmd = ["jadx", "-d", dest_dir, f"{dest_dir}/{member_name}"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()


def get_features_data(file_path: str) -> tuple[list[str], list[str], list[str]]:

    source_dir = "extracted_code" + file_path[file_path.rfind("/") :]

    file_list = []
    for root, dirs, files in walk(source_dir):
        for file in files:
            file_list.append(path.join(root,file))

    java_files = list(filter(lambda file_name: file_name.endswith(".java"), file_list))

    implicit_intents = []
    urls = []
    emails = []

    for file_name in java_files:
        with open(file_name, "r") as java_file:
            for line in java_file.readlines():

                # Check if the current line has any implicit intents
                if ("android.intent.action" in line or "Intent.ACTION" in line) and "new Intent" in line:
                    implicit_intents.append(line.strip())
                
                # Check if the current line has any URLs
                if re.search(HTTP_REGEX, line) is not None:
                    urls.append(line.strip())
                
                # Check if the current line has any URLs
                if re.search(EMAIL_REGEX, line) is not None:
                    emails.append(line.strip())
    
    return implicit_intents, urls, emails


async def get_raw_elements(file_path: str):
    """
    Extracts manifest and other important data from APK files and stores them
    in a RawApkData structure. Returns data or None if something goes wrong

    file_path: Absolute path to the application
    """
    if not path.exists(file_path):
        logger.error(f"Path doesn't exist: {file_path}")
        return None

    # Now that we have confirmed that the file exists, we will
    # read it as a zip file and extract the elements that we need
    # from it

    logger.info(f"Attempting to open: {file_path}")

    try:
        with ZipFile(file_path) as zf:
            implicit_intents = 0

            for name in zf.namelist():
                if ".dex" in name:
                    extract_source_code(zf, name, file_path)
                    implicit_intents, urls, emails = get_features_data(file_path)

            # Check if manifest exists in the file list
            if "AndroidManifest.xml" not in zf.namelist():
                # Return with manifest_xml as None
                logger.warn(f"Could not find AndroidManifest.xml for: {file_path}")
                return RawApkData(path.basename(file_path), None, implicit_intents, urls, emails)

            manifest_binary = zf.read("AndroidManifest.xml")

            # Turn the binary XML to read XML
            manifest_xml = AXMLPrinter(manifest_binary).get_xml_obj()

            return RawApkData(path.basename(file_path), manifest_xml, implicit_intents, urls, emails)

    except:
        # Maybe a bad zip file?
        logger.error(f"Failed to extract APK for: {file_path}")
        return None

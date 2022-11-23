from dataclasses import dataclass
from zipfile import ZipFile
from os import path
from androguard.core.bytecodes.axml import AXMLPrinter
from lxml.etree import _Element
from logging import getLogger

logger = getLogger("FE.CORE")


@dataclass
class RawApkData:
    """
    An object of all the data collected from an APK

    mainfest: AndroidManifest.xml
    """

    apk_name: str
    manifest: _Element


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
            # Check if manifest exists in the file list
            if "AndroidManifest.xml" not in zf.namelist():
                return None

            manifest_binary = zf.read("AndroidManifest.xml")

            # Turn the binary XML to read XML
            manifest_xml = AXMLPrinter(manifest_binary).get_xml_obj()

            return RawApkData(path.basename(file_path), manifest_xml)

    except:
        # Maybe a bad zip file?
        logger.error(f"Failed to extract APK for: {file_path}")
        return None

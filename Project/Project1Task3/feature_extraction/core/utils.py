import pickle as pkl
import zlib
from lxml import etree

from feature_extraction.core import RawApkData


def serialize_feats(mal_data: list[RawApkData], ben_data: list[RawApkData]):
    mal_base_data = {}
    mal_xmls = {}
    for mal in mal_data:
        mal_base_data[mal.apk_name] = {
            "emails": mal.emails,
            "implicit_intents": mal.implicit_intents,
            "urls": mal.urls,
        }
        mal_xmls[mal.apk_name] = (
            zlib.compress(etree.tostring(mal.manifest))
            if mal.manifest is not None
            else None
        )

    with open("mal_data.pkl", "wb") as f:
        pkl.dump({"base": mal_base_data, "xmls": mal_xmls}, f)

    ben_base_data = {}
    ben_xmls = {}
    for ben in ben_data:
        ben_base_data[ben.apk_name] = {
            "emails": ben.emails,
            "implicit_intents": ben.implicit_intents,
            "urls": ben.urls,
        }
        ben_xmls[ben.apk_name] = zlib.compress(etree.tostring(ben.manifest))

    with open("ben_data.pkl", "wb") as f:
        pkl.dump({"base": ben_base_data, "xmls": ben_xmls}, f)


def deserialize_feats(mal_file_path, ben_file_path):
    mal_list: list[RawApkData] = []
    ben_list: list[RawApkData] = []
    with open(mal_file_path, "rb") as f:
        data = pkl.load(f)
        for k, v in data["base"].items():
            xml = (
                etree.fromstring(zlib.decompress(data["xmls"]["manifest"]))
                if data["xmls"]["manifest"] is not None
                else None
            )
            mal_list.append(
                RawApkData(
                    apk_name=k,
                    implicit_intents=v["implicit_intents"],
                    manifest=xml,
                    urls=v["urls"],
                    emails=v["emails"],
                )
            )

    with open(ben_file_path, "rb") as f:
        data = pkl.load(f)
        for k, v in data["base"].items():
            xml = (
                etree.fromstring(zlib.decompress(data["xmls"]["manifest"]))
                if data["xmls"]["manifest"] is not None
                else None
            )
            ben_list.append(
                RawApkData(
                    apk_name=k,
                    implicit_intents=v["implicit_intents"],
                    manifest=xml,
                    urls=v["urls"],
                    emails=v["emails"],
                )
            )

    return mal_list, ben_list

"""
Utility for outputting top 10 permissions in a set of android applications.

Usage: python3 get_top_perms -m path/to/maliciousapps/folder
"""

import argparse
from feature_extraction import *
import asyncio


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--malware", type=str, help="Path to malware APKs", required=True
    )

    args = parser.parse_args()

    mal_apps, _ = asyncio.run(extract_features(args.malware, args.malware))

    perm_map = {}
    perm_name_key = "{http://schemas.android.com/apk/res/android}name"

    # Start counting
    for app in mal_apps:
        if app.manifest is None:
            continue

        perms = app.manifest.findall("uses-permission")

        for perm in perms:
            if perm_name_key in perm.keys():
                perm_name = perm.attrib[perm_name_key]
                if perm_name in perm_map.keys():
                    perm_map[perm_name] += 1
                else:
                    perm_map[perm_name] = 1

    # Sort and see the top
    perm_map = sorted(perm_map.items(), key=lambda x: x[1], reverse=True)

    print("#" * 80)
    print("#### Top 10 permissions -- ")
    print("#" * 80)
    pprint(perm_map[:10])

import json
from pprint import pprint
from itertools import islice


def get_most_freq_perms(all_perms):
    permMap = {}

    for perm in all_perms:
        for p in perm:
            if p in permMap:
                permMap[p] += 1
            else:
                permMap[p] = 1

    # Sort this
    permMap = sorted(permMap.items(), key=lambda x: x[1], reverse=True)

    # Slice and print the top 10
    print("-" * 80)
    print("Top 10 most frequent permissions")
    print("-" * 80)
    print("{:>30}{:>35}".format("Permission", "Number of apps"))
    print("-" * 80)
    for k, v in permMap[:10]:
        print("{:>44}{:>15}".format(k, v))


if __name__ == "__main__":
    ### Just tests, do not run this as the main file
    ### Always run `python3 main.py`
    all_perms = ""
    with open("perms.json", "r") as f:
        all_perms = json.loads(f.read())

    get_most_freq_perms(all_perms)

APP_PERMS_LEN = {}


def display_top_apps(top_10_apps):
    print("\nTop 10 apps with most permissions:\n")

    for apk_name, num_of_perms in top_10_apps.items():
        print(f"APK: {apk_name}, number of permissions: {num_of_perms}")


def get_top_10_apps(apks, all_perms):
    
    for i, apk in enumerate(apks):
        APP_PERMS_LEN[apk] = len(all_perms[i])
    
    sorted_apps = sorted(APP_PERMS_LEN.items(), key=lambda item:item[1], reverse=True)
    
    top_apps = dict(sorted_apps)
    top_10_apps = {apk_name: top_apps[apk_name] for apk_name in list(top_apps)[:10]}
    
    display_top_apps(top_10_apps)
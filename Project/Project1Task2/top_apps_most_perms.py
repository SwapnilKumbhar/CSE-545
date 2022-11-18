APP_PERMS_LEN = {}


def display_top_apps(top_10_apps):
    
    print("\nTop 10 apps with most permissions:\n")

    # For every app, display the APK name and its corresponding number of permissions
    index = 1

    for apk_name, num_of_perms in top_10_apps.items():
        print(f"{index}. APK: {apk_name}, number of permissions: {num_of_perms}")
        index += 1


def get_top_10_apps(apks, all_perms):
    
    # Map every APK to the number of permissions it requests
    for i, apk in enumerate(apks):
        number_of_perms = len(all_perms[i])
        APP_PERMS_LEN[apk] = number_of_perms
    
    # Sort the map based on the number of permissions in a descending order
    sorted_apps = sorted(APP_PERMS_LEN.items(), key=lambda item:item[1], reverse=True)
    
    # Put the sorted apps in a dictionary
    top_apps = dict(sorted_apps)

    # Get the top 10 apps with most permissions
    top_10_apps_list = list(top_apps)[:10]
    top_10_apps = {apk_name: top_apps[apk_name] for apk_name in top_10_apps_list}
    
    # Display the top 10 apps with most permissions
    display_top_apps(top_10_apps)
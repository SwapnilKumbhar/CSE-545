import apktool

if __name__ == "__main__":
    perms = apktool.get_app_permissions("../../../selectedAPKs/es.library.apk")

    print(perms)

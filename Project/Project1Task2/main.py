#!/usr/bin/python3

import apktool
import os
import threading
import top_apps_most_perms
import chart
import top_permissions

APKS_PATH = "selectedAPKs/"
ALL_PERMS = []

def get_perms(file_path, thread_num):
    ALL_PERMS[thread_num] = apktool.get_app_permissions(file_path, thread_num)

if __name__ == "__main__":
    all_apks = []
    
    for file_path in os.listdir(APKS_PATH):
        all_apks.append(APKS_PATH + file_path)
    
    ALL_PERMS = [[]] * len(all_apks)

    for i in range(0, len(all_apks) // 20 + 1):
        threads = []
        all_apks_processed = False

        # create all n threads (n <= 20)
        for j in range(i * 20, i * 20 + 20):
            if j >= len(all_apks):
                all_apks_processed = True
                break
            threads.append(threading.Thread(target=get_perms, args=(all_apks[j],j,)))

        if all_apks_processed and len(threads) == 0: break

        # start all n threads
        for j in range(0, len(threads)):
            threads[j].start()
        
        # join all n threads
        for j in range(0, len(threads)):
            threads[j].join()

    # Question 1
    # TODO by Swapnil

    # Question 2
    top_apps_most_perms.get_top_10_apps(all_apks, ALL_PERMS)
    
    # Question 3
    chart.create_line_chart(ALL_PERMS)
    top_permissions.get_most_freq_perms(ALL_PERMS)

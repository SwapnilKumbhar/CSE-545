import matplotlib.pyplot as plt
import numpy as np


def plot_chart(number_of_perms, number_of_apps):
    number_of_perms_arr = np.array(number_of_perms)
    number_of_apps_arr = np.array(number_of_apps)
    
    plt.rcParams["figure.figsize"] = (15,10)

    plt.title("Permission statistics")
    plt.xlabel("Number of permissions requested by apps")
    plt.ylabel("Number of apps requesting respective permissions")

    plt.xticks(np.arange(min(number_of_perms), max(number_of_perms)+1, 3.0))
    plt.yticks(np.arange(min(number_of_apps), max(number_of_apps)+1, 1.0))

    plt.plot(number_of_perms_arr, number_of_apps_arr)
    plt.savefig("line_chart.png")


def create_line_chart(app_perms):

    unique_perm_occurences = list({len(perms) for perms in app_perms})

    max_perms = max(unique_perm_occurences)
    
    perms = [i for i in range(0, max_perms + 1)]
    number_of_apps = [0] * len(perms)

    for app_perm in app_perms:
        number_of_perms = len(app_perm)
        number_of_apps[number_of_perms] += 1
    
    plot_chart(perms, number_of_apps)
    
    
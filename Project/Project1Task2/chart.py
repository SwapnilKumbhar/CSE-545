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

    perm_occurences_to_index_dict = {}

    for index, unique_occurence in enumerate(unique_perm_occurences):
        perm_occurences_to_index_dict[unique_occurence] = index

    number_of_apps = [0] * len(unique_perm_occurences)

    for app_perm in app_perms:
        number_of_perms = len(app_perm)
        occurences_index = perm_occurences_to_index_dict[number_of_perms]
        number_of_apps[occurences_index] += 1
    
    plot_chart(unique_perm_occurences, number_of_apps)
    
    
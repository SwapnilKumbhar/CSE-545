import matplotlib.pyplot as plt
import numpy as np


def plot_chart(number_of_perms, number_of_apps):

    number_of_perms_arr = np.array(number_of_perms)
    number_of_apps_arr = np.array(number_of_apps)
    
    # Set chart dimensions
    plt.rcParams["figure.figsize"] = (15,10)

    # Set chart labels
    plt.title("Permission statistics")
    plt.xlabel("Number of permissions requested by apps")
    plt.ylabel("Number of apps requesting respective permissions")

    # Set chart ticks (i.e. intervals on both axes)
    plt.xticks(np.arange(min(number_of_perms), max(number_of_perms)+1, 3.0))
    plt.yticks(np.arange(min(number_of_apps), max(number_of_apps)+1, 1.0))

    # Plot and save the chart
    plt.plot(number_of_perms_arr, number_of_apps_arr)
    plt.savefig("line_chart.png")


def create_line_chart(app_perms):

    # Get all unique number of permissions requested by apps
    unique_perm_occurences = list({len(perms) for perms in app_perms})

    # Get the maximum number of permissions requested by a single app
    max_perms = max(unique_perm_occurences)
    
    # Store the number of permissions in a list ranging from 0 to max_perms, i.e. [0, 1, 2, ..., max_perms]
    # Here every value represents the number of permissions
    perms = [i for i in range(0, max_perms + 1)]
    
    # Store the number of apps that require each number of permissions value in number_of_apps list
    number_of_apps = [0] * len(perms)

    for app_perm in app_perms:
        number_of_perms = len(app_perm)
        number_of_apps[number_of_perms] += 1
    
    # Plot number of permissions vs. number of apps that require corresponding number of permissions
    plot_chart(perms, number_of_apps)
    
    
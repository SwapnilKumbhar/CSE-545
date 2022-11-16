# Project 1 Task 2

The goal is to analyze a set of APKs using `apktool`.

## Setting up and running the code

The code requires Python version 3.7 and up. Further, it will also require the `virtualenv` (venv) package on the machine.

To set up the environment, open the project's folder in the terminal and run the following --

```sh
python3 -m venv venv                  # Create a virtual environment
source venv/bin/activate              # Activate the virtual environment
pip3 install -r requirements.txt      # Install dependencies in the virtual environment
```

> `python3` or `pip3` could also be named `python` or `pip` on your machine. Please run it accordingly.

Before running the code, **ensure that the `selectedAPKs` folder is in the same directory as the code**. The code will not run if it is not in the same folder.

To run the code, with the virtual environment activated, run --

```sh
./main.py
```

You'll see the results printed on the terminal for the first two problems. The line chart for the last problem will be saved in the same folder under the name `line_chart.png`.

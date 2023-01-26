# LeagueofLegends-AutoZhonya
Simple Python script to activate Zhonya's Hourglass or Stopwatch based on defined health threshold.


[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/mnyrLg9XK9I/0.jpg)](http://www.youtube.com/watch?v=mnyrLg9XK9I)


# Introduction

This repository contains a Python script that utilizes the League of Legends Game Client API to automatically use in-game items (stopwatch and zhonya) when the player's health falls below a certain threshold. The script uses the requests library to make API calls and the pyautogui library to simulate keypresses for activating the items. The script also uses the json library to parse the API's JSON response.

The user can specify their desired health threshold and the names of the items they wish to use in the script.

### Prerequisites

- pipenv

Install pipenv in the command line/terminal by typing pip install pipenv or pip3 install pipenv

# Setup

* Clone this repository to your local machine.
* In the command line, navigate to the project's root directory and run the following command to install the required dependencies:

```
pipenv install
```

* Activate the virtual environment:

```
pipenv shell
```

* Open the script in a code editor and update the health_threshold variable to your desired value.
* Run the script using your preferred method (e.g. command line, code editor's built-in terminal, etc.)

# Requirements

* Python 3.10 +

* League of Legends Game

* League of Legends Game Client API

* Requests library

* Pyautogui library

* json library

* cert file (included)


# Note

This script is for educational purposes only and should not be used to gain an unfair advantage in-game. The script is also intended for use in custom games and not in real matches.



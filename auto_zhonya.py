import requests
import json
import time
import pyautogui


def find_summoner_name(data):
    return data["activePlayer"]["summonerName"]


def find_item_slot(data, player, item_name):
    for p in data["allPlayers"]:
        if p["summonerName"] == player:
            for item in p["items"]:
                if item["displayName"] == item_name:
                    return item["slot"]
    return None


def check_health(data, health_threshold):
    if data["activePlayer"]["championStats"]["currentHealth"] <= health_threshold:
        return True
    else:
        return False


def is_alive(data, player):
    for p in data["allPlayers"]:
        if p["summonerName"] == player and p["isDead"] == False:
            return True
    return False


def use_item(data, player, item_name, health_threshold):
    item_slot = find_item_slot(data, player, item_name)
    if item_slot is not None:
        if check_health(data, health_threshold):
            print(item_name, "activated")
            pyautogui.press(str(item_slot + 1))
            time.sleep(120)


# SSL certificate to avoid errors
cert_path = "LoL Game Engineering Certificate Authority.crt"

response = requests.get(
    "https://127.0.0.1:2999/liveclientdata/allgamedata", verify=cert_path
)
data = json.loads(response.text)

# Get summoner's name
player = find_summoner_name(data)

# Leave as is
stopwatch_name = "Stopwatch"
zhonya_name = "Zhonya's Hourglass"

# User defined health threshold - Adjust to your liking
health_threshold = 225

while player:
    response = requests.get(
        "https://127.0.0.1:2999/liveclientdata/allgamedata", verify=cert_path
    )
    data = json.loads(response.text)

    # Checks whether the player is dead or alive.
    if is_alive(data, player):
        use_item(data, player, stopwatch_name, health_threshold)
        use_item(data, player, zhonya_name, health_threshold)

    # Add a delay - Turn off for faster response but may affect ping.
    time.sleep(0.3)

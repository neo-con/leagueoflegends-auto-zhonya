import requests
import json
import time
import pyautogui


class Summoner:
    def __init__(self, data):
        self.name = data["activePlayer"]["summonerName"]
        self.health_threshold = 225
        self.update(data)

    def update(self, data):
        self.health = data["activePlayer"]["championStats"]["currentHealth"]
        for player in data["allPlayers"]:
            if player["summonerName"] == self.name:
                self.items = player["items"]
                self.is_dead = player["isDead"]

    def find_item_slot(self, item_name):
        for item in self.items:
            if item["displayName"] == item_name:
                return item["slot"]
        return None

    def check_health(self):
        return self.health <= self.health_threshold

    def is_alive(self):
        return not self.is_dead


class GameClient:
    BASE_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    CERT_PATH = "LoL Game Engineering Certificate Authority.crt"

    def __init__(self):
        self.data = self._get_data()

    def _get_data(self):
        try:
            response = requests.get(self.BASE_URL, verify=self.CERT_PATH)
            return json.loads(response.text)
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the game. Ensure the game is running and try again.")
            return None

    def update(self):
        data = self._get_data()
        if data:
            self.data = data
        else:
            self.data = None



def use_item(summoner, item_name):
    item_slot = summoner.find_item_slot(item_name)
    if item_slot is not None and summoner.check_health():
        print(item_name, "activated")
        pyautogui.press(str(item_slot + 1))
        time.sleep(120)


if __name__ == "__main__":
    client = GameClient()
    if not client.data:
        exit()  # Exit if we couldn't get initial game data

    player = Summoner(client.data)
    stopwatch_name = "Stopwatch"
    zhonya_name = "Zhonya's Hourglass"

    while player.name:
        client.update()
        if not client.data:
            print("Lost connection to the game. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            continue

        player.update(client.data)

        # Only activate items if the game connection is active and the player is alive
        if client.data and player.is_alive():
            use_item(player, stopwatch_name)
            use_item(player, zhonya_name)

        time.sleep(0.3)
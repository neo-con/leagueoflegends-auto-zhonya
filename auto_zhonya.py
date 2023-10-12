import requests
import json
import time
import pyautogui
import logging


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
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Unable to connect to the game. Error: {e}")
            return None

    def update(self):
        data = self._get_data()
        if data:
            self.data = data
        else:
            self.data = None


class ItemActivator:
    def __init__(self, summoner):
        self.summoner = summoner

    def use_item(self, item_name):
        item_slot = self.summoner.find_item_slot(item_name)
        if item_slot is not None and self.summoner.check_health():
            logging.info(f"{item_name} activated")
            pyautogui.press(str(item_slot + 1))
            time.sleep(120)


def main():
    logging.basicConfig(level=logging.INFO)

    client = GameClient()
    if not client.data:
        return

    player = Summoner(client.data)
    activator = ItemActivator(player)

    stopwatch_name = "Stopwatch"
    zhonya_name = "Zhonya's Hourglass"

    while player.name:
        client.update()
        if not client.data:
            logging.error("Lost connection to the game. Retrying...")
            time.sleep(5)
            continue

        player.update(client.data)

        if client.data and player.is_alive():
            activator.use_item(stopwatch_name)
            activator.use_item(zhonya_name)

        time.sleep(0.3)


if __name__ == "__main__":
    main()

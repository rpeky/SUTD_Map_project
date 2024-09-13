import httplib2 as http
import json
import requests
import time
from urllib.parse import urlparse

import Path_query

# Base URL for Telegram API
BASE_URL = 'https://api.telegram.org/bot7338576036:AAEpgpNoLoja05lQyvx7R3WgEBk5Bzgvy5Y/'

# Fetch updates from the Telegram bot
def get_updates(offset=None):
    url = BASE_URL + 'getUpdates'
    if offset:
        url += f'?offset={offset}'
    response = requests.get(url)
    return response.json()

# Extract chat ID from the latest update
def get_chatid(updates):
    if updates.get("ok") and updates["result"]:
        return str(updates["result"][-1]["message"]["chat"]["id"])
    return None

# Send message through the Telegram bot
def send_tele_message(chatid, msg, reply_markup=None):
    url = BASE_URL + 'sendMessage'
    payload = {'chat_id': chatid, 'text': msg}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    response = requests.post(url, data=payload)
    print("Response:", response.content)
    return response.json()

# Poll for the next message from a specific chat ID
def wait_for_next_message(chat_id, timeout=60):
    start_time = time.time()
    offset = None
    while time.time() - start_time < timeout:
        updates = get_updates(offset)
        if updates.get("ok") and updates["result"]:
            for update in updates["result"]:
                message = update.get("message")
                if message and message["chat"]["id"] == chat_id:
                    return message.get("text", "")
                offset = update["update_id"] + 1
        time.sleep(2)
    return None

# Handle different callback queries -- lol ai solutions kinda troll wth
def handle_callback_query(callback_query):
    chat_id = callback_query['message']['chat']['id']
    callback_data = callback_query['data']
    
    if callback_data == "location_explorer":
        send_tele_message(chat_id, "Please provide a location name or ID:")
        # You can add logic here to fetch and display location details
    elif callback_data == "pathfinding":
        send_tele_message(chat_id, "Please enter the start location:")
        start_location = wait_for_next_message(chat_id)
        send_tele_message(chat_id, "Please enter the end location:")
        end_location = wait_for_next_message(chat_id)
        # Call pathquery.py logic here to get the route
        route = get_route(start_location, end_location)  # Replace with your function
        send_tele_message(chat_id, f"Your route is: {route}")

# Main menu options for user interaction
def main_menu_loadout(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Location Explorer", "callback_data": "location_explorer"},
             {"text": "Pathfinding", "callback_data": "pathfinding"}]
        ]
    }
    send_tele_message(chat_id, "Choose an option:", reply_markup=keyboard)

# Main polling loop to handle bot updates
def main():
    offset = None
    print("Bot is running...")
    while True:
        updates = get_updates(offset)
        if updates.get("ok") and updates["result"]:
            for update in updates["result"]:
                message = update.get("message")
                if message:
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "")
                    print(f"User said: {text}")
                    send_tele_message(chat_id, f"You said: {text}")
                    main_menu_loadout(chat_id)
                    offset = update["update_id"] + 1
        time.sleep(2)

if __name__ == '__main__':
    main()


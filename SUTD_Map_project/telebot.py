import os
import requests
import json
import time

import Path_query

class PathfindingWrapper:
    def __init__(self):
        # Initialize Query class for pathfinding logic
        self.query_processor = Path_query.Query()

    def process_pathfinding(self, start_location, end_location):
        """Process pathfinding between two locations."""
        # Translate start and end locations to internal vertices
        start_loc = self.query_processor.translatermIDtovert(start_location)
        end_loc = self.query_processor.translatermIDtovert(end_location)

        # Check if both locations are on the same map
        if self.query_processor.convertloc_todd(start_loc) == self.query_processor.convertloc_todd(end_loc):
            # Use Dijkstra's algorithm to find the shortest path
            result = self.query_processor.dijkstra(start_loc)
            path = result[end_loc][1]
            distance = result[end_loc][0]
            return f"Shortest path: {path}\nDistance to end point: {distance}"
        else:
            # Implement cross-map pathfinding if necessary
            return "Cross-map pathfinding is not yet supported."


# Define conversation states
STATE_WAITING_FOR_START = "waiting_for_start"
STATE_WAITING_FOR_END = "waiting_for_end"
STATE_IDLE = "idle"

# Dictionary to store user states and temporary data (start/end locations)
user_states = {}
user_data = {}

# Wrapper class for pathfinding
pathfinding_wrapper = PathfindingWrapper()

# Load environment variables
def load_env(fpath):
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

load_env('.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Function to get updates from Telegram
def get_updates(offset=None):
    url = f'{BASE_URL}/getUpdates'
    params = {"timeout": 60, "offset": offset}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting updates: {e}")
        return None

# Function to send a message via Telegram
def send_message(chat_id, text, reply_markup=None):
    url = f'{BASE_URL}/sendMessage'
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"Sent message to chat {chat_id}: {text}")
    except requests.RequestException as e:
        print(f"Error sending message: {e}")

# Function to display the main menu with inline buttons
def main_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Pathfinding", "callback_data": "pathfinding"}
            ]
        ]
    }
    send_message(chat_id, "Choose an option:", reply_markup=keyboard)

# Function to handle callback query data
def handle_callback_query(callback_query):
    chat_id = callback_query['message']['chat']['id']
    callback_data = callback_query['data']

    if callback_data == "pathfinding":
        send_message(chat_id, "Please enter the start location:")
        user_states[chat_id] = STATE_WAITING_FOR_START

# Function to handle user input and transition between states
def handle_user_input(chat_id, text):
    current_state = user_states.get(chat_id, STATE_IDLE)

    if current_state == STATE_WAITING_FOR_START:
        user_data[chat_id] = {'start_location': text}
        send_message(chat_id, "Please enter the end location:")
        user_states[chat_id] = STATE_WAITING_FOR_END

    elif current_state == STATE_WAITING_FOR_END:
        start_location = user_data[chat_id]['start_location']
        end_location = text
        result = pathfinding_wrapper.process_pathfinding(start_location, end_location)
        send_message(chat_id, result)
        user_states[chat_id] = STATE_IDLE  # Reset state after processing

    else:
        main_menu(chat_id)  # Show the main menu if idle

# Function to process updates and route messages to appropriate handlers
def process_updates():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates and updates.get("ok") and len(updates.get("result", [])) > 0:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                callback_query = update.get("callback_query")
                message = update.get("message")

                if callback_query:
                    handle_callback_query(callback_query)
                elif message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")

                    if text.lower() == "/start":
                        main_menu(chat_id)
                    else:
                        handle_user_input(chat_id, text)
        time.sleep(2)

# Main function to start the bot
if __name__ == '__main__':
    print("Starting bot...")
    process_updates()

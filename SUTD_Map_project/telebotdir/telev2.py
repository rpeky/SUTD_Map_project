import httplib2 as http
import json
import os
from urllib.parse import urlparse
import requests
import time

# Define conversation states
STATE_WAITING_FOR_START = "waiting_for_start"
STATE_WAITING_FOR_END = "waiting_for_end"
STATE_IDLE = "idle"

# Dictionary to store user states
user_states = {}

def load_env(fpath):
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value
load_env('.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Function to get updates from the Telegram bot
def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    if offset:
        url += f'?offset={offset}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting updates: {e}")
        return None
    return data
    
# Function to get the chat ID from the latest update
def get_chatid(jsdata):
    if jsdata and jsdata.get("ok") and len(jsdata.get("result", [])) > 0:
        last_message = jsdata["result"][-1].get("message")
        if last_message:
            chat_id = last_message["chat"]["id"]
            print("Chat ID:", chat_id)
            return str(chat_id)
    print("No new messages or invalid data format.")
    return None

# Function to send a message via the Telegram bot
def send_tele_message(chatid, msg, reply_markup=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chatid, 'text': msg}
    
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

    return response.json()

def handle_callback_query(callback_query):
    chat_id = callback_query['message']['chat']['id']
    callback_data = callback_query['data']

    if callback_data == "location_explorer":
        send_tele_message(chat_id, "Please provide a location name or ID:")
        # Fetch and display location details based on the input
    elif callback_data == "pathfinding":
        send_tele_message(chat_id, "Please enter the start location:")
        start_location = wait_for_next_message(chat_id)  # Wait for user input
        send_tele_message(chat_id, "Please enter the end location:")
        end_location = wait_for_next_message(chat_id)
        # Call pathquery.py to get the route and return to the user
        route = get_route(start_location, end_location)
        send_tele_message(chat_id, f"Your route is: {route}")

def main_menu_loadout(chatid):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Location Explorer", "callback_data": "location_explorer"},
                {"text": "Pathfinding", "callback_data": "pathfinding"}
            ]
        ]
    }
    send_tele_message(chat_id, "Choose an option:", reply_markup=keyboard)

def wait_for_next_message(chat_id, timeout=60):
    """
    Polls Telegram for the next message from the specified chat ID.
    Returns the text of the next message or None if no message arrives within the timeout.
    """
    start_time = time.time()
    offset = None  # Track the latest update to prevent duplicates

    while time.time() - start_time < timeout:
        updates = get_updates(offset)

        if updates["ok"] and len(updates["result"]) > 0:
            for update in updates["result"]:
                message = update.get("message")
                if message and message["chat"]["id"] == chat_id:
                    return message.get("text", "")
                offset = update["update_id"] + 1

        time.sleep(2)  # Poll every 2 seconds

    return None


# Function to handle user state
def handle_user_input(chat_id, text):
    # Check the user's current state
    current_state = user_states.get(chat_id, STATE_IDLE)

    if current_state == STATE_IDLE:
        if text.lower() == "pathfinding":
            send_tele_message(chat_id, "Please enter the start location:")
            user_states[chat_id] = STATE_WAITING_FOR_START  # Update state
        elif text.lower() == "location explorer":
            send_tele_message(chat_id, "Please provide a location name or ID:")
            # Here, you can add logic for handling location explorer
        else:
            send_tele_message(chat_id, "Unknown command. Type 'Pathfinding' or 'Location Explorer'.")
    
    elif current_state == STATE_WAITING_FOR_START:
        send_tele_message(chat_id, "Please enter the end location:")
        user_states[chat_id] = STATE_WAITING_FOR_END  # Move to the next state
    
    elif current_state == STATE_WAITING_FOR_END:
        # Here, you'd process the start and end locations and compute the route
        send_tele_message(chat_id, f"Calculating route from start to {text}.")
        # After processing, reset the user's state
        user_states[chat_id] = STATE_IDLE

# Main function with continuous polling
def main():
    offset = None

    while True:
        # Fetch updates from Telegram
        updates = get_updates(offset)

        if updates and updates.get("ok") and len(updates.get("result", [])) > 0:
            for update in updates["result"]:
                message = update.get("message")
                if message:
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "")

                    # Handle user input based on their state
                    handle_user_input(chat_id, text)

                    # Update the offset to avoid processing the same message again
                    offset = update["update_id"] + 1

        time.sleep(2)

if __name__ == '__main__':
    main()

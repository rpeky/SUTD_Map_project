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

# Function to handle callback queries
def handle_callback_query(callback_query):
    chat_id = callback_query['message']['chat']['id']
    callback_data = callback_query['data']

    if callback_data == "location_explorer":
        send_tele_message(chat_id, "Please provide a location name or ID:")
        # Handle location explorer logic here
    elif callback_data == "pathfinding":
        send_tele_message(chat_id, "Please enter the start location:")
        user_states[chat_id] = STATE_WAITING_FOR_START  # Set state for pathfinding

# Function to display the main menu with inline buttons
def main_menu(chat_id):
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

# Function to handle user input based on their state
def handle_user_input(chat_id, text):
    # Check the user's current state
    current_state = user_states.get(chat_id, STATE_IDLE)

    if current_state == STATE_WAITING_FOR_START:
        send_tele_message(chat_id, "Please enter the end location:")
        user_states[chat_id] = STATE_WAITING_FOR_END  # Move to the next state
    
    elif current_state == STATE_WAITING_FOR_END:
        # Here, you'd process the start and end locations and compute the route
        send_tele_message(chat_id, f"Calculating route to {text}.")
        user_states[chat_id] = STATE_IDLE  # Reset state after processing
    
    else:
        # If idle, show the main menu
        main_menu(chat_id)

# Main function with continuous polling
def main():
    offset = None

    while True:
        # Fetch updates from Telegram
        updates = get_updates(offset)

        if updates and updates.get("ok") and len(updates.get("result", [])) > 0:
            for update in updates["result"]:
                callback_query = update.get("callback_query")
                message = update.get("message")

                if callback_query:
                    # Handle button presses (callback queries)
                    handle_callback_query(callback_query)

                elif message:
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "")

                    # Handle user input (text messages)
                    handle_user_input(chat_id, text)

                    # Update the offset to avoid processing the same message again
                    offset = update["update_id"] + 1

        time.sleep(2)

if __name__ == '__main__':
    main()

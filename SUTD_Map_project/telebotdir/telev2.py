import httplib2 as http
import json
import os
from urllib.parse import urlparse
import requests
import time
#Using telegram API not local host

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Function to get updates from the Telegram bot
def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    # If offset is provided, add it to the request URL to get new updates only
    if offset:
        url += f'?offset={offset}'

    response = requests.get(url)
    data = response.json()
    print(data)
    return data

# Function to get the chat ID from the latest update
def get_chatid(jsdata):
    if jsdata["ok"] and len(jsdata["result"]) > 0:
        # Get the last message's chat ID
        chat_id = jsdata["result"][-1]["message"]["chat"]["id"]
        print("Chat ID:", chat_id)
        return str(chat_id)
    else:
        print("No new messages")
        return None

# Function to send a message via the Telegram bot
def send_tele_message(chatid, msg, reply_markup=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    
    # Prepare the payload with chat ID and message
    payload = {
        'chat_id': chatid,
        'text': msg
    }
    
    # If reply_markup is provided, add it to the payload
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)

    # Make the request
    response = requests.post(url, data=payload)
    
    # Print and return the response content
    print("Response:", response.content)
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

# Main function with continuous polling
def main():
    # Initialize offset to keep track of the last message processed
    offset = None

    print("Bot is running and waiting for user replies...")

    while True:
        # Fetch updates from Telegram
        updates = get_updates(offset)

        if updates["ok"] and len(updates["result"]) > 0:
            for update in updates["result"]:
                # Extract chat ID and message text
                message = update.get("message")
                if message:
                    chat_id = str(message["chat"]["id"])
                    text = message.get("text", "")

                    print(f"User said: {text}")
                    # Respond to the user
                    reply_message = f"You said: {text}"
                    send_tele_message(chat_id, reply_message)

                    # Update the offset to avoid processing the same message again
                    offset = update["update_id"] + 1

        # Wait for 3 seconds before checking again
        time.sleep(2)

if __name__ == '__main__':
    main()

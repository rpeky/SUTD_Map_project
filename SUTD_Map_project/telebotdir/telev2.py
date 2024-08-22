import httplib2 as http
import json
import os
from urllib.parse import urlparse
import requests
import time
#Using telegram API not local host

#All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: https://api.telegram.org/bot<token>/METHOD_NAME
#token = '7338576036:AAEpgpNoLoja05lQyvx7R3WgEBk5Bzgvy5Y' 
#req = 'https://api.telegram.org/bot7338576036:AAEpgpNoLoja05lQyvx7R3WgEBk5Bzgvy5Y/'

# Function to get updates from the Telegram bot
def get_updates(offset=None):
    url = 'https://api.telegram.org/bot7338576036:AAEpgpNoLoja05lQyvx7R3WgEBk5Bzgvy5Y/getUpdates'
    
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
def send_tele_message(chatid, msg):
    url = 'https://api.telegram.org/bot7338576036:AAEpgpNoLoja05lQyvx7R3WgEBk5Bzgvy5Y/sendMessage'
    target = urlparse(url + '?chat_id=' + chatid + '&text=' + msg)

    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers={}
            )

    print("Response: ", content)
    jsobj = json.loads(content)
    return jsobj

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
        time.sleep(3)

if __name__ == '__main__':
    main()

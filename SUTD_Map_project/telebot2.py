import os

# Pathfinding libraries
import Path_query

# Telegram Bot library stuff
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

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
            # Strip apostrophes and whitespaces
            value = value.strip(r" '")
            os.environ[key] = value

# Change this path to where you have placed your .env file with the telebot token
ENV_DIR = os.getcwd()
load_env(os.path.join(ENV_DIR, 'env'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = "Welcome to the SUTD Mapping Project Bot. Please select an option"
    start_options = ["Pathfinding", "Option 2"]
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in start_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(start_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("TODO: help command list")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("TODO: all the custom commands")

# Message handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.from_user.id
    text = update.message.text
    user_state = user_states.get(chat_id, STATE_IDLE)
    print(user_state)
    reply_text = None
    if user_state == STATE_WAITING_FOR_START:
        user_data[chat_id] = {'start_location': text}
        user_states[chat_id] = STATE_WAITING_FOR_END
        reply_text = "Please enter the end location:"
    elif user_state == STATE_WAITING_FOR_END:
        start_location = user_data[chat_id]['start_location']
        end_location = text
        user_states[chat_id] = STATE_IDLE
        try:
            reply_text = pathfinding_wrapper.process_pathfinding(start_location, end_location)
        except:
            reply_text = "Error in pathfinding process"
    else:
        reply_text = None
    await update.message.reply_text(reply_text)

# Callback query handlers
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selection = query.data
    if selection == "Pathfinding":
        user_states[query.from_user.id] = STATE_WAITING_FOR_START
        await query.from_user.send_message(text="Please enter the start location:")
    else:
        pass
    await query.answer()

# Error handlers
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Command Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Callback Query Handlers
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Error Handlers
    app.add_error_handler(handle_error)

    # Run the bot, i.e. get it to start polling
    print("Polling ...")
    app.run_polling(poll_interval=3)


# Main function to start the bot
if __name__ == '__main__':
    main()


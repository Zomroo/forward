from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time

# Enter your API ID and API hash here
api_id = 16844842
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"

# Enter your bot token here
bot_token = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"

app = Client("my_bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    client.send_message(message.chat.id, "Hi, I am a message forwarder bot! To forward messages from channel A to channel B, please use the command /fr.")

# Forward command
@app.on_message(filters.command("fr"))
def forward_command(client, message):
    client.send_message(message.chat.id, "Please provide the starting and ending message links in channel A, separated by a space.")
    client.register_callback_query_handler(forward_messages_callback, message.chat.id, timeout=30)

# Forward messages callback function
def forward_messages_callback(client, callback_query):
    try:
        # Extract starting and ending message links
        start_link, end_link = callback_query.data.split()

        # Get the chat IDs of channels A and B
        chat_a_id = -1001668076927 # Replace with the chat ID of channel A
        chat_b_id = -1001713208670 # Replace with the chat ID of channel B

        # Check if bot is a member of channels A and B
        chat_a_member = client.get_chat_member(chat_id=chat_a_id, user_id=app.get_me().id)
        chat_b_member = client.get_chat_member(chat_id=chat_b_id, user_id=app.get_me().id)
        if chat_a_member.status != "member" or chat_b_member.status != "member":
            raise Exception("Bot is not a member of one or both of the channels.")

        # Forward messages from channel A to channel B
        msg_count = 0
        for message in client.iter_history(chat_a_id, offset_date=0, offset_id=int(start_link[1:]), reverse=True):
            if message.link in (start_link, end_link):
                client.send_message(chat_b_id, message)
                msg_count += 1
                if msg_count == 200:
                    time.sleep(300) # Wait for 5 minutes
                    msg_count = 0

        # Notify the user when the forwarding is done
        client.send_message(callback_query.message.chat.id, "Message forwarding is complete!")

    except Exception as e:
        print(str(e))
        client.send_message(callback_query.message.chat.id, "An error occurred while forwarding messages. Please try again.")

# Run the bot
app.run()

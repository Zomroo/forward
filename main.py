import pyrogram
from pyrogram import filters

api_id = 16844842 # Replace with your Telegram API ID
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4" # Replace with your Telegram API hash
bot_token = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4" # Replace with your bot token

app = pyrogram.Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Add your source and destination chat IDs here
source_chat_id = -1001668076927
destination_chat_id = -1001713208670

# Forward the message from source chat
@app.on_message(filters.command("forward"))
def forward_message(client, message):
    client.send_message(chat_id=message.chat.id, text="Please forward the message from the group you want to forward.")

    # Wait for the user to forward the message and get the message ID
    @app.on_message(filters.forwarded & filters.private & filters.from_chat(source_chat_id))
    def forward_first_message(client, message):
        first_message_id = message.message_id
        client.send_message(chat_id=message.chat.id, text="Please forward the last message you want to forward.")

        # Wait for the user to forward the last message and get the message ID
        @app.on_message(filters.forwarded & filters.private & filters.from_chat(source_chat_id))
        def forward_last_message(client, message):
            last_message_id = message.message_id
            client.send_message(chat_id=message.chat.id, text="Forwarding messages...")

            # Forward all the messages from the first forwarded message to the last forwarded message
            with app:
                messages = client.get_messages(source_chat_id, offset_id=last_message_id, limit=last_message_id - first_message_id + 1)
                for message in reversed(messages):
                    client.send_message(chat_id=destination_chat_id, text=message.text)

    # Stop listening for messages after the first message has been forwarded
    app.stop()

# Start the bot
@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I am a bot that can forward messages from one group to another. To use me, just send /forward command and follow the instructions.")

app.run()

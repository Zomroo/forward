import pyrogram
from pyrogram import Client, filters

api_id = 16844842 # Replace with your Telegram API ID
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4" # Replace with your Telegram API hash
bot_token = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4" # Replace with your bot token

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.command("start"))
def start_command(client, message):
    client.send_message(message.chat.id, "Hello! Send me a message to forward to the database channel.")

@app.on_message(filters.private)
def forward_to_channel(client, message):
    # Replace 'database_channel' with the username or ID of the channel where you want to forward the messages
    client.forward_messages('-1001713208670', message.chat.id, message.message_id, as_copy=True)

app.run()

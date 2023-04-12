from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

api_id = 16844842 # Replace with your Telegram API ID
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4" # Replace with your Telegram API hash
bot_token = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4" # Replace with your bot token

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Define the group IDs
source_group_id = -1001668076927  # replace with the source group ID
destination_group_id = -1001713208670  # replace with the destination group ID

# Define the start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Hello! I'm a bot to forward messages from one group to another group or channel.")

# Define the forward command
@app.on_message(filters.command("forward"))
def forward_command(client, message):
    # Ask for the first message link
    message.reply_text("Please send me the link of the first message you want to forward.")

    # Define a filter to get the first message link
    @app.on_message(filters.text & filters.private & filters.user(message.from_user.id))
    def get_first_message_link(client, message):
        first_message_link = message.text

        # Ask for the last message link
        message.reply_text("Please send me the link of the last message you want to forward.")

        # Define a filter to get the last message link
        @app.on_message(filters.text & filters.private & filters.user(message.from_user.id))
        def get_last_message_link(client, message):
            last_message_link = message.text

            # Get the first and last message IDs
            try:
                first_message_id = client.get_messages(source_group_id, search=first_message_link).id
                last_message_id = client.get_messages(source_group_id, search=last_message_link).id
            except BadRequest:
                message.reply_text("Invalid message link. Please try again.")
                return

            # Forward the messages
            try:
                messages = client.get_messages(source_group_id, offset_id=first_message_id-1, limit=last_message_id-first_message_id+1)
                for message in messages:
                    client.send_message(destination_group_id, text=message.text)
            except BadRequest:
                message.reply_text("Error forwarding messages. Please try again.")

            # Remove the filters
            app.remove_handler(get_first_message_link)
            app.remove_handler(get_last_message_link)

            # Remove the last message handler
            app.remove_handler(get_last_message_link)

        # Add the filter
        app.add_handler(get_last_message_link)

    # Add the filter
    app.add_handler(get_first_message_link)

# Start the bot
app.run()

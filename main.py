import os
import time
from pyrogram import Client, filters

# Replace with your own values
API_ID = 16844842
API_HASH = 'f6b0ceec5535804be7a56ac71d08a5d4'
BOT_TOKEN = '5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4'

app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Define the start command
@app.on_message(filters.command('start'))
def start_command(client, message):
    client.send_message(message.chat.id, 'Hello! I am your forwarder bot. Use /fr to forward messages.')

# Define the forward command
@app.on_message(filters.command('fr'))
def forward_command(client, message):
    # Check if the bot is in both channels
    channel_a_id = -1001668076927
    channel_b_id = -1001713208670
    if not (client.get_chat_member(channel_a_id, 'me').status == 'member' and 
            client.get_chat_member(channel_b_id, 'me').status == 'member'):
        client.send_message(message.chat.id, 'Please add me to both channels.')
        return

    # Ask for the starting and ending message links
    client.send_message(message.chat.id, 'Please provide the starting and ending message links.')
    starting_link = None
    ending_link = None

    # Wait for the starting and ending links
    while True:
        reply = client.listen(filters.private & filters.regex(r'https://t.me/c/\d+/\d+'))
        link = reply.text
        if not starting_link:
            starting_link = link
            client.send_message(message.chat.id, 'Got it. Now please provide the ending message link.')
        else:
            ending_link = link
            break

    # Get the messages between the starting and ending links
    messages = []
    for message_link in client.iter_history(channel_a_id, offset_date=0):
        if message_link.link == starting_link:
            break
        elif message_link.link == ending_link:
            messages.reverse()
            break
        else:
            messages.append(message_link)

    # Forward the messages to channel B, with a 5-minute delay every 200 messages
    for i, message in enumerate(messages):
        client.forward_messages(channel_b_id, message.chat.id, message.message_id)
        if (i + 1) % 200 == 0:
            time.sleep(300)

    client.send_message(message.chat.id, 'All done! The messages have been forwarded to channel B.')

# Start the client
app.run()

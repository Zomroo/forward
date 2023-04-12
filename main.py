from pyrogram import Client, filters
from pyrogram.types import Message
import time

# Replace with your own values
API_ID = 16844842
API_HASH = 'f6b0ceec5535804be7a56ac71d08a5d4'
BOT_TOKEN = '5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4'
CHANNEL_A_ID = -1001668076927
CHANNEL_B_ID = -1001713208670


app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start command handler
@app.on_message(filters.command('start'))
async def start_handler(client, message):
    await message.reply_text('Hello! Send /fr to start forwarding messages.')


# Forward command handler
@app.on_message(filters.command('fr'))
async def forward_handler(client, message):
    # Check if the user is authorized to use the bot
    if message.chat.id not in [CHANNEL_A_ID, CHANNEL_B_ID]:
        await message.reply_text('You are not authorized to use this bot.')
        return

    # Ask for the starting and ending message links
    await message.reply_text('Please send the starting message link.')
    starting_link_message = await app.listen(filters.text & filters.chat(message.chat.id))

    await message.reply_text('Please send the ending message link.')
    ending_link_message = await app.listen(filters.text & filters.chat(message.chat.id))

    # Get the message IDs from the links
    starting_message_id = int(starting_link_message.text.split('/')[-1])
    ending_message_id = int(ending_link_message.text.split('/')[-1])

    # Determine the direction of the forwarding
    if message.chat.id == CHANNEL_A_ID:
        source_channel_id = CHANNEL_A_ID
        target_channel_id = CHANNEL_B_ID
    else:
        source_channel_id = CHANNEL_B_ID
        target_channel_id = CHANNEL_A_ID

    # Forward messages
    for message_id in range(starting_message_id, ending_message_id + 1):
        message = await client.get_messages(source_channel_id, message_id)
        await client.send_message(target_channel_id, message)

        # Take a break every 200 messages
        if message_id % 200 == 0:
            time.sleep(300)  # 5 minutes


app.run()

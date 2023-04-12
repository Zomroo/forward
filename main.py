import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.types import Message

import time

# Replace these placeholders with your own values
API_ID = 16844842
API_HASH = "f6b0ceec5535804be7a56ac71d08a5d4"
BOT_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("Hi! I am a Telegram bot programmed to forward messages from Channel A to Channel B. To get started, use the /fr command.")

@Client.on_message(filters.command("fr"))
async def forward_messages(client, message):
    # Check if the user is an admin in both channels
    try:
        admin_A = await client.get_chat_member(chat_id="-1001668076927", user_id=message.from_user.id)
        admin_B = await client.get_chat_member(chat_id="-1001713208670", user_id=message.from_user.id)
        if not (admin_A.status in ("creator", "administrator") and admin_B.status in ("creator", "administrator")):
            await message.reply("Sorry, you need to be an admin in both channels to use this command.")
            return
    except ChatAdminRequired:
        await message.reply("Sorry, I need to be an admin in both channels to use this command.")
        return
    
    # Ask for the starting and ending message links
    await message.reply("Please provide me the link of the starting message in Channel A.")
    start_link = (await app.listen(message.chat.id)).text
    await message.reply("Please provide me the link of the last message in Channel A where I am added.")
    end_link = (await app.listen(message.chat.id)).text
    
    # Get the message IDs of the starting and ending messages
    start_msg_id = int(start_link.split("/")[-1])
    end_msg_id = int(end_link.split("/")[-1])
    
    # Forward the messages in batches of 200 with a 5-minute break after each batch
    for i in range(start_msg_id, end_msg_id+1):
        try:
            message = await client.get_messages(chat_id="-1001668076927", message_ids=i)
            await client.send_message(chat_id="-1001713208670", text=message.text)
        except Exception as e:
            print(e)
        
        if i % 200 == 0:
            time.sleep(300)
    
    await message.reply("Messages forwarded successfully.")

app.run()

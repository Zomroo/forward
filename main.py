import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# insert your Telegram bot token here
BOT_TOKEN = '5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4'

# insert the ID of the channel you want to send messages to
CHANNEL_ID = '-1001713208670'

# function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I'm a bot that can forward your messages to a specified channel. Use the /sendmsg command to send a message.")

# function to handle the /sendmsg command
def sendmsg(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please enter the message you want to send to the channel.")
    # set a "waiting_for_message" flag to indicate that the bot is waiting for a message
    context.user_data['waiting_for_message'] = True

# function to handle incoming messages
def handle_message(update, context):
    # check if the bot is waiting for a message
    if context.user_data.get('waiting_for_message', False):
        # check if the message being forwarded has any attachments
        if update.message.effective_attachment:
            # loop through all attachments and forward each one to the specified channel
            for attachment in update.message.effective_attachment:
                if isinstance(attachment, telegram.Video):
                    context.bot.send_video(chat_id=CHANNEL_ID,
                                           video=attachment.file_id,
                                           caption=update.message.caption)
                elif isinstance(attachment, telegram.PhotoSize):
                    context.bot.send_photo(chat_id=CHANNEL_ID,
                                            photo=attachment.file_id,
                                            caption=update.message.caption)
                elif isinstance(attachment, telegram.Document):
                    context.bot.send_document(chat_id=CHANNEL_ID,
                                               document=attachment.file_id,
                                               caption=update.message.caption)
        else:
            # forward the text message to the specified channel
            context.bot.send_message(chat_id=CHANNEL_ID,
                                      text=update.message.text)
        # reset the "waiting_for_message" flag
        context.user_data['waiting_for_message'] = False
        # confirm to the user that the message was sent
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Message sent!")
    else:
        # if the bot is not waiting for a message, ignore the incoming message
        pass



def main():
    # create a new bot object using the token
    bot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add command handlers for /start and /sendmsg
    start_handler = CommandHandler('start', start)
    sendmsg_handler = CommandHandler('sendmsg', sendmsg)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(sendmsg_handler)

    # add a message handler to handle incoming messages
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)

    # start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

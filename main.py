import telegram
import telegram.ext
import time

# Telegram API token
token = '5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4'

# Initialize bot
bot = telegram.Bot(token=token)

# Channel IDs
channel_a_id = -1001668076927
channel_b_id = -1001713208670

# Start command
def start(update, context):
    update.message.reply_text('Welcome to the message forwarding bot!')
    context.user_data['start_link'] = False
    context.user_data['end_link'] = False


# Forward command
def forward(update, context):
    # Check if bot is in channel A
    if not bot.get_chat_member(chat_id=channel_a_id, user_id=bot.id).status == 'member':
        update.message.reply_text('Please add the bot to the source channel first.')
        return
    # Check if bot is in channel B
    if not bot.get_chat_member(chat_id=channel_b_id, user_id=bot.id).status == 'member':
        update.message.reply_text('Please add the bot to the destination channel first.')
        return
    # Get starting and ending message links
    update.message.reply_text('Please provide the starting and ending message links.')
    context.user_data['start_link'] = True
    context.user_data['end_link'] = False

# Message handler
def message(update, context):
    # Check if user is providing a link
    if context.user_data.get('start_link', False):
        context.user_data['start_link'] = False
        context.user_data['end_link'] = True
        context.user_data['start_message_id'] = int(update.message.text.split('/')[-1])
        update.message.reply_text('Please provide the ending message link.')
    elif context.user_data.get('end_link', False):
        context.user_data['end_link'] = False
        context.user_data['end_message_id'] = int(update.message.text.split('/')[-1])
        update.message.reply_text('Starting message ID: {}\nEnding message ID: {}'.format(
            context.user_data['start_message_id'],
            context.user_data['end_message_id']
        ))
        # Forward messages
        count = 0
        for message in bot.iter_history(channel_a_id):
            if message.message_id == context.user_data['start_message_id']:
                # Start forwarding
                update.message.reply_text('Started forwarding messages...')
                while message.message_id <= context.user_data['end_message_id']:
                    # Forward message
                    bot.forward_message(chat_id=channel_b_id, from_chat_id=channel_a_id, message_id=message.message_id)
                    count += 1
                    # Check if break is needed
                    if count % 200 == 0:
                        update.message.reply_text('Forwarded {} messages. Taking a 5-minute break...'.format(count))
                        time.sleep(300)
                    # Get next message
                    message = bot.get_messages(chat_id=channel_a_id, message_ids=message.message_id + 1)
                # End forwarding
                update.message.reply_text('Finished forwarding messages. Total messages forwarded: {}.'.format(count))
                break

# Main function
def main():
    # Create updater and dispatcher
    updater = telegram.ext.Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.CommandHandler('forward', forward))
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, message))

    # Start polling
    updater.start_polling()

    # Run until interrupted
    updater.idle()

if __name__ == '__main__':
    main()

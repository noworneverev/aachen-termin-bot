from telegram.ext import CommandHandler, Updater
from telegram import ParseMode
from typing import Final
import os
from termin import aachen_termin
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
# BOT_USERNAME: Final = '@aachen_termin_bot'
CHANNEL_ID: Final = '@aachen_termin'
URL: Final = 'https://aachen-termin-bot.onrender.com'

def start_command(update, context):
    update.message.reply_text("Hello! Welcome to Aachen Termin Bot! Join the channel @aachen_termin to get notified when appointment is available!", parse_mode = ParseMode.HTML)

def termin_command(update, context):
    if aachen_termin():
        update.message.reply_text('Appointment available now!')
    else:
        update.message.reply_text('No appointment available')

def termin_cron(context):
    if aachen_termin():
        context.bot.send_message(chat_id=CHANNEL_ID,text=f'{"Appointment available now!"}')

if __name__ == '__main__':    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue
    job_queue.run_repeating(termin_cron,interval=30.0,first=0.0)
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('termin', termin_command))
    updater.start_polling()
    updater.idle()    
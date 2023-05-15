from typing import Final
import requests
import logging
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv
import os
from flask import Flask

app = Flask(__name__)

load_dotenv()

TOKEN = os.getenv("TOKEN")
# BOT_USERNAME: Final = '@aachen_termin_bot'
CHANNEL_ID: Final = '@aachen_termin'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def aachen_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    
    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/'
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_3 = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?mdt=52&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=0&cnc-202=0&cnc-189=0&cnc-203=0&cnc-196=0&cnc-200=0&cnc-199=0&cnc-188=0&cnc-186=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-185=0&cnc-187=0&cnc-190=0&cnc-195=0&cnc-191=1&cnc-194=0&cnc-197=0&cnc-192=0"
    url_4 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-191=1&loc=28'

    res_1 = requests.get(url_1, headers=headers)
    res_2 = requests.get(url_2, headers=headers,cookies=res_1.cookies)
    res_3 = requests.get(url_3, headers=headers,cookies=res_2.cookies)
    res_4 = requests.get(url_4, headers=headers,cookies=res_3.cookies)
    
    if "Kein freier Termin verfügbar" not in res_4.text:
        logging.info(f'{"Appointment available now!"}')
        return True
    else:
        logging.info(f'{"No appointment available"}')  
        return False

def start_command(update, context):
    update.message.reply_text('Hello! Welcome to Aachen Termin Bot!')

def termin_command(update, context):
    if aachen_termin():
        update.message.reply_text('Appointment available now!')
    else:
        update.message.reply_text('No appointment available')

def termin_cron(context):
    if aachen_termin():
        context.bot.send_message(chat_id=CHANNEL_ID,text=f'{"Appointment available now!"}')

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue
    job_queue.run_repeating(termin_cron,interval=30.0,first=0.0)
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('termin', termin_command))
    updater.start_polling()
    updater.idle()

@app.route('/')
def hello_world():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue
    job_queue.run_repeating(termin_cron,interval=30.0,first=0.0)
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('termin', termin_command))
    updater.start_polling()
    updater.idle()
    return 'Hello, World!'

# if __name__ == '__main__':
    # updater = Updater(TOKEN, use_context=True)
    # dp = updater.dispatcher
    # job_queue = updater.job_queue
    # job_queue.run_repeating(termin_cron,interval=30.0,first=0.0)
    # dp.add_handler(CommandHandler('start', start_command))
    # dp.add_handler(CommandHandler('termin', termin_command))
    # updater.start_polling()
    # updater.idle()
    # app.run()
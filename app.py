from typing import Final
import requests
import telegram
from dotenv import load_dotenv
import os
from flask import Flask
from flask_apscheduler import APScheduler
from termin import aachen_termin

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

load_dotenv()

TOKEN = os.getenv("TOKEN")
# BOT_USERNAME: Final = '@aachen_termin_bot'
CHANNEL_ID: Final = '@aachen_termin'
URL: Final = 'https://aachen-termin-bot.onrender.com'


@app.route('/status')
def status():    
    return 'OK'

@app.route('/')
def hello_world():    
    return 'Hello, World!'

@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def job1():    
    bot = telegram.Bot(token=TOKEN)
    if aachen_termin():
        bot.send_message(chat_id=CHANNEL_ID, text='Appointment available now!')  

@scheduler.task('interval', id='do_job_2', seconds=300, misfire_grace_time=900)
def job2():
    r = requests.get(f'{URL}/status')
    print(r)

@scheduler.task('cron', id='do_job_3', day='*')
def job3():
    r = requests.get(URL)
    print(r)
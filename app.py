from typing import Final
import requests
import telegram
from dotenv import load_dotenv
import os
from flask import Flask
from flask_apscheduler import APScheduler
from termin import aachen_termin, aachen_an, Location
from utils import get_next_months

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

# https://serviceportal.aachen.de/suche/-/vr-bis-detail/dienstleistung/5790/show

KATSCHHOF_CHANNEL_ID_01: Final = '@'
KATSCHHOF_CHANNEL_ID_02: Final = '@'
KATSCHHOF_CHANNEL_ID_03: Final = '@'
KATSCHHOF_CHANNEL_ID_04: Final = '@'
KATSCHHOF_CHANNEL_ID_05: Final = '@'
KATSCHHOF_CHANNEL_ID_06: Final = '@'
KATSCHHOF_CHANNEL_ID_07: Final = '@'
KATSCHHOF_CHANNEL_ID_08: Final = '@'
KATSCHHOF_CHANNEL_ID_09: Final = '@kattermin09'
KATSCHHOF_CHANNEL_ID_10: Final = '@kattermin10'
KATSCHHOF_CHANNEL_ID_11: Final = '@kattermin11'
KATSCHHOF_CHANNEL_ID_12: Final = '@kattermin12'

BAHNHOFPLATZ_CHANNEL_ID_01: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_02: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_03: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_04: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_05: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_06: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_07: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_08: Final = '@'
BAHNHOFPLATZ_CHANNEL_ID_09: Final = '@bahtermin09'
BAHNHOFPLATZ_CHANNEL_ID_10: Final = '@bahtermin10'
BAHNHOFPLATZ_CHANNEL_ID_11: Final = '@bahtermin11'
BAHNHOFPLATZ_CHANNEL_ID_12: Final = '@bahtermin12'

@app.route('/status')
def status():    
    return 'OK'

@app.route('/')
def hello_world():    
    return 'Hello, World!'

@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def job1():    
    bot = telegram.Bot(token=TOKEN)
    notify_aachen_termin(bot)
    notify_aachen_anmeldung(bot)
    

def notify_aachen_termin(bot: telegram.Bot):
    is_available, res = aachen_termin()
    if is_available:
        bot.send_message(chat_id=CHANNEL_ID, text=res)  

def notify_aachen_anmeldung(bot: telegram.Bot):
    next_months, next_years = get_next_months(4)
    for month, year in zip(next_months, next_years):
        notify_anmeldung_by_month_and_location(bot, year, month, Location.Katschhof)
        notify_anmeldung_by_month_and_location(bot, year, month, Location.Bahnhofplatz)

def notify_anmeldung_by_month_and_location(bot: telegram.Bot, year: str, month: str, loc: Location):
    is_available, res = aachen_an(loc, year, month)
    if is_available:
        bot.send_message(chat_id=get_channel_id(loc, month), text=res)

def get_channel_id(loc: Location, month: str):
    month_dict = {}
    if loc == Location.Katschhof:
        month_dict = {
            "01": KATSCHHOF_CHANNEL_ID_01,
            "02": KATSCHHOF_CHANNEL_ID_02,
            "03": KATSCHHOF_CHANNEL_ID_03,
            "04": KATSCHHOF_CHANNEL_ID_04,
            "05": KATSCHHOF_CHANNEL_ID_05,
            "06": KATSCHHOF_CHANNEL_ID_06,
            "07": KATSCHHOF_CHANNEL_ID_07,
            "08": KATSCHHOF_CHANNEL_ID_08,
            "09": KATSCHHOF_CHANNEL_ID_09,
            "10": KATSCHHOF_CHANNEL_ID_10,
            "11": KATSCHHOF_CHANNEL_ID_11,
            "12": KATSCHHOF_CHANNEL_ID_12
        }
    elif loc == Location.Bahnhofplatz:
        month_dict = {
            "01": BAHNHOFPLATZ_CHANNEL_ID_01,
            "02": BAHNHOFPLATZ_CHANNEL_ID_02,
            "03": BAHNHOFPLATZ_CHANNEL_ID_03,
            "04": BAHNHOFPLATZ_CHANNEL_ID_04,
            "05": BAHNHOFPLATZ_CHANNEL_ID_05,
            "06": BAHNHOFPLATZ_CHANNEL_ID_06,
            "07": BAHNHOFPLATZ_CHANNEL_ID_07,
            "08": BAHNHOFPLATZ_CHANNEL_ID_08,
            "09": BAHNHOFPLATZ_CHANNEL_ID_09,
            "10": BAHNHOFPLATZ_CHANNEL_ID_10,
            "11": BAHNHOFPLATZ_CHANNEL_ID_11,
            "12": BAHNHOFPLATZ_CHANNEL_ID_12
        }
    
    return month_dict.get(month, CHANNEL_ID)


@scheduler.task('interval', id='do_job_2', seconds=300, misfire_grace_time=900)
def job2():
    r = requests.get(f'{URL}/status')
    print(r)
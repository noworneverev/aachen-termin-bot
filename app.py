from typing import Final
import requests
import telegram
from dotenv import load_dotenv
import os
from flask import Flask
from flask_apscheduler import APScheduler
from termin import superc_termin, aachen_hbf_termin, abholung_termin, fh_termin
from an import notify_aachen_anmeldung

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
HBF_CHANNEL_ID: Final = '@hbf_termin'
URL: Final = 'https://aachen-termin-bot.onrender.com'

ABHOLUNG_CHANNEL_ID: Final = '-1002267097890'
FH_AACHEN_CHANNEL_ID: Final = '-1002483658914'

APPOINTMENT_LINK = "https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1"

# HBF_URL = {
#     'Team 1': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=1&cnc-296=0&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0',
#     'Team 2': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=1&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0',
#     'Team 3': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=0&cnc-297=1&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0'
# }

@app.route('/status')
def status():    
    return 'OK'

@app.route('/')
def hello_world():    
    return 'Hello, World!'

@scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=900)
def job1():    
    bot = telegram.Bot(token=TOKEN)
    notify_aachen_termin(bot)
    notify_abholung(bot)
    # notify_aachen_anmeldung(bot)

def notify_abholung(bot: telegram.Bot):
    is_available, res = abholung_termin()
    if is_available:
        text = f"{res}\n[🔥 Book Now\!]({APPOINTMENT_LINK})"
        text = text.replace(".", "\.")
        bot.send_message(chat_id=ABHOLUNG_CHANNEL_ID, text=text, parse_mode='MarkdownV2')

def notify_aachen_termin(bot: telegram.Bot):

    # TODO ONE COULD POSSIBLY NOTIFY ABOUT OTHER APPOINTMENT TYPES
    # HOWEVER I AM NOT SURE IF THE SLOTS ARE SHARED BETWEEN TYPES
    # THIS SYSTEM HECKING SUCKS
    for pos in [0,1,2]:
        is_available, res = superc_termin(pos)
        if is_available:            
            text = f"{res}\n[🔥 Book Now\!]({APPOINTMENT_LINK})"
            text = text.replace(".", "\.")
            bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='MarkdownV2')
    
    for team in ['Team 1', 'Team 2', 'Team 3']:
        is_available, res = aachen_hbf_termin(team)
        if is_available:
            text = f"{res}\n[🔥 Book Now\!]({APPOINTMENT_LINK})"
            text = text.replace(".", "\.")
            bot.send_message(chat_id=HBF_CHANNEL_ID, text=text, parse_mode='MarkdownV2')
    
    
    is_available, res = fh_termin()
    if is_available:
        text = f"{res}\n[🔥 Check now]({APPOINTMENT_LINK})"
        text = text.replace(".", "\.")
        bot.send_message(chat_id=FH_AACHEN_CHANNEL_ID, text=text, parse_mode='MarkdownV2')

#  The site for Aachen Anmeldung is changed and the old method is not working
# def notify_aachen_anmeldung(bot: telegram.Bot):
#     next_months, next_years = get_next_months(4)
#     for month, year in zip(next_months, next_years):
#         notify_anmeldung_by_month_and_location(bot, year, month, Location.Katschhof)
#         notify_anmeldung_by_month_and_location(bot, year, month, Location.Bahnhofplatz)

# def notify_anmeldung_by_month_and_location(bot: telegram.Bot, year: str, month: str, loc: Location):
#     is_available, res = aachen_an(loc, year, month)
#     if is_available:
#         bot.send_message(chat_id=get_channel_id(loc, month), text=res)




@scheduler.task('interval', id='do_job_2', seconds=300, misfire_grace_time=900)
def job2():
    r = requests.get(f'{URL}/status')
    print(r)
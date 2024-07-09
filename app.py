from typing import Final
import requests
import telegram
from dotenv import load_dotenv
import os
from flask import Flask
from flask_apscheduler import APScheduler
from termin import superc_termin, aachen_an, Location, aachen_hbf_termin, driver_termin
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
HBF_CHANNEL_ID: Final = '@hbf_termin'
URL: Final = 'https://aachen-termin-bot.onrender.com'

# https://serviceportal.aachen.de/suche/-/vr-bis-detail/dienstleistung/5790/show

# KATSCHHOF_CHANNEL_ID_01: Final = '-1001917130132'
# KATSCHHOF_CHANNEL_ID_02: Final = '-1001929585127'
# KATSCHHOF_CHANNEL_ID_03: Final = '-1001916939289'
# KATSCHHOF_CHANNEL_ID_04: Final = '-1001947251124'
# KATSCHHOF_CHANNEL_ID_05: Final = '-1001956456096'
# KATSCHHOF_CHANNEL_ID_06: Final = '-1001933128610'
# KATSCHHOF_CHANNEL_ID_07: Final = '-1001917823310'
# KATSCHHOF_CHANNEL_ID_08: Final = '-1001926828618'
# KATSCHHOF_CHANNEL_ID_09: Final = '-1001979649417'
# KATSCHHOF_CHANNEL_ID_10: Final = '-1001714223745'
# KATSCHHOF_CHANNEL_ID_11: Final = '-1001920932827'
# KATSCHHOF_CHANNEL_ID_12: Final = '-1001910197421'

# BAHNHOFPLATZ_CHANNEL_ID_01: Final = '-1001843530956'
# BAHNHOFPLATZ_CHANNEL_ID_02: Final = '-1001835882216'
# BAHNHOFPLATZ_CHANNEL_ID_03: Final = '-1001924195962'
# BAHNHOFPLATZ_CHANNEL_ID_04: Final = '-1001937927958'
# BAHNHOFPLATZ_CHANNEL_ID_05: Final = '-1001669496886'
# BAHNHOFPLATZ_CHANNEL_ID_06: Final = '-1001847798054'
# BAHNHOFPLATZ_CHANNEL_ID_07: Final = '-1001885031649'
# BAHNHOFPLATZ_CHANNEL_ID_08: Final = '-1001972041919'
# BAHNHOFPLATZ_CHANNEL_ID_09: Final = '-1001959171341'
# BAHNHOFPLATZ_CHANNEL_ID_10: Final = '-1001878260812'
# BAHNHOFPLATZ_CHANNEL_ID_11: Final = '-1001904052376'
# BAHNHOFPLATZ_CHANNEL_ID_12: Final = '-1001881457658'

# HBF_URL = {
#     'Team 1': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=88&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=1&cnc-267=0&cnc-268=0&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0',
#     'Team 2': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=88&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=0&cnc-267=1&cnc-268=0&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0',
#     'Team 3': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=88&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=0&cnc-267=0&cnc-268=1&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0'
# }

# @app.route('/status')
# def status():    
#     return 'OK'

# @app.route('/')
# def hello_world():    
#     return 'Hello, World!'

# @scheduler.task('interval', id='do_job_1', seconds=300, misfire_grace_time=900)
# def job1():    
#     bot = telegram.Bot(token=TOKEN)
#     notify_aachen_termin(bot)
#     notify_aachen_anmeldung(bot)
    

# def notify_aachen_termin(bot: telegram.Bot):
#     is_available, res = superc_termin()
#     if is_available:
#         bot.send_message(chat_id=CHANNEL_ID, text=res)  

#     for key, value in HBF_URL.items():
#         is_available, res = aachen_hbf_termin(key, value)
#         if is_available:
#             bot.send_message(chat_id=HBF_CHANNEL_ID, text=res)

# def notify_aachen_anmeldung(bot: telegram.Bot):
#     next_months, next_years = get_next_months(4)
#     for month, year in zip(next_months, next_years):
#         notify_anmeldung_by_month_and_location(bot, year, month, Location.Katschhof)
#         notify_anmeldung_by_month_and_location(bot, year, month, Location.Bahnhofplatz)

# def notify_anmeldung_by_month_and_location(bot: telegram.Bot, year: str, month: str, loc: Location):
#     is_available, res = aachen_an(loc, year, month)
#     if is_available:
#         bot.send_message(chat_id=get_channel_id(loc, month), text=res)

# def get_channel_id(loc: Location, month: str):
#     month_dict = {}
#     if loc == Location.Katschhof:
#         month_dict = {
#             "01": KATSCHHOF_CHANNEL_ID_01,
#             "02": KATSCHHOF_CHANNEL_ID_02,
#             "03": KATSCHHOF_CHANNEL_ID_03,
#             "04": KATSCHHOF_CHANNEL_ID_04,
#             "05": KATSCHHOF_CHANNEL_ID_05,
#             "06": KATSCHHOF_CHANNEL_ID_06,
#             "07": KATSCHHOF_CHANNEL_ID_07,
#             "08": KATSCHHOF_CHANNEL_ID_08,
#             "09": KATSCHHOF_CHANNEL_ID_09,
#             "10": KATSCHHOF_CHANNEL_ID_10,
#             "11": KATSCHHOF_CHANNEL_ID_11,
#             "12": KATSCHHOF_CHANNEL_ID_12
#         }
#     elif loc == Location.Bahnhofplatz:
#         month_dict = {
#             "01": BAHNHOFPLATZ_CHANNEL_ID_01,
#             "02": BAHNHOFPLATZ_CHANNEL_ID_02,
#             "03": BAHNHOFPLATZ_CHANNEL_ID_03,
#             "04": BAHNHOFPLATZ_CHANNEL_ID_04,
#             "05": BAHNHOFPLATZ_CHANNEL_ID_05,
#             "06": BAHNHOFPLATZ_CHANNEL_ID_06,
#             "07": BAHNHOFPLATZ_CHANNEL_ID_07,
#             "08": BAHNHOFPLATZ_CHANNEL_ID_08,
#             "09": BAHNHOFPLATZ_CHANNEL_ID_09,
#             "10": BAHNHOFPLATZ_CHANNEL_ID_10,
#             "11": BAHNHOFPLATZ_CHANNEL_ID_11,
#             "12": BAHNHOFPLATZ_CHANNEL_ID_12
#         }
    
#     return month_dict.get(month, CHANNEL_ID)


# @scheduler.task('interval', id='do_job_2', seconds=300, misfire_grace_time=900)
# def job2():
#     r = requests.get(f'{URL}/status')
#     print(r)


def notify_aachen_driver(bot: telegram.Bot):
    is_available, res = driver_termin()
    if is_available:
        bot.send_message(chat_id="@aachen_driver", text=res)  

@scheduler.task('interval', id='do_job_3', seconds=300, misfire_grace_time=900)
def job3():
    bot = telegram.Bot(token=TOKEN)
    notify_aachen_driver(bot)
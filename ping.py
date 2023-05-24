import requests

URL = 'https://aachen-termin-bot.onrender.com'

def ping():
    r = requests.get(URL)
    print(r)

if __name__ == '__main__':
    ping()
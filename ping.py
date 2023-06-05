import requests

URL_TERMIN_BOT = 'https://aachen-termin-bot.onrender.com'
URL_GO_GERMANY = 'https://go-germany-api.onrender.com/status'

def ping():
    r1 = requests.get(URL_TERMIN_BOT)
    r2 = requests.get(URL_GO_GERMANY)    
    print(r1)
    print(r2)

if __name__ == '__main__':
    ping()
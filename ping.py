import requests

URL_TERMIN_BOT = 'https://aachen-termin-bot.onrender.com'
URL_GO_GERMANY = 'https://go-germany-api.onrender.com/status'

def ping():
    r1 = requests.get(URL_TERMIN_BOT)
    r2 = requests.get(URL_GO_GERMANY)    
    print(f"Ping results for {URL_TERMIN_BOT} and {URL_GO_GERMANY}:")
    print(f"Aachen Termin Bot: {r1.status_code}")
    print(f"Go Germany: {r2.status_code}")    

if __name__ == '__main__':
    ping()    
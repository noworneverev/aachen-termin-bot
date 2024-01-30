import requests

URL_TERMIN_BOT = 'https://aachen-termin-bot.onrender.com'
URL_GO_GERMANY = 'https://go-germany-api.onrender.com/status'

def ping():
    # r1 = requests.get(URL_TERMIN_BOT)
    # r2 = requests.get(URL_GO_GERMANY)    
    # print(r1)
    # print(r2)

    try:
        r1 = requests.get(URL_TERMIN_BOT)
        r1.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        print(f"Request to {URL_TERMIN_BOT} was successful:")
        print(r1.text)
    except Exception as ce:
        print(f"Connection error to {URL_TERMIN_BOT}: {ce}")    

    # try:
    #     r2 = requests.get(URL_GO_GERMANY)
    #     r2.raise_for_status()

    #     print(f"Request to {URL_GO_GERMANY} was successful:")
    #     print(r2.text)
    # except Exception as ce:
    #     print(f"Connection error to {URL_GO_GERMANY}: {ce}")

if __name__ == '__main__':
    ping()
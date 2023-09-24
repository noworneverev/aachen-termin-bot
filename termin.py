import requests
import logging
import bs4
# from requests_html import HTMLSession
# from requests_html import AsyncHTMLSession
# import datetime
import enum

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Location(enum.Enum):    
    Katschhof = "Bürgerservice Katschhof"
    Bahnhofplatz = "Bürgerservice Bahnhofplatz"

def get_termin_url(loc: Location):
    if loc == Location.Katschhof:
        pass
    elif loc == Location.Bahnhofplatz:
        pass

def aachen_an(loc: Location, year: str, month: str):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    url = ""
    if loc == Location.Katschhof:
        url = f"https://qtermin.de/api/timeslots?date={year}-{month}-01&serviceid=94948&rangesearch=1&caching=false&capacity=1&duration=10&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=70&appdeadline=0&appdeadlinewm=0&oneoff=null&msdcm=0&calendarid=57095,57096,57097,74724,74725,133598"
    elif loc == Location.Bahnhofplatz:
        url = f"https://www.qtermin.de/api/timeslots?date={year}-{month}-01&serviceid=94948&rangesearch=1&caching=false&capacity=1&duration=10&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=70&appdeadline=0&appdeadlinewm=0&oneoff=null&msdcm=0&calendarid=57003,57091,57092,57093,57094,71058,71059,71060,71061,71062,77257,77289,77291,77292,133608,133610,133607,133612,133614,133615,133616"

    if not url:
        logging.error(f'Invalid location: {loc.value}')
        return False, f'Invalid location: {loc.value}'
    
    
    headers = {"User-Agent": user_agent, "webid": 'bahnhofplatzkatschhof'}    
    res = requests.get(url, headers=headers).json()
    message = ''    

    for t in res:        
        if t['start'][5:7] == month:
            message += t['start'][:10]
            message += '\n'

    if message:        
        message = f'Available appointments at {loc.value} in {number_to_month(month)}:\n' + message[:-1]        
        logging.info(message)
        return True, message
    else:                
        message=  f'No available appointment at {loc.value} in {number_to_month(month)}'
        logging.info(message)
        return False, message
    

def number_to_month(number):
    month_dict = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    
    return month_dict.get(number, "Invalid Month")



def aachen_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    
    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/'    
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    # url_3 = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?mdt=52&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=0&cnc-202=0&cnc-189=0&cnc-203=0&cnc-196=0&cnc-200=0&cnc-199=0&cnc-188=0&cnc-186=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-185=0&cnc-187=0&cnc-190=0&cnc-195=0&cnc-191=1&cnc-194=0&cnc-197=0&cnc-192=0"    
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest?mdt=75&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=0&cnc-202=0&cnc-227=0&cnc-189=0&cnc-203=0&cnc-196=0&cnc-190=0&cnc-185=0&cnc-187=0&cnc-188=0&cnc-186=0&cnc-192=0&cnc-191=1&cnc-194=0&cnc-197=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-195=0&cnc-200=0&cnc-225=0'
    url_4 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-191=1&loc=28'             
    res_2 = requests.get(url_2, headers=headers)            
    res_3 = requests.get(url_3, headers=headers,cookies=res_2.cookies)    
    payload = {'loc':'28', 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen - Außenstelle RWTH auswählen'}
    
    # res_4 = requests.get(url_4, headers=headers,cookies=res_3.cookies)
    res_4 = requests.post(url_3, headers=headers,cookies=res_2.cookies, data=payload)        
        
    if "Kein freier Termin verfügbar" not in res_4.text:
        logging.info(f'{"Appointment available now!"}')

        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        h3 = div.find_all("h3")
        res = 'New appointments are available now!\n'
        for h in h3:
            res += h.text + '\n'             
        return True, res[:-1]
    else:
        logging.info(f'{"No appointment is available"}')                
        return False, "No appointment is available"

# def berlin_termin():
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
#     headers = {"User-Agent": user_agent}

#     url_start = 'https://otv.verwalt-berlin.de/ams/TerminBuchen'
#     # url_buchen = 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?sprachauswahl=de&mfDirect=true'
#     url_buchen = 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?sprachauswahl=de'
#     url_info = 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?dswid=6824&dsrid=30&sprachauswahl=de'
#     url= 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng;jsessionid=MAjR5U1_oZW4bBVXQw5WEHd0MTXOGLcJKM6zE5EJ.frontend-2?dswid=2704&dsrid=207&sprachauswahl=de'

#     res_start = requests.get(url_start, headers=headers)
#     domain = res_start.cookies.list_domains()[0]
#     JSESSIONID = res_start.cookies['JSESSIONID']
#     SERVERID = res_start.cookies['SERVERID']
#     TS018ca6c6 = res_start.cookies['TS018ca6c6']
#     otv_neu = res_start.cookies['otv_neu']    
    
#     headers = { 
#                 "User-Agent": user_agent,
#                 "Cookie": f"check=valid; JSESSIONID={JSESSIONID}; SERVERID={SERVERID}; otv_neu={otv_neu}; TS018ca6c6={TS018ca6c6}",
#                 "Host": "otv.verwalt-berlin.de", 
#                 "Referer": url_start,
#                 "Sec-Fetch-Dest": "document",
#                 "Sec-Fetch-Mode": "navigate",
#                 "Sec-Fetch-Site": "same-origin",
#                 "Sec-Fetch-User": "?1",
#                 "Upgrade-Insecure-Requests": "1",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#                 "Accept-Encoding": "gzip, deflate, br",
#                 "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",

#               }
#     res_buchen = requests.get(url_buchen, headers=headers)
#     print(res_buchen.url)
#     # print(res_buchen.cookies)
#     # res_buchen = requests.get(url_buchen, headers=headers, cookies=res_start.cookies)
#     # print(res_buchen.cookies)
#     # for res_buchen_cookie in res_buchen.cookies:
#     #     print(res_buchen_cookie.name, res_buchen_cookie.value)

#     # # print(res_buchen.text)
#     # soup = bs4.BeautifulSoup(res_buchen.text, 'html.parser')
#     # print(soup.text)

# asession = AsyncHTMLSession()
# # url_buchen = 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?sprachauswahl=de&mfDirect=true'
# url_buchen = 'https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?sprachauswahl=de'
# async def berlin_termin():
#     r = await asession.get(url_buchen)
#     return r

# results = asession.run(berlin_termin)
# for result in results:
#     # print(result.html.url)
#     # print(result.url)
#     soup = bs4.BeautifulSoup(result.html.html, 'html.parser')
#     print(soup.text)

import requests
import logging
import bs4
import enum

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Location(enum.Enum):    
    Katschhof = "Bürgerservice Katschhof"
    Bahnhofplatz = "Bürgerservice Bahnhofplatz"

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

def superc_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'    
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=0&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=1&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0'        
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)
    res_2 = session.get(url_2)
    payload = {'loc':'42', 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen - Außenstelle RWTH auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            logging.info(f'{"Appointment available now in SuperC!"}')
            h3 = div.find_all("h3")
            res = 'New appointments are available now!\n'
            for h in h3:
                res += h.text + '\n'             
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'{"Appointment available now in SuperC!"}')
            logging.info(f'{summary_text}')
            return True, 'New appointments are available now!\n' + summary_text
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now in SuperC!"}')                
            return False, "Cannot find sugg_accordion! Possible new appointments are available now!"
    else:
        logging.info(f'{"No appointment is available in SuperC."}')                
        return False, "No appointment is available in SuperC"    

hbf_url = {    
    'Team 1': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=1&cnc-296=0&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0',
    'Team 2': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=1&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0',
    'Team 3': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=0&cnc-297=1&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0'
}

def aachen_hbf_termin(team_name ,url_team):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_2 = url_team
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)
    res_2 = session.get(url_2)
    payload = {'loc':'45', 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen, 2. Etage auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            h3 = div.find_all("h3")
            res = f'New appointments are available now at HBF {team_name}!\n'
            for h in h3:
                res += h.text + '\n'             
            logging.info(res[:-1])
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'Appointment available now at HBF {team_name}!')
            logging.info(f'{summary_text}')
            return True, f'New appointments are available now at HBF {team_name}!\n' + summary_text
        else:
            logging.info(f'Cannot find sugg_accordion! Possible new appointments are available now at HBF {team_name}!')                
            return False, f"Cannot find sugg_accordion! Possible new appointments are available now at HBF {team_name}!"
    else:
        logging.info(f'No appointment is available at HBF {team_name}.')                
        return False, f'No appointment is available at HBF {team_name}.'   

def driver_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/select2?md=2'
    url_2 = 'https://termine.staedteregion-aachen.de/location?mdt=47&select_cnc=1&cnc-823=0&cnc-820=0&cnc-828=0&cnc-824=0&cnc-831=0&cnc-811=0&cnc-960=0&cnc-813=0&cnc-812=0&cnc-814=0&cnc-818=1&cnc-817=0&cnc-825=0&cnc-816=0&cnc-832=0&cnc-833=0&cnc-900=0&cnc-901=0&cnc-899=0&cnc-896=0&cnc-898=0&cnc-958=0&cnc-902=0&cnc-897=0&cnc-946=0&cnc-948=0&cnc-950=0&cnc-949=0&cnc-945=0&cnc-955=0&cnc-954=0&cnc-953=0&cnc-952=0&cnc-951=0'    
    url_3 = 'https://termine.staedteregion-aachen.de/suggest'
    res_1 = session.get(url_1)
    res_2 = session.get(url_2)
    payload = {'loc':'43', 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'StädteRegion Aachen Führerscheinstelle auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            logging.info(f'{"Appointment available now in DRIVER LICENSE!"}')
            h3 = div.find_all("h3")
            res = 'New appointments are available now!\n'
            for h in h3:
                res += h.text + '\n'             
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'{"Appointment available now in DRIVER LICENSE!"}')
            logging.info(f'{summary_text}')
            return True, 'New appointments are available now!\n' + summary_text
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now in DRIVER LICENSE!"}')                
            return False, "Cannot find sugg_accordion! Possible new appointments are available now!"
    else:
        logging.info(f'{"No appointment is available in DRIVER LICENSE."}')                
        return False, "No appointment is available in DRIVER LICENSE"

# superc_termin()
for key, value in hbf_url.items():
    aachen_hbf_termin(key, value)

# driver_termin()
superc_termin()
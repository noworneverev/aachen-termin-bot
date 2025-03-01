import requests
from typing import Final
import logging
import bs4
from utils import is_date_within_n_days, Location

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
User agent string for looking for Termine.    
"""
USER_AGENT_STRING: Final = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)

def aachen_an(loc: Location, year: str, month: str):
    url = ""
    if loc == Location.Katschhof:
        url = f"https://qtermin.de/api/timeslots?date={year}-{month}-01&serviceid=94948&rangesearch=1&caching=false&capacity=1&duration=10&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=70&appdeadline=0&appdeadlinewm=0&oneoff=null&msdcm=0&calendarid=57095,57096,57097,74724,74725,133598"
    elif loc == Location.Bahnhofplatz:
        url = f"https://www.qtermin.de/api/timeslots?date={year}-{month}-01&serviceid=94948&rangesearch=1&caching=false&capacity=1&duration=10&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=70&appdeadline=0&appdeadlinewm=0&oneoff=null&msdcm=0&calendarid=57003,57091,57092,57093,57094,71058,71059,71060,71061,71062,77257,77289,77291,77292,133608,133610,133607,133612,133614,133615,133616"

    if not url:
        logging.error(f'Invalid location: {loc.value}')
        return False, f'Invalid location: {loc.value}'
    
    
    headers = {"User-Agent": USER_AGENT_STRING, "webid": 'bahnhofplatzkatschhof'}    
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


def format_url_2(soup: bs4.BeautifulSoup, needle: str, form_options_position: int = 0):
    """ Find the form options and format a url for the appropriate entry on 
    the "Auswahl des Anliegens" page of the appointment finder.

    :param soup: bs4.Beautifulsoup to search for the right <h3><h3/> element.
    :param needle: String to search for in a <h3></h3> element.
    :param form_options_position: Some options on the page have multiple elements (students / family / employees, for example)
    """
    url_base = "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1"
    header_element = soup.find("h3", string=lambda s: needle in s if s else False)
    if header_element:
        next_sibling = header_element.find_next_sibling()
        if next_sibling:
            li_elements = next_sibling.find_all("li")
            cnc_id = li_elements[form_options_position].get("id").split("-")[-1] if li_elements else None
            url_2 = f"{url_base}&cnc-{cnc_id}=1"            
            logging.info(f"{f'{needle} has cnc id: ' + cnc_id}")
            return True, url_2
        else:
            return False, f"Sibling element to h3 with '{needle}' not found."
    else:
        logging.info(f"Element containing '{needle}' not found.")
        return False, f"Element containing '{needle}' not found."


def abholung_termin():
    # The structure of the code is exactly the same as superc_termin, I'm just too lazy to refactor it.
    headers = {"User-Agent": USER_AGENT_STRING}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'        
    url_2 = ''
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)

    # Get RWTH cnc id
    soup = bs4.BeautifulSoup(res_1.content, 'html.parser')
    success, url_2 = format_url_2(soup, "Abholung", 0)
    if success:
        res_2 = session.get(url_2)
    else:
        return False, url_2

    soup = bs4.BeautifulSoup(res_2.content, 'html.parser')
    loc = soup.find('input', {'name': 'loc'}).get('value')
    logging.info(f'{"Abholung loc: " + loc}')

    payload = {'loc':str(loc), 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen - Aachen Arkaden, Trierer Straße 1, Aachen auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            logging.info(f'{"Appointment available now in Abholung Aufenthaltserlaubnis!"}')
            h3 = div.find_all("h3")
            res = 'New appointments are available now\n'
            flag = False
            for h in h3:
                if is_date_within_n_days(h.text, 50):
                    res += h.text + '\n'
                    flag = True
            if not flag:
                logging.info(f'{"There are appointments available, but they are not within 50 days from today."}')
                return False, "There are appointments available, but they are not within 50 days from today."
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            if is_date_within_n_days(summary_text, 50):                
                logging.info(f'{"Appointment available now in Abholung Aufenthaltserlaubnis!"}')
                logging.info(f'{summary_text}')
                return True, 'New appointments are available now\n' + summary_text
            else:
                logging.info(f'{"There are appointments available, but they are not within 50 days from today."}')
                return False, "There are appointments available, but they are not within 50 days from today."            
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now in Abholung Aufenthaltserlaubnis!"}')                
            return False, "Cannot find sugg_accordion! Possible new appointments are available now"
    else:
        logging.info(f'{"No appointment is available in Abholung Aufenthaltserlaubnis."}')                
        return False, "No appointment is available in Abholung Aufenthaltserlaubnis"

def superc_termin(form_pos: int = 0):
    """ Check if appointments are available at the Außenstelle SuperC.
    
    param: form_pos: There are 3 Anliegen to select. 0 for students, 1 for family, 2 for employees. 
    """
    form_labels = {
        0: "RWTH Studenten",
        1: "RWTH Familienangehörige",
        2: "RWTH Mitarbeitende & Forschende"
    }

    if form_pos not in form_labels:
        logging.error(f"Invalid form_pos: {form_pos}. Must be 0, 1, or 2")
        return False, "Invalid request type"
    
    form_label = form_labels[form_pos]
    logging.info(f"Checking SuperC appointments for: {form_label}")

    headers = {"User-Agent": USER_AGENT_STRING}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'        
    url_2 = ''
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)

    # Get RWTH cnc id
    soup = bs4.BeautifulSoup(res_1.content, 'html.parser')         
    success, url_2 = format_url_2(soup, "Super C", form_pos)
    if success:
        res_2 = session.get(url_2)
    else:
        return False, url_2

    soup = bs4.BeautifulSoup(res_2.content, 'html.parser')
    loc = soup.find('input', {'name': 'loc'}).get('value')
    logging.info(f'{"Super C loc: " + loc}')

    payload = {'loc':str(loc), 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen - Außenstelle RWTH auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            # logging.info(f'{"Appointment available now in SuperC!"}')
            logging.info(f"Appointments found for {form_label} at SuperC!")
            h3 = div.find_all("h3")
            # res = 'New appointments are available now\n'
            res = f'New appointments available for {form_label}:\n'
            for h in h3:
                res += h.text + '\n'             
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'{"Appointment available now in SuperC!"}')            
            logging.info(f"Immediate availability for {form_label} at SuperC!")
            return True, f'{form_label}:\n{summary_text}'
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now in SuperC!"}')                
            return False, "Cannot find sugg_accordion! Possible new appointments are available now"
    else:        
        logging.info(f"No appointments available for {form_label} at SuperC")       
        return False, f"No available slots for {form_label} at this time"

def fh_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'        
    url_2 = ''
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)

    # Get RWTH cnc id
    soup = bs4.BeautifulSoup(res_1.content, 'html.parser')         
    header_element = soup.find('h3', string=lambda s: 'Fachhochschule Aachen' in s if s else False)
    
    if header_element:        
        next_sibling = header_element.find_next_sibling()
        if next_sibling:
            li_elements = next_sibling.find_all('li')
            cnc_id = li_elements[0].get('id').split('-')[-1] if li_elements else None
            url_2 = f'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-{cnc_id}=1'
            logging.info(f'{"Fachhochschule Aachen cnc id: " + cnc_id}')
    else:
        logging.info("Element containing 'Fachhochschule Aachen' not found.")
        return False, "Element containing 'Fachhochschule Aachen' not found."
        
    res_2 = session.get(url_2)

    soup = bs4.BeautifulSoup(res_2.content, 'html.parser')
    loc = soup.find('input', {'name': 'loc'}).get('value')
    logging.info(f'{"Fachhochschule Aachen loc: " + loc}')

    payload = {'loc':str(loc), 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen, 2. Etage auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            logging.info(f'{"Appointment available now in Fachhochschule Aachen!"}')
            h3 = div.find_all("h3")
            res = 'New appointments are available now\n'
            for h in h3:
                res += h.text + '\n'             
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'{"Appointment available now in Fachhochschule Aachen!"}')
            logging.info(f'{summary_text}')
            return True, 'New appointments are available now\n' + summary_text
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now in Fachhochschule Aachen!"}')                
            return False, "Cannot find sugg_accordion! Possible new appointments are available now"
    else:
        logging.info(f'{"No appointment is available in Fachhochschule Aachen."}')                
        return False, "No appointment is available in Fachhochschule Aachen"

# hbf_url = {
#     'Team 1': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-293=1',
#     'Team 2': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-296=1',
#     'Team 3': 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-297=1'
# }

def get_hbf_url(res_1, team_name):    
    soup = bs4.BeautifulSoup(res_1.content, 'html.parser')         
    header_element = soup.find('h3', string=lambda s: 'Aufenthalt' in s if s else False)
    url_2 = ''
    li_index = int(team_name.split(' ')[-1]) - 1
    if header_element:        
        next_sibling = header_element.find_next_sibling()
        if next_sibling:
            li_elements = next_sibling.find_all('li')
            cnc_id = li_elements[li_index].get('id').split('-')[-1] if li_elements else None
            url_2 = f'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-{cnc_id}=1'
            logging.info(f"Aufenthalt {team_name} cnc id: {cnc_id}")
    else:
        logging.info("Element containing 'Aufenthalt' not found.")        

    return url_2

def aachen_hbf_termin(team_name):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_2 = ''    
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)

    url_2 = get_hbf_url(res_1, team_name)

    res_2 = session.get(url_2)
    soup = bs4.BeautifulSoup(res_2.content, 'html.parser')
    loc = soup.find('input', {'name': 'loc'}).get('value')
    logging.info(f"Aufenthalt {team_name} loc: {loc}")

    payload = {'loc':str(loc), 'gps_lat': '55.77858', 'gps_long': '65.07867', 'select_location': 'Ausländeramt Aachen, 2. Etage auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            h3 = div.find_all("h3")
            res = f'{team_name}\n'
            for h in h3:
                res += h.text + '\n'             
            logging.info(res[:-1])
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'Appointment available now at HBF {team_name}')
            logging.info(f'{summary_text}')
            return True, f'{team_name}\n' + summary_text
        else:
            logging.info(f'Cannot find sugg_accordion! Possible new appointments are available now at HBF {team_name}')                
            return False, f"Cannot find sugg_accordion! Possible new appointments are available now at HBF {team_name}"
    else:
        logging.info(f'No appointment is available at HBF {team_name}.')                
        return False, f'No appointment is available at HBF {team_name}.'   


# superc_termin(1)
# aachen_hbf_termin('Team 1')
# aachen_hbf_termin('Team 2')
# aachen_hbf_termin('Team 3')
# for key, value in hbf_url.items():
#     aachen_hbf_termin(key, value)

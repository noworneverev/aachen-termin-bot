import requests
from typing import Final
import logging
import bs4
from utils import is_date_within_n_days, Location
from urllib.parse import urlencode, urljoin

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


def format_url_2(
    soup: bs4.BeautifulSoup,
    needle: str,
    form_options_position: int = 0,
    *,
    page_url: str = "https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1",
):
    """ Find the form options and format a url for the appropriate entry on 
    the "Auswahl des Anliegens" page of the appointment finder.

    :param soup: bs4.Beautifulsoup to search for the right <h3><h3/> element.
    :param needle: String to search for in a <h3></h3> element.
    :param form_options_position: Some options on the page have multiple elements (students / family / employees, for example)
    """
    header_element = soup.find(
        "h3", string=lambda value: needle in value if value else False
    )
    if not header_element:
        logging.info("Element containing '%s' not found.", needle)
        return False, f"Element containing '{needle}' not found."

    form = header_element.find_parent("form", id="cnc-select-form")
    mdt = form.find("input", {"name": "mdt"}) if form else None
    if not form or not mdt or not mdt.get("value"):
        return False, "The appointment form is missing its mdt value."

    concern_group = header_element.find_parent(
        "div", id=lambda value: value and value.startswith("concerns_accordion-")
    )
    concerns = concern_group.select("input.cnc-number[name^='cnc-']") if concern_group else []
    if form_options_position < 0 or form_options_position >= len(concerns):
        return False, f"No concern at position {form_options_position} for '{needle}'."

    concern_name = concerns[form_options_position].get("name")
    if not concern_name:
        return False, f"Concern at position {form_options_position} has no name."

    action = form.get("action") or "location"
    location_url = urljoin(page_url, action)
    query = urlencode({"mdt": mdt["value"], "select_cnc": "1", concern_name: "1"})
    logging.info("%s has concern id: %s", needle, concern_name.removeprefix("cnc-"))
    return True, f"{location_url}?{query}"


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
    success, url_2 = format_url_2(soup, "Abholung", 0, page_url=url_1)
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
    success, url_2 = format_url_2(soup, "Super C", form_pos, page_url=url_1)
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
    success, url_2 = format_url_2(soup, "Fachhochschule Aachen", 0, page_url=url_1)
    if not success:
        return False, url_2
        
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

def _check_selected_appointment(session, location_url: str, suggest_url: str, label: str):
    location_response = session.get(location_url, timeout=30)
    location_response.raise_for_status()
    soup = bs4.BeautifulSoup(location_response.content, 'html.parser')

    fields = {}
    for name in ('loc', 'gps_lat', 'gps_long'):
        field = soup.find('input', {'name': name})
        if not field or not field.get('value'):
            return False, f"Could not read {name} for {label}."
        fields[name] = field['value']

    continue_button = soup.find('input', {'name': 'select_location', 'value': 'Weiter'})
    if not continue_button:
        return False, f"Could not find the continue button for {label}."

    fields['select_location'] = continue_button['value']
    session.post(location_url, data=fields, timeout=30).raise_for_status()
    response = session.get(suggest_url, timeout=30)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    no_appointments = (
        "Kein freier Termin verfügbar" in response.text
        or "Derzeit sind leider alle Termine vergeben" in response.text
        or "Keine Zeiten verfügbar" in response.text
    )
    if no_appointments:
        logging.info("No appointments are currently available for %s.", label)
        return False, f"No appointments are currently available for {label}."

    accordion = soup.find('div', {'id': 'sugg_accordion'})
    summary = soup.find('summary', {'id': 'suggest_details_summary'})
    if accordion:
        dates = [heading.get_text(' ', strip=True) for heading in accordion.find_all('h3')]
        if dates:
            return True, f"Appointments available for {label}:\n" + '\n'.join(dates)
    if summary:
        return True, f"Appointments available for {label}:\n{summary.get_text(' ', strip=True)}"

    return False, f"Could not recognize the appointment response for {label}."


def aachen_hbf_termin(team_name=None):
    """Check the current Hbf service, now booked at Aachen Arkaden."""
    select_url = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    suggest_url = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT_STRING})

    response = session.get(select_url, timeout=30)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    success, location_url = format_url_2(soup, 'Infostelle', 0, page_url=select_url)
    if not success:
        return False, location_url

    return _check_selected_appointment(
        session, location_url, suggest_url, 'Hbf at Aachen Arkaden'
    )


DRIVER_LICENSE_REQUESTS = (
    ('Ersterteilung einer Fahrerlaubnis', 'new or extended driver license'),
    ('Umschreibung ausländische Fahrerlaubnis', 'foreign driver license conversion'),
    ('Verlängerung einer Fahrerlaubnis', 'driver license renewal'),
)


def driver_termin():
    """Check Würselen appointments for the driver-license requests in issue #6."""
    select_url = 'https://termine.staedteregion-aachen.de/select2?md=2'
    suggest_url = 'https://termine.staedteregion-aachen.de/suggest'
    available = []
    results = []

    for concern, label in DRIVER_LICENSE_REQUESTS:
        session = requests.Session()
        session.headers.update({'User-Agent': USER_AGENT_STRING})
        response = session.get(select_url, timeout=30)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        success, location_url = format_url_2(
            soup, concern, 0, page_url=select_url
        )
        if not success:
            results.append(location_url)
            continue

        is_available, result = _check_selected_appointment(
            session, location_url, suggest_url, label
        )
        if is_available:
            available.append(result)
        results.append(result)

    if available:
        return True, '\n\n'.join(available)
    return False, '\n'.join(results)


# superc_termin(1)
# aachen_hbf_termin('Team 1')
# aachen_hbf_termin('Team 2')
# aachen_hbf_termin('Team 3')
# for key, value in hbf_url.items():
#     aachen_hbf_termin(key, value)

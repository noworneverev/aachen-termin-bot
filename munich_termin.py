import json
import re
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_token(session, url):
    response = session.get(url)
    try:
        token = re.search(r'FRM_CASETYPES_token" value="(.*?)"', response.text).group(1)
        return token
    except AttributeError:
        return None

def munich_notfall_termin():
    url = "https://terminvereinbarung.muenchen.de/abh/termin/"
    session = requests.Session()

    token = get_token(session, url)

    data = {
        'FRM_CASETYPES_token': token,
        'step': 'WEB_APPOINT_SEARCH_BY_CASETYPES',
        'CASETYPES[Notfalltermin UA 35]': 1,
    }
    response = session.post(url, data)
    json_str = re.search(r'jsonAppoints = \'(.*?)\'', response.text).group(1)
    appointments = json.loads(json_str)['LOADBALANCER']['appoints']

    message = []
    has_appointments = False

    for date, times in appointments.items():
        if times:
            has_appointments = True
            message.append(f"Date: {date}")
            for time in times:
                message.append(f" - {time}")

    message_str = "\n".join(message)
    if has_appointments:
        logging.info(f"{'Available slots for Munich: ' + message_str}")                        
        return True, message_str
    else:
        logging.info(f'{"No available slots for any date."}')
        return False, "No available slots for any date."
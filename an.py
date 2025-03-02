# # import requests
# from curl_cffi import requests
# import logging
# import re
# import json
# import http.client as http_client
# from html import unescape
# from datetime import datetime
# from collections import defaultdict
# from utils import get_channel_id, Location

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# class Appointment:
#     def __init__(self, date_time, unit, duration, link):
#         self.date_time: datetime = date_time
#         self.unit = unit
#         self.duration = duration
#         self.link = link

#     def __str__(self):
#         return f"Date: {self.date_time}, Unit: {self.unit}, Duration: {self.duration} minutes"
    
#     def __repr__(self):
#         return f"Date: {self.date_time}, Unit: {self.unit}, Duration: {self.duration} minutes"

#     # Parse from json
#     @staticmethod
#     def from_json(json_data):                                
#         datetime_str = json_data["datetime_iso86001"]
#         if len(datetime_str) > 26:  # Check if microseconds part has more than 6 digits
#             datetime_str = datetime_str[:26] + datetime_str[26+1:]  # Truncate the extra digit
        
#         return Appointment(
#             datetime.fromisoformat(datetime_str),
#             json_data["unit"],
#             json_data["duration"],
#             "https://stadt-aachen.saas.smartcjm.com" + json_data["link"]
#         )


# def enable_debug():
#     http_client.HTTPConnection.debuglevel = 1
#     logging.basicConfig()
#     logging.getLogger().setLevel(logging.DEBUG)
#     requests_log = logging.getLogger("requests.packages.urllib3")
#     requests_log.setLevel(logging.DEBUG)
#     requests_log.propagate = True


# def get_appointments() -> list[Appointment]:
#     # headers = {
#     #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     #     'Accept-Language': 'en-US,en;q=0.9',
#     #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
#     # }
#     headers = {
#         # ':authority': 'stadt-aachen.saas.smartcjm.com',
#         # ':method': 'GET',
#         # ':path': '/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34',
#         # ':scheme': 'https',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Referer': 'https://stadt-aachen.saas.smartcjm.com/',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'Connection': 'keep-alive',
#         'DNT': '1',
#     }
#     domain = "https://stadt-aachen.saas.smartcjm.com"    
#     logging.info("Getting wsid token")

#     # session = requests.Session()
#     # session.headers.update(headers)
#     initial_url = domain + "/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34"
#     # response = session.get(initial_url, allow_redirects=False)
    
#     with requests.Session(impersonate="chrome120") as session:
#         response = session.get(
#             initial_url,
#             headers=headers,
#             allow_redirects=False  # Critical to handle redirects manually
#         )

#         if response.status_code != 302:
#             logging.error(response)
#             logging.error(f"Failed to get wsid. Status: {response.status_code}")
#             logging.error(response.text)
#             exit()

#         # Extract redirected URL with wsid
#         base_url = domain + response.headers["Location"]
#         logging.info(f"Redirect URL: {base_url}")

#     # # response = requests.get(domain + "/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34",
#     # #                         headers=headers,
#     # #                         allow_redirects=False)

#     # # Base url should return 302 with 'wsid' as a parameter in the url        
#     # logging.info(response)
#     # logging.info(response.headers)    
#     # if response.status_code != 302:        
#     #     logging.error("Couldn't get wsid token. Status code: %d", response.status_code)
#     #     # print("Couldn't get wsid token")
#     #     exit()
    
#     # # Get parameter from the url
#     # base_url = domain + response.headers["Location"]
#     # # # Only send cookies "__RequestVerificationToken" and "ASP.NET_SessionId"
#     # # cookies = {
#     # #     "__RequestVerificationToken": response.cookies.get_dict()["__RequestVerificationToken"],
#     # #     "ASP.NET_SessionId": response.cookies.get_dict()["ASP.NET_SessionId"],
#     # # }    
#     # # response2 = requests.get(base_url, cookies=cookies, headers=headers, allow_redirects=False)

#         response2 = session.get(base_url, allow_redirects=False)

#         # Load request token
#         pattern = (r"^(?:.*)<input type='hidden' id='RequestVerificationToken' name='__RequestVerificationToken' value='("
#                 r".*?)' />")
#         match = re.search(pattern, response2.text, flags=re.MULTILINE)
#         if match:
#             form_token = match.group(1)
#         else:
#             print("Couldn't get form token")
#             exit()

#         # an bahnhoftplatz and katschhof
#         form_data = '&action_type=&steps=serviceslocationssearch_resultsbookingfinish&step_current=services&step_current_index=0&step_goto=%2B1&services=&services=7bee4872-ba56-4070-9f6d-f45afdf491cb&service_7bee4872-ba56-4070-9f6d-f45afdf491cb_amount=1'

#         # Test
#         # form_data = '&action_type=&steps=serviceslocationssearch_resultsbookingfinish&step_current=services&step_current_index=0&step_goto=%2B1&services=&services=116df7ba-ea4e-4cf0-b6b9-0723d37ef78d&service_116df7ba-ea4e-4cf0-b6b9-0723d37ef78d_amount=1&services=e2da5155-fe39-4a21-bc07-46cd16a824b9&service_e2da5155-fe39-4a21-bc07-46cd16a824b9_amount=0&services=167f484a-f65d-49cf-8925-dca7be061b36&service_167f484a-f65d-49cf-8925-dca7be061b36_amount=0&services=c4e3989a-e5c0-418f-9198-80493c707ec2&service_c4e3989a-e5c0-418f-9198-80493c707ec2_amount=0&services=fae35b04-9e00-4f73-b1f2-e1ad0a17a87e&service_fae35b04-9e00-4f73-b1f2-e1ad0a17a87e_amount=0&services=10b657a5-0e90-44bc-b72a-2cfec873f6d2&service_10b657a5-0e90-44bc-b72a-2cfec873f6d2_amount=0&services=00dc099a-f550-4481-b1da-48321aea5224&service_00dc099a-f550-4481-b1da-48321aea5224_amount=0&services=c4893630-52bf-4f77-b728-f09407c728e3&service_c4893630-52bf-4f77-b728-f09407c728e3_amount=0&services=0886bc62-fa3e-405a-af63-8054959e85b3&service_0886bc62-fa3e-405a-af63-8054959e85b3_amount=0&services=716e4507-b635-4dca-8b86-00c10da3d3f9&service_716e4507-b635-4dca-8b86-00c10da3d3f9_amount=0&services=74575ac4-9906-4ad5-a8af-aa556e526704&service_74575ac4-9906-4ad5-a8af-aa556e526704_amount=0&services=0f3887e6-be79-46fc-a5b1-af02110d91be&service_0f3887e6-be79-46fc-a5b1-af02110d91be_amount=0&services=d9c6e7d3-d24d-4ccf-8fd4-62ba9c05caf7&service_d9c6e7d3-d24d-4ccf-8fd4-62ba9c05caf7_amount=0&services=51d53890-e2e0-4f76-a05d-537341860a51&service_51d53890-e2e0-4f76-a05d-537341860a51_amount=0&services=a38ae120-a5a8-4fe7-a5b1-7a7a938a07db&service_a38ae120-a5a8-4fe7-a5b1-7a7a938a07db_amount=0&services=d60dc34b-8586-48bd-9feb-23bc6fa91794&service_d60dc34b-8586-48bd-9feb-23bc6fa91794_amount=0&services=07103639-8025-4df0-9772-220e84eb0af2&service_07103639-8025-4df0-9772-220e84eb0af2_amount=0&services=5e0d7cd5-8784-43f0-a3ac-b10da3d2af96&service_5e0d7cd5-8784-43f0-a3ac-b10da3d2af96_amount=0&services=7d4c84e7-fb13-45c1-97a6-185af8235b6e&service_7d4c84e7-fb13-45c1-97a6-185af8235b6e_amount=0&services=2fc984c8-70b3-439c-9dca-b77db3ad76d8&service_2fc984c8-70b3-439c-9dca-b77db3ad76d8_amount=0&services=05bdef1d-1b12-45ba-bd29-fae0d1a58ed7&service_05bdef1d-1b12-45ba-bd29-fae0d1a58ed7_amount=0&services=7caa3811-0ba7-4e31-841e-aa69831d7782&service_7caa3811-0ba7-4e31-841e-aa69831d7782_amount=0&services=7028a6df-7a61-40f8-a920-3ec5c9d1f969&service_7028a6df-7a61-40f8-a920-3ec5c9d1f969_amount=0&services=146c80d6-bb02-42b8-aafa-bd3e855414c9&service_146c80d6-bb02-42b8-aafa-bd3e855414c9_amount=0&services=64a30e77-8224-41e8-bee9-624464dcd860&service_64a30e77-8224-41e8-bee9-624464dcd860_amount=0&services=cc8b1d05-8cd9-4555-a666-39ed185292ba&service_cc8b1d05-8cd9-4555-a666-39ed185292ba_amount=0&services=38c66af1-44e8-4781-804d-1693e703a346&service_38c66af1-44e8-4781-804d-1693e703a346_amount=0&services=b0a3bbe1-4747-44cb-a8d3-b56a3be9fe15&service_b0a3bbe1-4747-44cb-a8d3-b56a3be9fe15_amount=0&services=b755ee1f-9df1-4a66-acfd-76b9e46b1211&service_b755ee1f-9df1-4a66-acfd-76b9e46b1211_amount=0&services=216bbe43-d673-472b-be08-fe122ee1bc2b&service_216bbe43-d673-472b-be08-fe122ee1bc2b_amount=0&services=b829df33-9df6-4bd9-b740-301df3efb643&service_b829df33-9df6-4bd9-b740-301df3efb643_amount=0&services=2db0b2e2-8f00-4aa6-a08c-44dff95cc043&service_2db0b2e2-8f00-4aa6-a08c-44dff95cc043_amount=0&services=7bee4872-ba56-4070-9f6d-f45afdf491cb&service_7bee4872-ba56-4070-9f6d-f45afdf491cb_amount=0&services=d1a00eaf-f73b-4e98-ac2f-568b2d9c16c1&service_d1a00eaf-f73b-4e98-ac2f-568b2d9c16c1_amount=0&services=4a561c29-1721-4e27-b470-1a3265bf93ab&service_4a561c29-1721-4e27-b470-1a3265bf93ab_amount=0&services=1d2f6113-811d-4643-87d0-ebd3a7780959&service_1d2f6113-811d-4643-87d0-ebd3a7780959_amount=0&services=4c62d7e6-1c14-44a2-a8ea-3dac4b680023&service_4c62d7e6-1c14-44a2-a8ea-3dac4b680023_amount=0&services=98025ae5-88a5-4e8e-ac53-6ddd11231543&service_98025ae5-88a5-4e8e-ac53-6ddd11231543_amount=0&services=b98b99d3-aa3b-4af8-99c6-ed9580de78aa&service_b98b99d3-aa3b-4af8-99c6-ed9580de78aa_amount=0&services=bab4aab0-4572-4ae6-9b81-5db9f7ea75df&service_bab4aab0-4572-4ae6-9b81-5db9f7ea75df_amount=0&services=3f6be2ff-0acf-477f-afd7-1bc3400dfa0e&service_3f6be2ff-0acf-477f-afd7-1bc3400dfa0e_amount=0&services=f8a495fc-90bf-4e96-a776-802483d2b542&service_f8a495fc-90bf-4e96-a776-802483d2b542_amount=0&services=602452fb-fdcf-49ad-a3f6-48dba4af97db&service_602452fb-fdcf-49ad-a3f6-48dba4af97db_amount=0&services=9968f6be-36d5-494e-846d-cdcb0388b221&service_9968f6be-36d5-494e-846d-cdcb0388b221_amount=0'

#         form_data = "__RequestVerificationToken=" + form_token + form_data

#         # Send post to base_url with form_data
#         headers = {"Content-Type": "application/x-www-form-urlencoded"}
#         # requests.post(base_url, data=form_data, cookies=cookies, headers=headers, allow_redirects=False)
#         session.post(base_url, data=form_data, headers=headers, allow_redirects=False)

#         # Finally, get the appointments
#         url = base_url.split("?")[0] + "search_result?search_mode=all&" + base_url.split("?")[1]
#         # response4 = requests.get(url, cookies=cookies, allow_redirects=False)
#         response4 = session.get(url, allow_redirects=False)

#         pattern = r"(?<=<div id=\"json_appointment_list\">).*?(?=</div>)"
#         match = re.search(pattern, response4.text, flags=re.DOTALL)

#         if match:
#             appointments_json = json.loads(unescape(match.group(0)))
#             if "nothing_Found" in appointments_json["appointments"]:
#                 print("No appointments found for anmeldung")
#                 exit()        
#             appointments = []
#             for appointment in appointments_json["appointments"]:
#                 appointments.append(Appointment.from_json(appointment))
#             return appointments
#         else:
#             print("JSON data not found")
#             exit()

# def notify_aachen_anmeldung(bot):
#     appointments = get_appointments()
#     grouped_appointments = defaultdict(lambda: defaultdict(set))
#     for a in appointments:
#         if "Bürgerservice Katschhof" in a.unit:
#             loc = Location.Katschhof
#             # print(f"Bürgerservice Katschhof: {a.date_time}")
#         elif "Bürgerservice Bahnhofplatz" in a.unit:
#             loc = Location.Bahnhofplatz
#             # print(f"Bürgerservice Bahnhofplatz: {a.date_time}")
#         else:
#             continue

#         date_str = str(a.date_time).split()[0]
#         month = date_str.split('-')[1]
        
#         # Store in grouping dictionary
#         grouped_appointments[loc][month].add(date_str)

#     for location, months in grouped_appointments.items():
#         for month, dates in months.items():
#             channel_id = get_channel_id(location, month)
#             sorted_dates = sorted(dates)
#             date_list = ", ".join(sorted_dates)        
#             print(f"Send to channel {channel_id}: Available appointments at {location.value}\n{date_list}")
#             an_link = "https://stadt-aachen.saas.smartcjm.com/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34&wsid=d68ff95f-e3bd-45d2-ad8a-bc98a6e8879c&lang=de"
#             text = f"Available appointments at {location.value}\n{date_list}"
#             text = text.replace(".", "\.").replace("-", "\-")
#             text = f"{text}\n[🔥 Book Now\!]({an_link})"
#             bot.send_message(chat_id=channel_id, text=text)


# # notify_aachen_anmeldung(None)
#     # for a in sorted(get_appointments(), key=(lambda x : x.date_time)):
#     #     print(a)

# # Date: 2025-05-14 14:10:00+02:00, Unit:  Bürgerservice Bahnhofplatz, Duration: 5 minutes
# # Date: 2025-04-14 08:20:00+02:00, Unit: Bezirksamt Aachen Brand, Duration: 10 minutes
# # Date: 2025-05-16 10:45:00+02:00, Unit:  Bürgerservice Katschhof, Duration: 10 minutes
# # Date: 2025-05-16 10:50:00+02:00, Unit:  Bürgerservice Katschhof, Duration: 10 minutes


# TODO It works locally, but something wrong with cloudfare, already tried github action and render, cannot bypass, may need to use selenium.
import cloudscraper
import logging
import re
import json
from html import unescape
from datetime import datetime
from collections import defaultdict
from utils import get_channel_id, Location
import telegram
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Appointment:
    def __init__(self, date_time, unit, duration, link):
        self.date_time: datetime = date_time
        self.unit = unit
        self.duration = duration
        self.link = link

    def __str__(self):
        return f"Date: {self.date_time}, Unit: {self.unit}, Duration: {self.duration} minutes"
    
    def __repr__(self):
        return f"Date: {self.date_time}, Unit: {self.unit}, Duration: {self.duration} minutes"

    @staticmethod
    def from_json(json_data):                                
        datetime_str = json_data["datetime_iso86001"]
        if len(datetime_str) > 26:  # Check if microseconds part has more than 6 digits
            datetime_str = datetime_str[:26] + datetime_str[26+1:]  # Truncate the extra digit
        
        return Appointment(
            datetime.fromisoformat(datetime_str),
            json_data["unit"],
            json_data["duration"],
            "https://stadt-aachen.saas.smartcjm.com" + json_data["link"]
        )

def get_appointments() -> list[Appointment]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://stadt-aachen.saas.smartcjm.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'DNT': '1',
    }
    domain = "https://stadt-aachen.saas.smartcjm.com"    
    logging.info("Getting wsid token")

    # Replace requests with cloudscraper
    # scraper = cloudscraper.create_scraper()
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        },
        delay=10,  # Add delay to mimic human behavior
        debug=False
    )
    session = scraper
    session.headers.update(headers)
    initial_url = domain + "/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34"
    response = session.get(initial_url, allow_redirects=False)

    logging.info(response)
    logging.info(response.headers)    
    if response.status_code != 302:        
        logging.error("Couldn't get wsid token. Status code: %d", response.status_code)
        exit()
    
    base_url = domain + response.headers["Location"]
    response2 = session.get(base_url, allow_redirects=False)

    pattern = (r"^(?:.*)<input type='hidden' id='RequestVerificationToken' name='__RequestVerificationToken' value='("
               r".*?)' />")
    match = re.search(pattern, response2.text, flags=re.MULTILINE)
    if match:
        form_token = match.group(1)
    else:
        print("Couldn't get form token")
        exit()

    form_data = "&action_type=&steps=serviceslocationssearch_resultsbookingfinish&step_current=services&step_current_index=0&step_goto=%2B1&services=&services=7bee4872-ba56-4070-9f6d-f45afdf491cb&service_7bee4872-ba56-4070-9f6d-f45afdf491cb_amount=1"
    # test
    # form_data = '&action_type=&steps=serviceslocationssearch_resultsbookingfinish&step_current=services&step_current_index=0&step_goto=%2B1&services=&services=116df7ba-ea4e-4cf0-b6b9-0723d37ef78d&service_116df7ba-ea4e-4cf0-b6b9-0723d37ef78d_amount=1&services=e2da5155-fe39-4a21-bc07-46cd16a824b9&service_e2da5155-fe39-4a21-bc07-46cd16a824b9_amount=0&services=167f484a-f65d-49cf-8925-dca7be061b36&service_167f484a-f65d-49cf-8925-dca7be061b36_amount=0&services=c4e3989a-e5c0-418f-9198-80493c707ec2&service_c4e3989a-e5c0-418f-9198-80493c707ec2_amount=0&services=fae35b04-9e00-4f73-b1f2-e1ad0a17a87e&service_fae35b04-9e00-4f73-b1f2-e1ad0a17a87e_amount=0&services=10b657a5-0e90-44bc-b72a-2cfec873f6d2&service_10b657a5-0e90-44bc-b72a-2cfec873f6d2_amount=0&services=00dc099a-f550-4481-b1da-48321aea5224&service_00dc099a-f550-4481-b1da-48321aea5224_amount=0&services=c4893630-52bf-4f77-b728-f09407c728e3&service_c4893630-52bf-4f77-b728-f09407c728e3_amount=0&services=0886bc62-fa3e-405a-af63-8054959e85b3&service_0886bc62-fa3e-405a-af63-8054959e85b3_amount=0&services=716e4507-b635-4dca-8b86-00c10da3d3f9&service_716e4507-b635-4dca-8b86-00c10da3d3f9_amount=0&services=74575ac4-9906-4ad5-a8af-aa556e526704&service_74575ac4-9906-4ad5-a8af-aa556e526704_amount=0&services=0f3887e6-be79-46fc-a5b1-af02110d91be&service_0f3887e6-be79-46fc-a5b1-af02110d91be_amount=0&services=d9c6e7d3-d24d-4ccf-8fd4-62ba9c05caf7&service_d9c6e7d3-d24d-4ccf-8fd4-62ba9c05caf7_amount=0&services=51d53890-e2e0-4f76-a05d-537341860a51&service_51d53890-e2e0-4f76-a05d-537341860a51_amount=0&services=a38ae120-a5a8-4fe7-a5b1-7a7a938a07db&service_a38ae120-a5a8-4fe7-a5b1-7a7a938a07db_amount=0&services=d60dc34b-8586-48bd-9feb-23bc6fa91794&service_d60dc34b-8586-48bd-9feb-23bc6fa91794_amount=0&services=07103639-8025-4df0-9772-220e84eb0af2&service_07103639-8025-4df0-9772-220e84eb0af2_amount=0&services=5e0d7cd5-8784-43f0-a3ac-b10da3d2af96&service_5e0d7cd5-8784-43f0-a3ac-b10da3d2af96_amount=0&services=7d4c84e7-fb13-45c1-97a6-185af8235b6e&service_7d4c84e7-fb13-45c1-97a6-185af8235b6e_amount=0&services=2fc984c8-70b3-439c-9dca-b77db3ad76d8&service_2fc984c8-70b3-439c-9dca-b77db3ad76d8_amount=0&services=05bdef1d-1b12-45ba-bd29-fae0d1a58ed7&service_05bdef1d-1b12-45ba-bd29-fae0d1a58ed7_amount=0&services=7caa3811-0ba7-4e31-841e-aa69831d7782&service_7caa3811-0ba7-4e31-841e-aa69831d7782_amount=0&services=7028a6df-7a61-40f8-a920-3ec5c9d1f969&service_7028a6df-7a61-40f8-a920-3ec5c9d1f969_amount=0&services=146c80d6-bb02-42b8-aafa-bd3e855414c9&service_146c80d6-bb02-42b8-aafa-bd3e855414c9_amount=0&services=64a30e77-8224-41e8-bee9-624464dcd860&service_64a30e77-8224-41e8-bee9-624464dcd860_amount=0&services=cc8b1d05-8cd9-4555-a666-39ed185292ba&service_cc8b1d05-8cd9-4555-a666-39ed185292ba_amount=0&services=38c66af1-44e8-4781-804d-1693e703a346&service_38c66af1-44e8-4781-804d-1693e703a346_amount=0&services=b0a3bbe1-4747-44cb-a8d3-b56a3be9fe15&service_b0a3bbe1-4747-44cb-a8d3-b56a3be9fe15_amount=0&services=b755ee1f-9df1-4a66-acfd-76b9e46b1211&service_b755ee1f-9df1-4a66-acfd-76b9e46b1211_amount=0&services=216bbe43-d673-472b-be08-fe122ee1bc2b&service_216bbe43-d673-472b-be08-fe122ee1bc2b_amount=0&services=b829df33-9df6-4bd9-b740-301df3efb643&service_b829df33-9df6-4bd9-b740-301df3efb643_amount=0&services=2db0b2e2-8f00-4aa6-a08c-44dff95cc043&service_2db0b2e2-8f00-4aa6-a08c-44dff95cc043_amount=0&services=7bee4872-ba56-4070-9f6d-f45afdf491cb&service_7bee4872-ba56-4070-9f6d-f45afdf491cb_amount=0&services=d1a00eaf-f73b-4e98-ac2f-568b2d9c16c1&service_d1a00eaf-f73b-4e98-ac2f-568b2d9c16c1_amount=0&services=4a561c29-1721-4e27-b470-1a3265bf93ab&service_4a561c29-1721-4e27-b470-1a3265bf93ab_amount=0&services=1d2f6113-811d-4643-87d0-ebd3a7780959&service_1d2f6113-811d-4643-87d0-ebd3a7780959_amount=0&services=4c62d7e6-1c14-44a2-a8ea-3dac4b680023&service_4c62d7e6-1c14-44a2-a8ea-3dac4b680023_amount=0&services=98025ae5-88a5-4e8e-ac53-6ddd11231543&service_98025ae5-88a5-4e8e-ac53-6ddd11231543_amount=0&services=b98b99d3-aa3b-4af8-99c6-ed9580de78aa&service_b98b99d3-aa3b-4af8-99c6-ed9580de78aa_amount=0&services=bab4aab0-4572-4ae6-9b81-5db9f7ea75df&service_bab4aab0-4572-4ae6-9b81-5db9f7ea75df_amount=0&services=3f6be2ff-0acf-477f-afd7-1bc3400dfa0e&service_3f6be2ff-0acf-477f-afd7-1bc3400dfa0e_amount=0&services=f8a495fc-90bf-4e96-a776-802483d2b542&service_f8a495fc-90bf-4e96-a776-802483d2b542_amount=0&services=602452fb-fdcf-49ad-a3f6-48dba4af97db&service_602452fb-fdcf-49ad-a3f6-48dba4af97db_amount=0&services=9968f6be-36d5-494e-846d-cdcb0388b221&service_9968f6be-36d5-494e-846d-cdcb0388b221_amount=0'
    form_data = "__RequestVerificationToken=" + form_token + form_data

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    session.post(base_url, data=form_data, headers=headers, allow_redirects=False)

    url = base_url.split("?")[0] + "search_result?search_mode=all&" + base_url.split("?")[1]
    response4 = session.get(url, allow_redirects=False)

    pattern = r"(?<=<div id=\"json_appointment_list\">).*?(?=</div>)"
    match = re.search(pattern, response4.text, flags=re.DOTALL)

    if match:
        appointments_json = json.loads(unescape(match.group(0)))
        if "nothing_Found" in appointments_json["appointments"]:
            print("No appointments found for anmeldung")
            exit()        
        appointments = []
        for appointment in appointments_json["appointments"]:
            appointments.append(Appointment.from_json(appointment))
        return appointments
    else:
        print("JSON data not found")
        exit()

def notify_aachen_anmeldung(bot):
    appointments = get_appointments()
    grouped_appointments = defaultdict(lambda: defaultdict(set))
    for a in appointments:
        if "Bürgerservice Katschhof" in a.unit:
            loc = Location.Katschhof
        elif "Bürgerservice Bahnhofplatz" in a.unit:
            loc = Location.Bahnhofplatz
        else:
            continue

        date_str = str(a.date_time).split()[0]
        month = date_str.split('-')[1]
        
        grouped_appointments[loc][month].add(date_str)

    for location, months in grouped_appointments.items():
        for month, dates in months.items():
            channel_id = get_channel_id(location, month)
            sorted_dates = sorted(dates)
            date_list = ", ".join(sorted_dates)        
            print(f"Send to channel {channel_id}: Available appointments at {location.value}\n{date_list}")
            an_link = "https://stadt-aachen.saas.smartcjm.com/m/buergerservice/extern/calendar/?uid=15940648-b483-46d9-819e-285707f1fc34&wsid=d68ff95f-e3bd-45d2-ad8a-bc98a6e8879c&lang=de"
            text = f"Available appointments at {location.value}\n{date_list}"
            text = text.replace(".", "\.").replace("-", "\-")
            text = f"{text}\n[🔥 Book Now\!]({an_link})"
            bot.send_message(chat_id=channel_id, text=text)

if __name__ == "__main__":
    TOKEN = os.environ['TG_TOKEN']
    bot = telegram.Bot(token=TOKEN)
    notify_aachen_anmeldung(bot)
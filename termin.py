import requests
import logging
import bs4

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def aachen_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    
    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/'
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_3 = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?mdt=52&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=0&cnc-202=0&cnc-189=0&cnc-203=0&cnc-196=0&cnc-200=0&cnc-199=0&cnc-188=0&cnc-186=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-185=0&cnc-187=0&cnc-190=0&cnc-195=0&cnc-191=1&cnc-194=0&cnc-197=0&cnc-192=0"
    url_4 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-191=1&loc=28'

    res_1 = requests.get(url_1, headers=headers)
    res_2 = requests.get(url_2, headers=headers,cookies=res_1.cookies)
    res_3 = requests.get(url_3, headers=headers,cookies=res_2.cookies)
    res_4 = requests.get(url_4, headers=headers,cookies=res_3.cookies)
    
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

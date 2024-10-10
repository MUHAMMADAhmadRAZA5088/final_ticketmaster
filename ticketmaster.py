import requests
import urllib.parse
import json
import os
import pandas as pd
import time
from dotenv import load_dotenv
from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime

def convert_json(fine_name, link):
    try:
        with open(f'{fine_name}', 'r') as file:
            data_list = json.load(file)
        
        data_list.append(link)
        data_list = list(set(data_list))
        # JSON string se read karna
        with open(f'{fine_name}', 'w') as file:
            json.dump(data_list, file)

    except:
        with open('/home/ubuntu/livenation_ticketmaster/'+f'{fine_name}', 'r') as file:
            data_list = json.load(file)
        data_list.append(link)
        data_list = list(set(data_list))
        # JSON string se read karna
        with open('/home/ubuntu/livenation_ticketmaster/'+f'{fine_name}', 'w') as file:
            json.dump(data_list, file)

# csv convert data
def csv_convert(soup, type_event , data , target_url):
    new_data = {
        'Event Title': [],
        'URL': [],
        'status' : []
            }

    event_title = soup.find('h1', class_='sc-1eku3jf-14 ghwxrG').text
    new_data['Event Title'].append(event_title)
    new_data["URL"].append(target_url)
    new_data["status"].append(type_event)
    df_new = pd.DataFrame(new_data)
    df_new.to_csv('ticketmaster1.csv', mode='a', header=False, index=False)

    return data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"]

# Load environment variables
def load_env_variables():
    load_dotenv()
    return os.getenv("PROXY_API_KEY")

# Check if the array has elements and return the first if exists
def return_if_exist(arr):
    if len(arr):
        return arr[0]
    return ""

# Generate the API base URL with the provided token and target URL
def generate_api_url(token, target_url):
    api_base_url = "http://api.scrape.do?token={}&url={}&super=true&render=true"
    return api_base_url.format(token, urllib.parse.quote(target_url))

# Generate the proxy URL with the provided token
def generate_proxy_url(token):
    return "http://{}:@proxy.scrape.do:8080".format(token)

# Define the headers for the HTTP request
def get_headers():
    return {
        'sd-x-tmlangcode': 'en-us',
        'sd-x-tmplatform': 'global',
        'sd-x-tmregion': '200'
    }

# Make an HTTP GET request to the provided URL
def make_request(url, headers):
    return requests.request("GET", url, headers=headers)

livenation_link = []
bad_link = []
ticketmaster_link = []
ticketmaster_all_url = []

# ticketmaster ca
# ticketmaster ca
def filter_url_ticketmaster_ca(target_url):
    retries = 3

    for i in range(retries):
        try:
            targetUrl = urllib.parse.quote(target_url)
            url = f"http://api.scrape.do?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={targetUrl}"
            response = requests.request("GET", url )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                        
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            try :
                                generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                            except :
                                generalinfo = "key error"

                            current_date = datetime.now().date()
                            target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                            if current_date < target_date and generalinfo != "":
                                ticketmaster_link.append(target_url)
                                convert_json('website_ticketmaster_link_ticketmaster.json', target_url)
                                return "success_value"
                                    
                    except:
                        return "No Value"
                else: 
                    return "no link"
            else:       
                if i < retries - 1:  # Don't retry on the last attempt
                    print(f"attempt {i + 1}")
                    time.sleep(10)
                else:
                    pass  
        
        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                print(f"attempt {i + 1}")
                time.sleep(10)
            else:
                pass

# ticketmaster
def filter_url_ticketmaster(target_url):
    retries = 3

    for i in range(retries):
        try:
            url = f"http://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={target_url}"
            response = requests.request("GET", url )
            if response.status_code == 200: 
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            try :
                                generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                            except :
                                generalinfo = "key error"

                            current_date = datetime.now().date()
                            target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                            if current_date < target_date and generalinfo != "":
                                type_event = "coming event"
                                ticketmaster_link.append(target_url)
                                convert_json('website_ticketmaster_link_ticketmaster.json', target_url)

                    except:
                        return "No link"
                else:
                    return "No link"
            else:
                if i < retries - 1:  # Don't retry on the last attempt
                    print(f"attempt {i + 1}")
                    time.sleep(10)
                else:
                    pass


        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                print(f"attempt {i + 1}")
                time.sleep(10)
            else:
                pass

#  livenation
def filter_url_livenation(targetUrl, max_retries=5, delay=10):

    for attempt in range(max_retries):
        # target_Url = urllib.parse.quote(targetUrl)
        try:
            url = f"https://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={targetUrl}"
            response = requests.request("GET", url )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            livenation_link.append(target_url)
                            convert_json('website_ticketmaster_link_livenation_.json', target_url)
                            return data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"]
                    except:
                        return "No Value"           
                else:
                    return "No link"
            else:
                print(f"attempt {attempt + 1}")
                if attempt < 5 :
                    time.sleep(10)
                else:
                    pass
                
        except requests.exceptions.ConnectionError:
            print(f"attempt {attempt + 1}")
            if attempt < 5 :
                time.sleep(10)
            else:
                pass


# Extract the seed value from the HTML response
def extract_seed(response):
    root = html.fromstring(response.content)
    return return_if_exist(root.xpath("//div[@id='projects_list']/@data-seed"))

# Execute another Python script
def execute_script(script_name):
    with open(script_name) as file:
        exec(file.read())

def save_to_json(listing_urls, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(listing_urls, json_file)

def get_lxml(token, url):
    url = generate_api_url(
        token, url)

    headers = get_headers()
    response = make_request(url, headers)
    if response.status_code != 400:
        return html.fromstring(response.content)
    
def main():
    token = "4452cbd7342d4a36971719b194897d692073b3c06af"
    concerts = [
        '/discover/concerts?classificationId=KnvZfZ7vAve',
        '/discover/concerts?classificationId=KnvZfZ7vAeA',
        '/discover/concerts?classificationId=KnvZfZ7vAvl',
        '/discover/concerts?classificationId=KnvZfZ7vAeF',
        '/discover/concerts?classificationId=KnvZfZ7vAvd',
        '/discover/concerts?classificationId=KnvZfZ7vAvk',
        '/discover/concerts?classificationId=KnvZfZ7vAeJ',
        '/discover/concerts?classificationId=KnvZfZ7vAv6',
        '/discover/concerts?classificationId=KnvZfZ7vAvF',
        '/discover/concerts?classificationId=KnvZfZ7vAva',
        '/discover/concerts?classificationId=KnvZfZ7vAv1',
        '/discover/concerts?classificationId=KnvZfZ7vAvJ',
        '/discover/concerts?classificationId=KnvZfZ7vAvE',
        '/discover/concerts?classificationId=KnvZfZ7vAJ6',
        '/discover/concerts?classificationId=KnvZfZ7vAvI',
        '/discover/concerts?classificationId=KnvZfZ7vAvt',
        '/discover/concerts?classificationId=KnvZfZ7vAvn',
        '/discover/concerts?classificationId=KnvZfZ7vAev',
        '/discover/concerts?classificationId=KnvZfZ7vAee',
        '/discover/concerts?classificationId=KnvZfZ7vAed',
        '/discover/concerts?classificationId=KnvZfZ7vAe7',
        'discover/concerts?classificationId=KnvZfZ7vAvv'
         ]

    for concert in concerts:
        try:
            root = get_lxml(token, f"https://www.ticketmaster.com/{concert}")
            data = json.loads(root.xpath("//script[@id='__NEXT_DATA__']")[0].text)
            events = data.get("props", "").get("pageProps", "").get("eventsJsonLD", "")[0]
            print(concert)
            if events:
                for link in events:
                  
                    link = link["url"]

                    if "ticketmaster.com" in link and "ticketmaster.com." not in link:
                        data = filter_url_ticketmaster(link)
                    elif "concerts.livenation.com" in link:
                        data = filter_url_livenation(link)
                    elif "ticketmaster.ca" in link:
                        data = filter_url_ticketmaster_ca(link)
                    else:
                        bad_link.append(link)
                        convert_json('bad_link.json', link)
                    ticketmaster_all_url.append(link)
                    convert_json('all_url.json', link)
                    print(f"bad_url = {len(set(bad_link))} and livenation_concert  = {len(set(livenation_link))} and ticketmaster = {len(set(ticketmaster_link))} and all_website_link.json ={len(set(ticketmaster_all_url))}")

                for i in range(1,50):
                    try:
                        concert1 = concert.replace("/discover/concerts?classificationId=","")
                        concert1 = concert1.replace("discover/concerts?classificationId=","")
                        encoded_url = urllib.parse.quote(f"https://www.ticketmaster.com/api/search/events/category/{concert1}?page={i}&region=200")
                        url = f"http://api.scrape.do?token=4452cbd7342d4a36971719b194897d692073b3c06af&url={encoded_url}&extraHeaders=true"
                        payload = {}
                        headers = {
                        'sd-x-tmlangcode': 'en-us',
                        'sd-x-tmplatform': 'global',
                        'sd-x-tmregion': '200'
                        }
                        response = requests.request("GET", url, headers=headers, data=payload)
                        data = json.loads(response.text)               
                        if response.status_code != 400:               
                            for data in data["events"]:      
                                link = data["url"]
                                        
                                if "ticketmaster.com" in link and "ticketmaster.com." not in link:
                                    data = filter_url_ticketmaster(link)
                                elif "concerts.livenation.com" in link:
                                    data = filter_url_livenation(link)
                                elif "ticketmaster.ca" in link:
                                    data = filter_url_ticketmaster_ca(link)
                                else:
                                    bad_link.append(link)
                                    convert_json('bad_link.json', link)
                                ticketmaster_all_url.append(link)
                                convert_json('all_url.json', link)
                                print(f"bad_url = {len(set(bad_link))} and livenation_concert  = {len(set(livenation_link))} and ticketmaster = {len(set(ticketmaster_link))} and all_website_link.json ={len(set(ticketmaster_all_url))}")

                    except Exception as ex:
                        print(ex)
        except Exception as ex:
            print(ex)    

if __name__ == "__main__":
    main()

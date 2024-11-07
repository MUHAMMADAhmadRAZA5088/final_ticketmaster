import json
import os

empty=[]
for data in ["all_url.json","bad_link.json","website_ticketmaster_link_livenation.json","website_ticketmaster_link_ticketmaster.json"]:
    try:
        with open(f'{data}', 'w') as file:
            json.dump(empty, file)

    except:
        with open('/home/ubuntu/livenation_ticketmaster/'+f'data', 'w') as file:
            json.dump(empty, file)

print("All JSON files will now be converted into empty JSON files.")
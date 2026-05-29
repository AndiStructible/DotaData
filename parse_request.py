from functions import post_parse_request
import json
import time
from datetime import datetime

BASE_URL = "https://api.opendota.com/api"
match_id = 8796335304
#parse = post_parse_request(BASE_URL,match_id)
#print(parse)

with open("public_all_pick_data_2.json", "r") as f:
    match_ids = json.load(f)

counter = 0

for match in match_ids:
    if counter <20:
        counter += 1
        continue
        

    response = post_parse_request(BASE_URL,match_id)
    counter += 1
    print(f'parse request for {match}')
    print(response)
    print(datetime.now())
    print(counter)
    time.sleep(20)


import json 
from functions import get_match, all_party_size_one, gold_total_per_minute, xp_total_per_minute, wards_placed_by_minute, towers_destroyed_by_minute, get_first_blood
import time 
import os


BASE_URL = "https://api.opendota.com/api"
with open("public_all_pick_data.json", "r") as f:
    match_ids = json.load(f)
all_processed_matches = []
minute = 10
counter = 0
print(match_ids)
for match_id in match_ids:
    processed_match = {}
    if counter < 113:
        counter += 1
        continue

    parsed_match = get_match(BASE_URL=BASE_URL, match_id=match_id)    
    if parsed_match.get('teamfights'):
        print("all fine")
    else:
        print("not parsed?")
        continue
    if parsed_match['duration'] < 660:
        # 660 equals to minute 110 ingame 
        print("Not long enough")
        continue
    elif  parsed_match['game_mode'] != 22:
        #22 is Ranked All Pick Game Mode 
        print("Stupid Game Mode")
        continue
    elif  parsed_match['patch'] != 60:
        # 60 is 7.41b
        print("Wrong Patch")
        continue
    elif not all_party_size_one(parsed_match):
        # No parties shall be involved to ensure MMR between players is close 
        print("Parties involved")
        continue
    processed_match['match_id'] = parsed_match['match_id']
    processed_match['radiant_win'] = parsed_match['radiant_win']

    processed_match['duration'] = parsed_match['duration']

    radiant_gold, dire_gold = gold_total_per_minute(parsed_match, minute)
    processed_match['radiant_gold'] = radiant_gold 
    processed_match['dire_gold'] = dire_gold 
    processed_match['radiant_gold_div'] = radiant_gold - dire_gold
        
    radiant_xp, dire_xp = xp_total_per_minute(parsed_match, minute)
    processed_match['radiant_xp'] = radiant_xp 
    processed_match['dire_xp'] = dire_xp 
    processed_match['radiant_xp_div'] = radiant_xp - dire_xp

    radiant_wards, dire_wards = wards_placed_by_minute(parsed_match, minute)
    processed_match['radiant_wards'] = radiant_wards
    processed_match['dire_wards'] = dire_wards
    processed_match['radiant_wards_div'] = radiant_wards - dire_wards

    radiant_tower, dire_tower = towers_destroyed_by_minute(parsed_match, minute)
    processed_match['radiant_towers_destroyed'] = radiant_tower
    processed_match['dire_towers_destroyed'] = dire_tower
    processed_match['radiant_towers_destroyed_div'] = radiant_tower - dire_tower

    processed_match['radiant_first_blood'] = get_first_blood(parsed_match)

    time.sleep(10)
    counter += 1
    print(counter)
    print(processed_match)

    all_processed_matches.append(processed_match)

    if counter == 150:
        break
    


filename = "match_details.json"

# Check if file exists
if os.path.exists(filename):
    # Load existing data
    with open(filename, "r") as f:
        data = json.load(f)
    
    # Append new entry
    for match in all_processed_matches:


        # Check if item already exists (by id)
        exists = any(match["match_id"] == new_match["match_id"] for new_match in data)

        if not exists:
            data.append(match)
            print("Added new item")
        else:
            print("Item already exists, skipping")


else:
    # Create new list with the first entry
    data = []
    for match in all_processed_matches:
        data.append(match)

# Write updated data back to file
with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print("Done.")



from functions import get_latest_100_parsed_matches, wards_placed_by_minute, towers_destroyed_by_minute, gold_total_per_minute, xp_total_per_minute, get_match, write_to_file, write_json, all_party_size_one, get_radiant_xp_adv_min10
from collections import Counter
import time
import csv 
import os


BASE_URL = "https://api.opendota.com/api"
match_id = 	8769904228 #start ID: 8769900228
match_list = get_latest_100_parsed_matches(BASE_URL, match_id)
#print(match_list)
#print(get_match(BASE_URL, match_id))
match_json_data = get_match(BASE_URL, match_id)
write_json("match.json", match_json_data)
minute = 9 # meaning minute 10 but time tracking starts at 0 need to check from real game what about -1?
#client = opendota.OpenDota()
processed_match = {}
# print(all_party_size_one(match=match_json_data))
# print(get_radiant_xp_adv_min10)
# print(xp_total_per_minute(match_json_data, minute))
useful_match_id_list = []
# Initialize the API-connection object
cleaned_match_data = []

for match_id in match_list:
    time.sleep(0.1)
    print(f"Checking match {match_id['match_id']}")
    try:
        match = get_match(BASE_URL, match_id['match_id'])
        processed_match = {}
    except Exception as e:
        print(f"Error fetching {match_id['match_id']}: {e}")
        # optional: skip, retry, or log
        continue
    if not match:
        print(f'no parsed match found here')
        continue
    isParty = all_party_size_one(match)
    if match['duration'] < 600:
        # 600 equals to 10 minutes 
        print("Not long enough")
    elif  match['game_mode'] != 22:
        #22 is Ranked All Pick Game Mode 
        print(f'{match['game_mode']}')
        print("Stupid Game Mode")
    elif  match['patch'] != 60:
        # 60 is 7.41b
        print("Wrong Patch")
    elif not isParty:
        # No parties shall be involved to ensure MMR between players is close 
        print(isParty)
        print("Parties involved")
    else: 
        processed_match['match_id'] = match_id['match_id']
        processed_match['radiant_win'] = match['radiant_win']

        processed_match['duration'] = match['duration']

        radiant_gold, dire_gold = gold_total_per_minute(match, minute)
        processed_match['radiant_gold'] = radiant_gold 
        processed_match['dire_gold'] = dire_gold 
        processed_match['radiant_gold_div'] = radiant_gold - dire_gold
        
        radiant_xp, dire_xp = xp_total_per_minute(match, minute)
        processed_match['radiant_xp'] = radiant_xp 
        processed_match['dire_xp'] = dire_xp 
        processed_match['radiant_xp_div'] = radiant_xp - dire_xp

        radiant_wards, dire_wards = wards_placed_by_minute(match, minute)
        processed_match['radiant_wards'] = radiant_wards
        processed_match['dire_wards'] = dire_wards
        processed_match['radiant_wards_div'] = radiant_wards - dire_wards

        radiant_tower, dire_tower = towers_destroyed_by_minute(match, minute)
        processed_match['radiant_towers_destroyed'] = radiant_tower
        processed_match['dire_towers_destroyed'] = dire_tower
        processed_match['radiant_towers_destroyed_div'] = radiant_tower - dire_tower

        useful_match_id_list.append(match_id)
        cleaned_match_data.append(processed_match)
        print(f"useful match found!!!")
        #print(f'{processed_match}')

print(len(useful_match_id_list))

# with open("output.csv", "w", newline="") as f:
#     writer = csv.DictWriter(f, fieldnames=cleaned_match_data[0].keys())
#     writer.writeheader()
#     writer.writerows(cleaned_match_data)


filename = "output.csv"
file_exists = os.path.isfile(filename)

with open(filename, "a", newline="") as f:
    # Use the keys from the first dict, same as your original code
    fieldnames = cleaned_match_data[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Only write header if file did NOT exist
    if not file_exists:
        writer.writeheader()

    # Append all rows
    writer.writerows(cleaned_match_data)
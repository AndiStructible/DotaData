from functions import get_public_matches, write_json
import os
import json 
import requests
#this file creates a list of match ids of matches that are all pick ranked in divine or higher rank (avg_rank_tier higher than 70)

match_id = 8796332762
BASE_URL = "https://api.opendota.com/api"
min_rank = 70 #70 is Divine I, 71 is Divine II etc. 
matches_json_data = get_public_matches(BASE_URL=BASE_URL, match_id=match_id, min_rank= min_rank)
filtered_matches_json_data = []
# print(matches_json_data)
# filename = "public_divine_matches.json"

with open("public_divine_matches_2.json", "r") as f:
    matches = json.load(f)
count= 0
for match in matches:
    count+=1
    if match['game_mode'] == 22:
        filtered_matches_json_data.append(match)
    else: 
        print("stupid game mode")

print(len(filtered_matches_json_data))
print(count)


filename = "public_all_pick_data_2.json"

# Check if file exists
if os.path.exists(filename):
    # Load existing data
    with open(filename, "r") as f:
        data = json.load(f)

    # Append new entry
    for match in filtered_matches_json_data:
        data.append(match['match_id'])

else:
    # Create new list with the first entry
    data = []
    for match in filtered_matches_json_data:
        if match['match_id'] not in data:
            data.append(match['match_id'])
        else:
            print('duplicate')

# Write updated data back to file
with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print("Done.")

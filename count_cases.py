import json

with open("match_details_2.json", "r") as f:
    match_ids = json.load(f)


count = sum(1 for match in match_ids if match.get("radiant_win") is True)

print(count)
print(len(match_ids))
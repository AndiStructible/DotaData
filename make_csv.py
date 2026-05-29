# import json
# import csv

# # Input and output file paths
# json_file = "match_details_2.json"
# csv_file = "match_details_output.csv"

# # Load JSON data
# with open(json_file, "r", encoding="utf-8") as f:
#     data = json.load(f)

# # If the JSON is a dict, convert to list of dicts
# if isinstance(data, dict):
#     # Use the values as rows
#     data = list(data.values())

# # Extract CSV headers from keys of first item
# headers = data[0].keys()

# # Write CSV
# with open(csv_file, "w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(data)

# print("CSV file created:", csv_file)



import json
import csv

# Input and output file paths
json_file = "match_details_2.json"
csv_file = "match_details_output.csv"

# Load JSON data
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# If the JSON is a dict, convert to list of dicts
if isinstance(data, dict):
    data = list(data.values())

# Filter: keep only rows where radiant_first_blood is 0 or 1
filtered_data = [
    row for row in data
    if "radiant_first_blood" in row and row["radiant_first_blood"] in (0, 1)
]
# Radiant win percentage for filtered rows
filtered_total = len(filtered_data)
filtered_radiant_wins = sum(
    1 for row in filtered_data if row.get("radiant_win") is True
)

filtered_radiant_win_percentage = (
    (filtered_radiant_wins / filtered_total) * 100
    if filtered_total > 0 else 0
)

print("Filtered matches:", filtered_total)
print("Filtered radiant wins:", filtered_radiant_wins)
print("Filtered radiant win %:", round(filtered_radiant_win_percentage, 2))

# Extract CSV headers from keys of first item
headers = filtered_data[0].keys()

# Write CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(filtered_data)

print("CSV file created:", csv_file)

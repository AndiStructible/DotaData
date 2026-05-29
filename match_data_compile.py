import csv
import json
import os
import time
from functions import (
    get_latest_100_parsed_matches, get_match, write_json,
    all_party_size_one, all_players_divine,
    gold_total_per_minute, xp_total_per_minute,
    wards_placed_by_minute, towers_destroyed_by_minute,
    get_first_blood
)

BASE_URL = "https://api.opendota.com/api"
PARSED_FILE = "parsed_matches.json"
DETAILS_FILE = "match_details_2.json"
CSV_FILE = "match_details_2.csv"
NUM_BATCHES = 5
MINUTE = 10


def load_existing(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def write_csv(filename, data):
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def process_match(parsed_match):
    """Filters and extracts features from a full match object. Returns None if unusable."""
    if not parsed_match.get("teamfights"):
        print("  Not parsed")
        return None
    if parsed_match["duration"] < 660:
        print("  Too short")
        return None
    if parsed_match["game_mode"] != 22:
        print("  Wrong game mode")
        return None
    if parsed_match["patch"] != 60:
        print("  Wrong patch")
        return None
    if not all_party_size_one(parsed_match):
        print("  Parties involved")
        return None
    if not all_players_divine(parsed_match):
        print("  Below divine rank")
        return None

    first_blood = get_first_blood(parsed_match)
    if first_blood not in (0, 1):
        print("  Missing first blood event")
        return None

    radiant_gold, dire_gold = gold_total_per_minute(parsed_match, MINUTE)
    radiant_xp, dire_xp = xp_total_per_minute(parsed_match, MINUTE)
    radiant_wards, dire_wards = wards_placed_by_minute(parsed_match, MINUTE)
    radiant_tower, dire_tower = towers_destroyed_by_minute(parsed_match, MINUTE)

    return {
        "match_id":                    parsed_match["match_id"],
        "radiant_win":                 parsed_match["radiant_win"],
        "duration":                    parsed_match["duration"],
        "radiant_gold":                radiant_gold,
        "dire_gold":                   dire_gold,
        "radiant_gold_div":            radiant_gold - dire_gold,
        "radiant_xp":                  radiant_xp,
        "dire_xp":                     dire_xp,
        "radiant_xp_div":              radiant_xp - dire_xp,
        "radiant_wards":               radiant_wards,
        "dire_wards":                  dire_wards,
        "radiant_wards_div":           radiant_wards - dire_wards,
        "radiant_towers_destroyed":    radiant_tower,
        "dire_towers_destroyed":       dire_tower,
        "radiant_towers_destroyed_div": radiant_tower - dire_tower,
        "radiant_first_blood":         first_blood,
    }


def main():
    all_match_ids = load_existing(PARSED_FILE)
    processed_matches = load_existing(DETAILS_FILE)
    existing_ids = {m["match_id"] for m in processed_matches}

    if all_match_ids:
        match_id = all_match_ids[-1]["match_id"]
        print(f"Resuming ID fetch from match_id {match_id}")
    else:
        match_id = 8796335304
        print("Starting fresh from latest matches")

    for batch in range(NUM_BATCHES):
        print(f"\nFetching batch {batch + 1}/{NUM_BATCHES} (less_than_match_id={match_id})...")
        id_batch = get_latest_100_parsed_matches(BASE_URL, match_id)

        if not id_batch:
            print("No more matches returned. Stopping.")
            break

        all_match_ids.extend(id_batch)
        write_json(PARSED_FILE, all_match_ids)
        match_id = id_batch[-1]["match_id"]

        for entry in id_batch:
            mid = entry["match_id"]
            if mid in existing_ids:
                print(f"  {mid} already processed, skipping")
                continue

            time.sleep(1)
            print(f"  Querying match {mid}...")
            parsed_match = get_match(BASE_URL, mid)

            result = process_match(parsed_match)
            time.sleep(1)

            if result:
                processed_matches.append(result)
                existing_ids.add(mid)
                write_json(DETAILS_FILE, processed_matches)
                write_csv(CSV_FILE, processed_matches)
                print(f"  Saved: {result}")

    print(f"\nDone. Processed matches saved: {len(processed_matches)}")


if __name__ == "__main__":
    main()

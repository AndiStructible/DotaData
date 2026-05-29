import requests
import json

def get_latest_100_parsed_matches(BASE_URL, match_id):
    """
    Returns the latest parsed matches from OpenDota (max 100).
    """
    response = requests.get(
        f"{BASE_URL}/parsedMatches?less_than_match_id={match_id}",
        timeout=10
    )
    response.raise_for_status()
    return response.json()

def get_match(BASE_URL, match_id):
    response = requests.get(
        f"{BASE_URL}/matches/{match_id}",
        timeout=10
    )
    print(f'ran match id: {match_id}')
    response.raise_for_status()

    return response.json()

def get_public_matches(BASE_URL, match_id, min_rank):
    #Get 100 random match ids from Divine (70+) tier 
    response = requests.get(
        f"{BASE_URL}/parsedMatches?less_than_match_id{match_id}&min_rank={min_rank}",
        timeout=10
    )
    response.raise_for_status()
    return response.json()

def post_parse_request(BASE_URL, match_id):
    response = requests.post(
        f"{BASE_URL}/request/{match_id}"
    )
    response.raise_for_status()
    return response.json()

def all_party_size_one(match) -> bool:
    """
    Returns True if every player in the match has party_size = 1.
    Returns False if any player has party_size != 1 or if the field is missing.
    """
    players = match.get("players", [])
    if not players:
        return False  # no players = invalid match

    for p in players:
        # If party_size is missing or not equal to 1 → fail
        #print(p.get("party_size"))
        if p.get("party_size") != 1:
            return False

    return True

def wards_placed_by_minute(match, minute):
    cutoff_time = minute * 60

    radiant_wards = 0
    dire_wards = 0

    for player in match.get("players", []):
        team = "radiant" if player["player_slot"] < 128 else "dire"

        # Observer ward placements
        for event in player.get("obs_log", []):
            if event["time"] <= cutoff_time:
                if team == "radiant":
                    radiant_wards += 1
                else:
                    dire_wards += 1

        # Sentry ward placements
        for event in player.get("sen_log", []):
            if event["time"] <= cutoff_time:
                if team == "radiant":
                    radiant_wards += 1
                else:
                    dire_wards += 1

    return radiant_wards, dire_wards


def towers_destroyed_by_minute(match, minute):
    #returns the number of towers kills scored by the team in 
    cutoff_time = minute * 60


    radiant_destroyed = 0  #towers destroyed by radiant
    dire_destroyed = 0     # towers destroyed by dire

    for obj in match.get("objectives", []):
        if obj.get("type") != "building_kill":
            continue
        key = obj.get("key", "")
        if "tower" not in key:
            continue
        if obj.get("time", 99999) >= cutoff_time:
            continue

        # Tower belongs to Radiant
        if "goodguys" in key:
            dire_destroyed += 1

        # Tower belongs to Dire
        elif "badguys" in key:
            radiant_destroyed += 1

    return radiant_destroyed, dire_destroyed
    




def gold_total_per_minute(match, minute):
    radiant_gold = 0
    dire_gold = 0
    radiant_gold = sum(
        p["gold_t"][minute]
        for p in match["players"]
        if p["player_slot"] < 128
        )

    dire_gold = sum(
        p["gold_t"][minute]
        for p in match["players"]
        if p["player_slot"] >= 128
    )

    return radiant_gold, dire_gold

def xp_total_per_minute(match, minute):
     #README minute 10 translates in this case to 660 seconds as the array starts at 0 
    radiant_xp = 0
    dire_xp = 0
    radiant_xp = sum(
        p["xp_t"][minute]
        for p in match["players"]
        if p["player_slot"] < 128
    )

    dire_xp = sum(
        p["xp_t"][minute]
        for p in match["players"]
        if p["player_slot"] >= 128
    )

    return radiant_xp, dire_xp

def get_radiant_xp_adv_min10(match):
    """
    Returns the radiant_xp_adv value at minute 10.
    Returns None if the field is missing or too short.
    """
    xp_adv = match.get("radiant_xp_adv")
    if not isinstance(xp_adv, list):
        return None

    if len(xp_adv) <= 10:
        return None

    return xp_adv[10]

def write_to_file(filename: str, text: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def write_json(filename: str, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_first_blood(match):
    objectives = match.get("objectives", [])
    fb = None

    # Find the first blood objective
    for obj in objectives:
        if obj.get("type") == "CHAT_MESSAGE_FIRSTBLOOD":
            fb = obj
            break

    if fb is None:
        return "No first blood event found."

    killer_slot = fb.get("player_slot")
    radiant_firstblood = None
    # Radiant = 0–127, Dire = 128–255
    if killer_slot < 128:
        radiant_firstblood = 1
    else:
        radiant_firstblood = 0
    
    return radiant_firstblood

def all_players_divine(match):
    players = match.get("players")
    if not isinstance(players, list):
        return False

    for p in players:
        tier = p.get("rank_tier")

        # Private profile or missing rank_tier → fail
        if tier is None:
            return False

        if tier < 70:
            return False

    return True


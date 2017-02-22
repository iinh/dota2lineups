#

import time
import dota2api
import database_helper
import configparser

CONFIG_FILE = 'config.ini'


def load_config():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    return cfg


def main():
    cfg = load_config()
    match_file = cfg['settings']['match_file']
    with open(match_file) as file:
        matches = 0
        for match_id in file:
            lineups = get_lineups(match_id)       # Store lineups in array
            match_id = match_id.rstrip()
            matches += 1
            if matches % 100 == 0:                # Print info every 100 match
                print('Matches done: ', matches)

            winning_lineup = lineups[0]
            losing_lineup = lineups[1]

            winning_lineup_key = make_lineup_key(winning_lineup)
            losing_lineup_key = make_lineup_key(losing_lineup)

            if not database_helper.lineup_in_db(winning_lineup_key):
                database_helper.add_lineup(match_id, winning_lineup_key, True)
            else:
                print('Adding a win to: ', winning_lineup_key)
                database_helper.add_win(match_id, winning_lineup_key)

            if not database_helper.lineup_in_db(losing_lineup_key):
                database_helper.add_lineup(match_id, losing_lineup_key, False)
            else:
                print('Adding a loss to: ', winning_lineup_key)
                database_helper.add_loss(match_id, losing_lineup_key)


def get_lineups(match_id):
    cfg = load_config()
    api_key = cfg['settings']['api_key']
    api = dota2api.Initialise(api_key)
    winning_lineup = []
    losing_lineup = []
    lineups = []

    while True:
        try:
            match = api.get_match_details(match_id=match_id)
        except:
            time.sleep(1)
            print("exception")
            continue
        break

    if match["radiant_win"]:
        winning_lineup.append(match["players"][0]["hero_id"])
        winning_lineup.append(match["players"][1]["hero_id"])
        winning_lineup.append(match["players"][2]["hero_id"])
        winning_lineup.append(match["players"][3]["hero_id"])
        winning_lineup.append(match["players"][4]["hero_id"])

        losing_lineup.append(match["players"][5]["hero_id"])
        losing_lineup.append(match["players"][6]["hero_id"])
        losing_lineup.append(match["players"][7]["hero_id"])
        losing_lineup.append(match["players"][8]["hero_id"])
        losing_lineup.append(match["players"][9]["hero_id"])
    else:
        losing_lineup.append(match["players"][0]["hero_id"])
        losing_lineup.append(match["players"][1]["hero_id"])
        losing_lineup.append(match["players"][2]["hero_id"])
        losing_lineup.append(match["players"][3]["hero_id"])
        losing_lineup.append(match["players"][4]["hero_id"])

        winning_lineup.append(match["players"][5]["hero_id"])
        winning_lineup.append(match["players"][6]["hero_id"])
        winning_lineup.append(match["players"][7]["hero_id"])
        winning_lineup.append(match["players"][8]["hero_id"])
        winning_lineup.append(match["players"][9]["hero_id"])

    lineups.append(winning_lineup)
    lineups.append(losing_lineup)
    return lineups


def make_lineup_key(lineup):
    lineup.sort()
    return ".".join(str(lid) for lid in lineup)

if __name__ == "__main__":
    main()

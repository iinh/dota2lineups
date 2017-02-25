import database_helper
import json

FILE = 'my_dict_200k.json'

with open(FILE) as f:
    lineups_parsed = 0
    matches = json.load(f)
    for key, value in matches.items():
        if lineups_parsed % 10 == 0:
            print('200k - Lineups done: ', lineups_parsed)
        lineup_key = key
        wins = value['wins']
        losses = value['losses']
        winning_matches = value['winning_matches']
        losing_matches = value['losing_matches']
        if not database_helper.lineup_in_db(lineup_key):
            database_helper.add_lineup_complete(lineup_key, wins, losses,
                                                winning_matches, losing_matches)
            database_helper.update_winrate(lineup_key)
            lineups_parsed += 1

"""
This module is the database abstraction
Make sure these database credentials are stored as environment vars:
    MONGODB_URI: Link to mongodb server w/ authentication
    DATABASE_NAME: name of the database
    DATABASE_COLLECTION: the collection used.
"""

from pymongo import MongoClient
import os


def get_collection():
    """
    Get a collection from the database and return it
    """
    uri = os.environ.get('MONGODB_URI_DO')

    database = os.environ.get('DATABASE_NAME_DO')
    collection = os.environ.get('DATABASE_COLLECTION_DO')
    client = MongoClient(uri)
    db = client[database]
    collection = db[collection]
    return collection


def add_lineup_complete(lineup_key, wins, losses, winning_matches, losing_matches):
    """
    Add a new lineup to the database using a with all info parsed.
    """
    collection = get_collection()

    cmd = {'winning_matches': winning_matches,
           'losing_matches': losing_matches,
           'lineup': lineup_key,
           'wins': wins,
           'losses': losses,
           'win_rate': -1}

    collection.insert(cmd)


def add_lineup(match_id, lineup_key, win):
    """
    Add a new lineup to the database
    """
    collection = get_collection()

    if win:
        cmd = {'winning_matches': [match_id],
               'lineup': lineup_key,
               'wins': 1,
               'losses': 0,
               'win_rate': 1}
    else:
        cmd = {'losing_matches': [match_id],
               'lineup': lineup_key,
               'wins': 0,
               'losses': 1,
               'win_rate': 0}

    collection.insert(cmd)


def remove_lineup(lineup_key):
    """
    Remove a lineup from database
    """
    collection = get_collection()

    cmd = {'lineup': lineup_key}

    collection.remove(cmd)


def lineup_in_db(lineup_key):
    """
    Check if a lineup already exists in the database.
    Returns bool
    """
    collection = get_collection()
    return collection.find({'lineup': lineup_key}).count() > 0


def add_win(match_id, lineup_key):
    """
    Add a win and a match_id to an existing lineup_key in the database.
    """
    collection = get_collection()

    collection.update({'lineup': lineup_key}, {
                          '$inc': {'wins': 1},
                          '$addToSet': {'winning_matches': match_id}
                      })
    update_winrate(lineup_key)


def update_winrate(lineup_key):
    """
    Help function to update the winrate column of a lineup_key.
    Note: The winrate column does not update on its own unless you run this
    function.
    """
    collection = get_collection()
    res = collection.find_one({'lineup': lineup_key}, {'wins': 1, 'losses': 1, '_id': 0})
    win_rate = round(res['wins']/(res['wins']+res['losses']), 4)
    collection.update({'lineup': lineup_key},
                      {'$set': {'win_rate': win_rate}})


def add_loss(match_id, lineup_key):
    """
    Add a loss and a match_id to an existing lineup_key in the database.
    """
    collection = get_collection()

    collection.update({'lineup': lineup_key}, {
                          '$inc': {'losses': 1},
                          '$addToSet': {'losing_matches': match_id}
                      })
    update_winrate(lineup_key)


def get_most_wins():
    """
    Return a list of the 20 lineups with most wins.
    """
    res = []
    collection = get_collection()
    lineups = collection.find().sort('wins', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_most_losses():
    """
    Return a list of the 20 lineups with most wins.
    """
    res = []
    collection = get_collection()
    lineups = collection.find().sort('losses', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_highest_winrate():
    """
    Return a list of the 20 lineups with highest winrate
    """
    res = []
    collection = get_collection()
    lineups = collection.find().sort('win_rate', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_matches_parsed():
    """
    Get the number of matches already in the database by calculating the amount
    of total wins. This should be equal to the amount of losses and thus
    the amount of games parsed
    """
    collection = get_collection()
    res = collection.aggregate([{'$group': {
                                            '_id': 0,
                                            'matches_parsed': {
                                                '$sum': "$wins"
                                            }
                                            }
                                 }])
    for x in res:
        return x


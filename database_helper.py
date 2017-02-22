from pymongo import MongoClient
import os


def get_collection():
    uri = os.environ.get('MONGODB_URI')

    database = os.environ.get('DATABASE_NAME')
    collection = os.environ.get('DATABASE_COLLECTION')
    client = MongoClient(uri)
    db = client[database]
    collection = db[collection]
    return collection


def add_lineup(match_id, lineup_key, win):
    collection = get_collection()

    if win:
        cmd = {'match_ids': [match_id],
               'lineup': lineup_key,
               'wins': 1,
               'losses': 0,
               'win_rate': 1}
    else:
        cmd = {'match_ids': [match_id],
               'lineup': lineup_key,
               'wins': 0,
               'losses': 1,
               'win_rate': 0}

    collection.insert(cmd)


def lineup_in_db(lineup_key):
    collection = get_collection()
    return collection.find({'lineup': lineup_key}).count() > 0


def add_win(match_id, lineup_key):
    collection = get_collection()

    collection.update({'lineup': lineup_key}, {
                          '$inc': {'wins': 1},
                          '$addToSet': {'match_ids': match_id}
                      })
    update_winrate(lineup_key)


def update_winrate(lineup_key):
    collection = get_collection()
    res = collection.find_one({'lineup': lineup_key}, {'wins': 1, 'losses': 1, '_id': 0})
    win_rate = round(res['wins']/(res['wins']+res['losses']), 4)
    collection.update({'lineup': lineup_key},
                      {'$set': {'win_rate': win_rate}})


def add_loss(match_id, lineup_key ):
    collection = get_collection()

    collection.update({'lineup': lineup_key}, {
                          '$inc': {'losses': 1},
                          '$addToSet': {'match_ids': match_id}
                      })
    update_winrate(lineup_key)


def get_most_wins():
    res = []
    collection = get_collection()
    lineups = collection.find().sort('wins', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_most_losses():
    res = []
    collection = get_collection()
    lineups = collection.find().sort('losses', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_highest_winrate():
    res = []
    collection = get_collection()
    lineups = collection.find().sort('win_rate', -1).limit(20)
    for l in lineups:
        res.append(l)
    return res


def get_matches_parsed():
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


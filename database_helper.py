#!/usr/bin/python
import configparser
import psycopg2
import math
import json
import os
from psycopg2 import extras

CONFIG_FILE = 'config.ini'


def load_config():
    """
    Load config.ini file
    """
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)

#   Add the following in connect() to use the cfg file:
#   cfg = load_config()
#   user = cfg['database']['user']
#   password = cfg['database']['password']
#   host = cfg['database']['host']
#   port = cfg['database']['port']
#   database = cfg['database']['database']
    return cfg


def connect():
    """
    Connect to a POSTGRES database. Config-vars in heroku env
    :return: A valid connection
    """
    user = os.environ.get('PSQL_USER')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    port = os.environ.get('PSQL_PORT')
    database = os.environ.get('PSQL_DATABASE')

    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)
    return conn


def add_lineup(match_id, lineup_key, win):
    """
    Add a new lineup to the database
    """
    conn = connect()
    cur = conn.cursor()
    query_lineup = 'insert into lineups values(%s, %s, %s, %s, %s)'
    query_match_id = 'insert into match_ids values(%s, %s, %s)'

    if win:
        cur.execute(query_lineup, (lineup_key, 1, 0, 1, math.log(1)))
        cur.execute(query_match_id, (lineup_key, match_id, True))
    else:
        cur.execute(query_lineup, (lineup_key, 0, 1, 0, 0))
        cur.execute(query_match_id, (lineup_key, match_id, False))
    conn.commit()


def add_win(match_id, lineup_key):
    """
    Add a win to an existing lineup the database
    """
    conn = connect()
    cur = conn.cursor()
    query_lineup = 'update lineups set wins = wins +1 where lineup_key = %s'
    query_match_id = 'insert into match_ids values(%s, %s, %s)'
    cur.execute(query_match_id, (lineup_key, match_id, True))
    cur.execute(query_lineup, (lineup_key,))
    update_lineup_stats(lineup_key)
    cur.commit()


def add_loss(match_id, lineup_key):
    """
    Add a win to an existing lineup the database
    """
    conn = connect()
    cur = conn.cursor()
    query_lineup = 'update lineups set losses = losses +1 where lineup_key = %s'
    query_match_id = 'insert into match_ids values(%s, %s, %s)'
    cur.execute(query_match_id, (lineup_key, match_id, False))
    cur.execute(query_lineup, (lineup_key,))
    update_lineup_stats(lineup_key)
    cur.commit()


def import_db_json(file):
    """
    Help function to import json file of already parsedlineups to the database.
    See ex 'my_dict_9300k.json'.
    """
    conn = connect()
    cur = conn.cursor()
    print('Starting to parse')

    with open(file) as f:
        batch_lineup = []
        batch_match_ids = []
        lineups_parsed = 0
        matches = json.load(f)
        del matches['0.0.0.0.0']
        for key, value in matches.items():
            lineup_key = key
            wins = value['wins']
            losses = value['losses']
            winning_matches = value['winning_matches']
            losing_matches = value['losing_matches']
            win_rate = wins/(wins+losses)
            weighted_sort = win_rate * math.log(wins+losses)
            batch_lineup.append((lineup_key, wins, losses, win_rate, weighted_sort))
            for m in winning_matches:

                batch_match_ids.append((lineup_key, m, True))

            for m in losing_matches:
                batch_match_ids.append((lineup_key, m, False))

            if lineups_parsed % 5000 == 0:
                print('Lineups done: ', lineups_parsed)
                query_lineups = 'insert into lineups values %s'
                query_match_ids = 'insert into match_ids values %s'

                extras.execute_values(cur, query_lineups, batch_lineup)
                extras.execute_values(cur, query_match_ids, batch_match_ids)
                conn.commit()
                batch_lineup = []
                batch_match_ids = []

            lineups_parsed += 1


def get_highest_weighted_sort():
    """
    Return top 20 lineups with weighted_sort (win_rate * ln(wins+losses)
    :return: Array of sql rows.
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select * from lineups ' \
            'order by(weighted_sort) desc ' \
            'limit(20)'
    cur.execute(query)
    lineups_sorted = cur.fetchall()
    return lineups_sorted


def get_lowest_weighted_sort():
    """
    Return bottom 20 lineups with weighted_sort (win_rate * ln(wins+losses)
    Note: Weighted_sorts with less than 5 losses are not shown.
    :return: Array of sql rows.
    """
    conn = connect()
    cur = conn.cursor()
    print('getting weighted')
    query = 'select * from lineups ' \
            'where losses > 5 ' \
            'order by(weighted_sort) desc ' \
            'limit(20)'
    cur.execute(query)
    lineups_sorted = cur.fetchall()
    return lineups_sorted


def get_most_wins():
    """
    Return top 20 lineups sorted by wins
    :return: Array of sql rows.
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select * from lineups ' \
            'order by(wins) desc ' \
            'limit(20)'
    cur.execute(query)
    lineups_sorted = cur.fetchall()
    return lineups_sorted


def get_highest_win_rate():
    """
    Return top 20 lineups sorted by win_rate
    Note: Only games with more than 20 wins are shown.
    :return: Array of sql rows.
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select * from lineups ' \
            'where wins > 20 ' \
            'order by win_rate desc, wins desc ' \
            'limit(20)'
    cur.execute(query)
    lineups_sorted = cur.fetchall()
    return lineups_sorted


def get_most_losses():
    """
    Return top 20 lineups sorted by most losses
    :return: Array of sql rows.
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select * from lineups ' \
            'order by(losses) desc ' \
            'limit(20)'
    lineups_sorted = cur.execute(query)
    return lineups_sorted


def get_matches_parsed():
    """
    Get number of matches parsed.
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select count(*) from match_ids'
    cur.execute(query)
    matches_parsed = cur.fetchone()[0]         # contains loss and win for each
    matches_parsed = round(matches_parsed/2.0)                  # match, so we need to divide by 2.
    return matches_parsed


def get_matches_by_lineup(lineup_key):
    """
    Get a list of all match_ids with a specific lineup_key
    """
    conn = connect()
    cur = conn.cursor()
    query = 'select match_id, win from match_ids ' \
            'where lineup_key=%s'
    cur.execute(query, (lineup_key,))
    matches = cur.fetchall()
    return matches


def update_lineup_stats(lineup_key):
    """
    Help function to update win_rate and weighted_sort.
    Use when adding a win/loss to a lineup since the two functions won't update
    manually.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('select wins, losses from lineups '
                'where lineup_key =%s')
    old_stats = cur.fetchone()
    wins = old_stats[0]
    losses = old_stats[1]
    win_rate = wins/(wins+losses)
    weighted_sort = wins * math.log(wins+losses)

    query = 'update lineups ' \
            'set win_rate = %s, weighted_sort = %s ' \
            'where lineup_key = %s'
    cur.execute(query, (win_rate, weighted_sort, lineup_key))
    conn.commit()

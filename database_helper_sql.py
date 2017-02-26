#!/usr/bin/python
import configparser
import psycopg2
import math
import json
from psycopg2 import extras

CONFIG_FILE = 'config.ini'


def load_config():
    """
    Load config.ini file
    """
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    return cfg


def connect():
    cfg = load_config()
    user = cfg['database']['user']
    password = cfg['database']['password']
    host = cfg['database']['host']
    port = cfg['database']['port']
    database = cfg['database']['database']

    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)
    return conn


def add_lineup(match_id, lineup_key, win):
    conn = connect()
    cur = conn.cursor()
    cmd_lineup = 'insert into lineups values(%s, %s, %s, %s, %s)'
    cmd_match_id = 'insert into match_ids values(%s, %s, %s)'

    if win:
        cur.execute(cmd_lineup, (lineup_key, 1, 0, 1, math.log(1)))
        cur.execute(cmd_match_id, (lineup_key, match_id, True))
    else:
        cur.execute(cmd_lineup, (lineup_key, 0, 1, 0, 0))
        cur.execute(cmd_match_id, (lineup_key, match_id, False))

    conn.commit()


def import_db_json(file):
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
                cmd_lineups = 'insert into lineups values %s'
                cmd_match_ids = 'insert into match_ids values %s'

                extras.execute_values(cur, cmd_lineups, batch_lineup)
                extras.execute_values(cur, cmd_match_ids, batch_match_ids)
                conn.commit()
                batch_lineup = []
                batch_match_ids = []

            lineups_parsed += 1

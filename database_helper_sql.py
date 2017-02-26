#!/usr/bin/python
import MySQLdb


def connect():
    db = MySQLdb.connect(host='198.199.126.36',
                         user='root',
                         passwd='glassbil1337',
                         db='lineups_db')
    return db


def add_lineup(match_id, lineup_key, win):
    db = connect()
    cur = db.cursor()
    cmd_lineup = 'insert into lineups values(%s, %s, %s, %s, %s)'
    cmd_match_id = 'insert into match_ids values(%s, %s, %s)'

    if win:
        cur.execute(cmd_lineup, (lineup_key, 1, 0, 1))
        cur.execute(cmd_match_id, (lineup_key, match_id, True))
    else:
        cur.execute(cmd_lineup, (lineup_key, 0, 1, 0))
        cur.execute(cmd_match_id, (lineup_key, match_id, False))

    db.commit()


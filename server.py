#!/usr/bin/python
"""
This module acts as a Flask server for the project
"""

import os
from flask import Flask, request, jsonify
import database_helper
import json

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    """
    Send the initial html to the client.
    """
    return app.send_static_file('client.html')


@app.route('/force_update', methods=['POST'])
def force_update():
    """
    Force update the top lineups table in the database
    """
    if database_helper.update_top_tables():
        return json.dumps({'success': True,
                           'message': 'Top lineups has been update'
                           })
    else:
        return json.dumps({'success': False,
                           'message': 'Failed to update top lineups'
                           })


@app.route('/show_matches', methods=['POST'])
def show_matches():
    """
    This route sends the top 20 matches that have been parsed to the client.

    Sorting can be either win_rate or wins.
    """
    sorting = request.form['sorting']
    matches = None

    if sorting == 'win_rate':
        matches = database_helper.get_highest_win_rate()

    elif sorting == 'weighted_sort':
        matches = database_helper.get_highest_weighted_sort()

    elif sorting == 'wins':
        matches = database_helper.get_most_wins()

    elif sorting == 'losses':
        matches = database_helper.get_most_losses()

    else:
        return json.dumps({'success': False,
                           'message': 'Match data could not be retrieved',
                           })

    matches_parsed = database_helper.get_matches_parsed_fast()
    last_update = database_helper.get_last_update().strftime("%Y-%m-%d %H:%M")
    if matches:
        data = []
        for m in matches:
            keys = ['lineup_key', 'wins', 'losses', 'win_rate', 'weighted_sort']
            data.append(dict(zip(keys, m)))
        return json.dumps({'success': True,
                           "message": "Match data retrieved successfully",
                           "data": data,
                           "matches_parsed": matches_parsed,
                           "last_update": last_update
                           })
    else:
        return json.dumps({'success:': False,
                           "message": "Match data could not be retrieved",
                           })


@app.route('/lineup/<lineup_key>', methods=['GET'])
def show_matches_for_lineup(lineup_key):
    """
    Get a dict with match_id and win/loss
    """
    matches = {'wins': [], 'losses': []}
    for m in database_helper.get_matches_by_lineup(lineup_key):

        if m[1]:        # match won
            matches['wins'].append(m[0])

        else:           # match lost
            matches['losses'].append(m[0])

    return jsonify(matches)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

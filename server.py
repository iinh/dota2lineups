"""
This module acts as a Flask server for the project

"""

import os
from flask import Flask, request
import database_helper
import json

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    """
    Send the initial html to the client.
    """
    return app.send_static_file('client.html')


@app.route('/show_matches', methods=['POST'])
def show_matches():
    """
    This route sends the top 20 matches that have been parsed to the client.

    Sorting can be either win_rate or wins.
    """
    sorting = request.form['sorting']
    matches = None

    if sorting == 'win_rate':
        matches = database_helper.get_highest_winrate()

    elif sorting == 'wins':
        matches = database_helper.get_most_wins()

    # used for counting the number of lineups currently parsed.
    lineups_parsed = database_helper.get_lineups_parsed()

    if matches:
        data = []

        # we need to pop the id column that Mongo db adds
        # matches are stored as dictionaries in the data array
        for m in matches:
            m.pop('_id')
            dict(m)
            data.append(m)

        return json.dumps({'success': True,
                           "message": "Match data retrieved successfully",
                           "data": data, "lineups_parsed": lineups_parsed})
    else:
        return json.dumps({'success:': False,
                           "message": "Match data could not be retrieved"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

import os
from flask import Flask, request
import database_helper
import json

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return app.send_static_file('client.html')


@app.route('/show_matches', methods=['POST'])
def show_matches():
    sorting = request.form['sorting']

    matches = None

    if sorting == 'win_rate':
        matches = database_helper.get_highest_winrate()

    elif sorting == 'wins':
        matches = database_helper.get_most_wins()

    matches_parsed = database_helper.get_matches_parsed().pop('matches_parsed')
    if matches:
        data = []
        for m in matches:
            m.pop('_id')
            dict(m)
            data.append(m)

        return json.dumps({'success:': True,
                           "message": "Match data retrieved successfully",
                           "data": data, "matches_parsed": matches_parsed})
    else:
        return json.dumps({'success:': False,
                           "message": "Match data could not be retrieved"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

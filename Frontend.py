from flask import Flask, render_template, request, session, flash, jsonify
# import sqlite3 as sql
import os
# import string, base64
# import pandas as pd
# import Backend

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("input.html")


@app.route('/query', methods=['POST'])
def do_query():
    try:
        ands = request.form['req']
        ors = request.form['con']
        nots = request.form['not']
        range1 = request.form['range1']
        range2 = request.form['range2']
        range3 = request.form['range3']

        print(ands, ors, nots, range1, range2, range3)
        if(not range1):
            print("range 1 is infinite")
        if (not range2):
            print("range 2 is infinite")
        if (not range3):
            print("range 3 is infinite")

        flash("query was accepted")
    except:
        flash("We had some issues searching.")
    finally:
        print("Block end reached, nice")
    return home()

@app.route('/results', methods=['POST'])
def results():
    return results()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)



from sys import path
import os

path.append('src')  #go to src directory to import
from flask import Flask, render_template, redirect
from CASClient import CASClient
import secrets
import validation
import subprocess

# app info
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
os.putenv("export", "DB_URL=postgres://oxifvfuc:3Z_OtccJkuJzjE4je2oRnEe3LE47Ksgk@peanut.db.elephantsql.com/oxifvfuc")

@app.route('/')
def hello():
    return render_template('landing.html')

@app.route('/home')
def application():
    print(os.getenv('DB_URL'))
    netid = CASClient().Authenticate()
    netid = netid[0:len(netid)-1]
    is_in_club = validation.get_club_status(netid, 1)
    print(is_in_club, "huh")
    if is_in_club:
        return render_template('home.html', CASValue = netid, validation = is_in_club)
    else:
        return render_template('invalid.html', CASValue = netid)

@app.route('/unvalidated')
def unvalidated():
    return render_template('invalid.html', CASValue = netid, validation = is_in_club)

@app.route('/members')
def members():
    members = [{"name": "john", "year": 2020, "position": "mid"}, {"name": "frank", "year": 2020, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}, {"name": "john", "year": 2020, "position": "mid"}, {"name": "frank", "year": 2020, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}]
    return render_template('members.html', members = members)
@app.route('/announcements')
def announcements():
    netid = CASClient().Authenticate()
    netid = netid[0:len(netid)-1]
    is_in_club = validation.get_club_status(netid, 1)
    return render_template('announcements.html', CASValue = netid, validation = is_in_club)


if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

from sys import path
import os
path.append('src')  #go to src directory to import
from flask import Flask, render_template, redirect, request
from CASClient import CASClient
import secrets
import posts
import profile

CLUB_SOCC = 1


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
    user = profile.Profile(user_id = netid)
    # need to check if in user database OR add to database if not
    is_in_club = user.validate(CLUB_SOCC)
    if is_in_club:
        return render_template('home.html', CASValue = netid, validation = is_in_club)
    else:
        return render_template('invalid.html', CASValue = netid)

@app.route('/members')
def members():
    members = [{"name": "john", "year": 2020, "position": "mid"}, {"name": "frank", "year": 2020, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}, {"name": "john", "year": 2020, "position": "mid"}, {"name": "frank", "year": 2020, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}]
    return render_template('members.html', members = members)

@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        posts.make_posts("Added through the button")
    post_values = posts.get_posts()
    print(post_values)
    # print(posts)
    return render_template('announcements.html', posts = post_values)

@app.route('/announcements/posts')
def post_announcement():
    posts.get_posts()
    print(post_values)
    # print(posts)
    return render_template('announcements.html', posts = post_values)

if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

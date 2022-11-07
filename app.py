import profile
import posts
import secrets
from CASClient import CASClient
from flask import Flask, render_template, redirect, request
from sys import path
import os
path.append('src')  # go to src directory to import

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
    user = profile.Profile(user_id=netid)
    # need to check if in user database OR add to database if not
    is_in_club = user.validate(CLUB_SOCC)
    if is_in_club:
        return render_template('home.html', CASValue=netid, validation=is_in_club)
    else:
        return render_template('invalid.html', CASValue=netid)


@app.route('/members')
def members():
    # members = [{"name": "Yash", "year": 2024, "position": "mid"}, {"name": "Emilio", "year": 2023, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}, {"name": "Allen", "year": 2024, "position": "mid"}, {"name": "frank", "year": 2020, "position": "striker"}, {"name": "mollie", "year": 2020, "position": "striker"}]
    members = profile.get_profiles_from_club(1)
    return render_template('members.html', members=members)


@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        posts.make_posts(request.form.get('Post Description'))
    post_values = posts.get_posts()
    print(post_values)
    return render_template('announcements.html', posts=post_values)


@app.route('/profile')
def profiles():
    net_id = request.args.get("net_id", None)
    user = profile.get_profile_from_id(net_id)
    return render_template('profile.html', user=user)


@app.route('/donations')
def donations():
    return render_template('donations.html')


@app.route('/donations/completed')
def completed():
    return render_template('donations')


if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

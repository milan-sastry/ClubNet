

import profile
import posts
import secrets
from flask import Flask, render_template, redirect, request, url_for
from sys import path
import os
import admin

# separation
path.append('src')  # go to src directory to import
from CASClient import CASClient


CLUB_SOCC = 1

INVALID = 0
REQUEST = 1
VALIDATED = 2


# app info
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def hello():
    return render_template('landing.html')


@app.route('/home')
def application():
    print(os.getenv('DB_URL'))

    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    return render_template('home.html', CASValue=response[0], validation=response[1])


@app.route("/pending_request")
def pending_request():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == VALIDATED:
        return redirect(url_for('application'))

    return render_template('pending_request.html', CASValue=response[0])


@app.route("/invalid", methods=['GET', 'POST'])
def invalid():
    response = validate_user(CLUB_SOCC)
    if response[1] == VALIDATED:
        return redirect(url_for('application'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    # print(request)
    if request.method == 'POST':
        admin.create_request(request.args.get('user_id'), CLUB_SOCC)
        return redirect(url_for('pending_request'))
    return render_template('invalid.html', CASValue=response[0])


@app.route('/members')
def members():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    members = profile.get_profiles_from_club(CLUB_SOCC)
    return render_template('members.html', members=members)


@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    post_values = posts.get_posts()
    return render_template('announcements.html', posts=post_values)


@app.route('/profile')
def profiles():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    net_id = request.args.get("net_id", None)
    user = profile.get_profile_from_id(net_id)
    return render_template('profile.html', user=user)

@app.route('/myprofile', methods=["GET", "POST"])
def myProfile():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    net_id = CASClient().Authenticate()
    net_id = net_id[0:len(net_id)-1]
    user = profile.get_profile_from_id(net_id)
    if request.method == 'POST':
        print(request.form, "requqest?")
    return render_template('myprofile.html', user=user)


@app.route('/donations')
def donations():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    return render_template('donations.html')


@app.route('/donations/completed')
def completed():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    return render_template('donations')


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    pendingRequests = admin.get_requests()
    return render_template('admin.html', requests=pendingRequests)


@app.route('/admin/accept', methods=['GET', 'POST'])
# response.set_cookie('previous_search', ("/?dept=" + str(dept) +
# "&coursenum=" + str(coursenum) + "&area=" + str(area) +
# "&title=" + str(title)))
#  previous_search = flask.request.cookies.get('previous_search')
def admin_accept_page():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    admin.acceptRequest(user_id, club_id)
    return redirect(url_for('admin_page'))

@app.route('/form', methods=['GET', 'POST'])
def render_form():
    if request.method == 'POST':
        # make the post
        # then send them to add image
        print(request)
        posts.make_posts(request.form.get('Post Title'),request.form.get('Post Description'))
        return redirect(url_for('announcements'))
    return render_template("form.html")

# @app.route('/image', methods=['GET', 'POST'])
# def add_image():
#     netid = CASClient().Authenticate()
#     return render_template("add_image.html", user_id=netid)

@app.route('/admin/deny', methods=['GET', 'POST'])
def admin_deny_page():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    admin.deleteRequest(user_id, club_id)
    return redirect(url_for('admin_page'))

def validate_user(club_id):
    netid = CASClient().Authenticate()
    netid = netid[0:len(netid)-1]
    is_in_club = profile.validate(netid, club_id)
    if is_in_club:
        return (netid, VALIDATED)
    else:
        is_in_requests = admin.check_request(netid, CLUB_SOCC)
        if is_in_requests:
            return (netid, REQUEST)
        else:
            return (netid, INVALID)

if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

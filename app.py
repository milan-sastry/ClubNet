

import profile
import posts
import secrets
from flask import Flask, render_template, redirect, request, url_for, jsonify
from sys import path
import os
import admin
import upload
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
from cloudinary.utils import cloudinary_url

# separation
path.append('src')  # go to src directory to import
from CASClient import CASClient


CLUB_SOCC = 1

INVALID = 0
REQUEST = 1
VALIDATED = 2
ADMIN = 3


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
    img = get_profile_pic(response[0])
    return render_template('home.html', CASValue=response[0], validation=response[1],
    img1="https://upload.wikimedia.org/wikipedia/commons/d/d0/Princeton_seal.svg",
    img2="https://www.princeton.edu/~clubsocc/img/team_main.jpeg", img=img)


@app.route("/pending_request")
def pending_request():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == VALIDATED:
        return redirect(url_for('application'))
    img = get_profile_pic(response[0])
    return render_template('pending_request.html', CASValue=response[0], img=img)


@app.route("/invalid", methods=['GET'])
def invalid():
    response = validate_user(CLUB_SOCC)
    if response[1] == (VALIDATED or ADMIN):
        return redirect(url_for('application'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    img = get_profile_pic(response[0])
    return render_template('invalid.html', CASValue=response[0], img=img)

@app.route("/process_request", methods=['GET', 'POST'])
def process_request():
    netid = request.args.get('user_id', None)
    name = request.form.get('name', None)
    year = request.form.get('year', None)
    print(netid, name, year)
    profile.create_profile(netid, name, year)
    admin.create_request(netid, CLUB_SOCC, name, year)
    return redirect(url_for('pending_request'))


@app.route('/members')
def members():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    img = get_profile_pic(response[0])
    members = profile.get_profiles_from_club(CLUB_SOCC)
    return render_template('members.html', members=members, img=img)


@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    post_values = posts.get_posts()
    img = get_profile_pic(response[0])
    return render_template('announcements.html', posts=post_values, img=img)


@app.route('/profile')
def profiles():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    net_id = request.args.get("net_id", None)
    user = profile.get_profile_from_id(net_id)
    img = get_profile_pic(response[0])
    return render_template('profile.html', user=user, img=img)

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
        profile.edit_profile(net_id, request.form)
    img = get_profile_pic(response[0])
    return render_template('myprofile.html', user=user, img=img)


@app.route('/donations')
def donations():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    img = get_profile_pic(response[0])
    return render_template('donations.html', img=img)


@app.route('/donations/completed')
def completed():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    img = get_profile_pic(response[0])
    return render_template('donations', img=img)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("application"))
    pendingRequests = admin.get_requests()
    img = get_profile_pic(response[0])
    return render_template('admin.html', requests=pendingRequests, img=img)


@app.route('/admin/accept', methods=['GET'])
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
    if response[1] == VALIDATED:
        return redirect(url_for("application"))

    user_id = request.args.get("user_id", None)
    admin.approve_request(user_id, CLUB_SOCC)
    return redirect(url_for('admin_page'))

@app.route('/admin/deny', methods=['GET', 'POST'])
def admin_deny_page():
    response = validate_user(CLUB_SOCC)
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("application"))

    user_id = request.args.get("user_id", None)
    admin.delete_request(user_id, CLUB_SOCC)
    return redirect(url_for('admin_page'))

@app.route('/form', methods=['GET', 'POST'])
def render_form():
    if request.method == 'POST':
        # make the post
        # then send them to add image
        print(request)
        posts.make_posts(request.form.get('Post Title'),request.form.get('Post Description'))
        return redirect(url_for('base_upload'))
    return render_template("form.html")

# @app.route('/image', methods=['GET', 'POST'])
# def add_image():
#     netid = CASClient().Authenticate()
#     if request.method == 'POST':
#         # upload.add_image(netid, request.form.get('File'))
#         return redirect(url_for('base_upload'))
#     # netid = CASClient().Authenticate()
#     return render_template("image.html")

def validate_user(club_id):
    netid = CASClient().Authenticate()
    netid = netid[0:len(netid)-1]
    is_in_club = profile.validate(netid, club_id)
    if is_in_club:
        if admin.is_admin(netid, club_id):
            return (netid, ADMIN)
        else:
            return (netid, VALIDATED)
    else:
        is_in_requests = admin.check_request(netid, CLUB_SOCC)
        if is_in_requests:
            return (netid, REQUEST)
        else:
            return (netid, INVALID)

# WIP here about the uploading of images
@app.route("/upload", methods=['POST'])
def upload_file():
    # netid = CASClient().Authenticate()
    file_cloudinary_link = ""
    app.logger.info('in upload route')

    cloudinary.config(cloud_name = 'clubnet', api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        file_cloudinary_link = upload_result['url']
        if file_cloudinary_link != None:
            # print(netid)
            print(file_cloudinary_link)
            print(jsonify(upload_result))
            posts.add_image("yparikh", file_cloudinary_link)
            # return redirect(url_for('announcements'))
    return jsonify(upload_result)

@app.route("/upload_page")
def base_upload():
    return render_template("image_upload.html")

def get_profile_pic(net_id):
    user = profile.get_profile_from_id(net_id)
    img = user.profile_image_url
    return img

if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

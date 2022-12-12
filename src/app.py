# import necessary libraries and modules
import secrets
from flask import Flask, render_template, redirect, request, url_for, jsonify, flash, session
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import sqlalchemy
from flask_mail import Mail, Message
from CASClient import CASClient
import admin as adminmod
import posts as postsmod
import profiles as profilemod

# Types of validation status
INVALID = 0
REQUEST = 1
VALIDATED = 2
ADMIN = 3

# app info and secret keys
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
os.environ['DB_URL']="postgres://oxifvfuc:3Z_OtccJkuJzjE4je2oRnEe3LE47Ksgk@peanut.db.elephantsql.com/oxifvfuc"
os.environ['CLOUDINARY_URL']="cloudinary://375874577914178:bAM3VvtO-xWQCB_TIdgZ--bhG5Y@clubnet"
os.environ['API_KEY']="375874577914178"
os.environ['API_SECRET']="bAM3VvtO-xWQCB_TIdgZ--bhG5Y"

#mail account information
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ClubNetPrinceton@gmail.com'
app.config['MAIL_PASSWORD'] = 'rzylxkhufcffwzxo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#database connection
DATABASE_URL = os.getenv('DB_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = sqlalchemy.create_engine(DATABASE_URL)

#landing page for site
@app.route('/')
def hello():
    return render_template('landing.html')

# ---------------------- END POINTS FOR VALIDATION ---------------------

#landing page for invalidated users
@app.route("/invalid", methods=['GET'])
def invalid():
    response = validate_user()
    if response[1] == VALIDATED:
        return redirect(url_for('home'))
    if response[1] == ADMIN:
        return redirect(url_for('home'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    return render_template('invalid.html', CAS_Value=response[0],validation=response[1])

#endpoint for processing a join request
@app.route("/process_request", methods=['GET', 'POST'])
def process_request():
    response = validate_user()
    user_id = request.args.get('user_id', None)
    name = request.form.get('name', None)
    year = request.form.get('year', None)
    email = request.form.get('email', None)
    print("process request", name, year, email)

    # flash error message if input data is not proper
    if name == '' or year == '' or year.isnumeric() == False or email == '':
        flash('please enter valid, nonempty personal information')
        return redirect(url_for('invalid'))

    else:
        profilemod.create_profile(engine, user_id, name, year, email)
        adminmod.create_request(engine, user_id)

         # sends email to user after requests to join
        messagetwo = Message("Your User Request on ClubNet!",sender ='ClubNetPrinceton@gmail.com', recipients = [email])
        messagetwo.body = 'You are being notified because your request to join Club Soccer on ClubNet is now pending! You will be notified again if you are approved! \n \n '
        messagetwo.body += "Best regards,\n"
        messagetwo.body += "The ClubNet Team\n"
        messagetwo.body += "clubnet.onrender.com"
        mail.send(messagetwo)
        print("SENT AN EMAIL")

        # sends email to admins for new join requests
        admins = adminmod.get_admins(engine)
        recipientlistone = []
        for each_admin in admins:
            if each_admin.get_email() != "None":
                email = each_admin.get_email()
                recipientlistone.append(email)
        message = Message("New User Request on ClubNet!",sender ='ClubNetPrinceton@gmail.com', recipients = recipientlistone)
        message.body = 'You are being notified because a new user has made a request to join Club Soccer on ClubNet that needs to be processed! \n \n To view the contents of this new request, go to https://clubnet.onrender.com/adminmod.\n \n '
        message.body += "Best regards,\n"
        message.body += "The ClubNet Team\n"
        message.body += "clubnet.onrender.com"
        mail.send(message)
        print("SENT AN EMAIL")

        return redirect(url_for('pending_request'))

# landing page for users with pending requests
@app.route("/pending_request")
def pending_request():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == VALIDATED:
        return redirect(url_for('home'))
    if response[1] == ADMIN:
        return redirect(url_for('home'))

    admins = adminmod.get_admins(engine)
    return render_template('pending_request.html', CASValue=response[0], admins = admins)

# home website (also landing page for approved users)
@app.route('/home')
def home():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    user_id = response[0]

    user = profilemod.get_profile_from_id(engine, user_id)
    img = user.get_profile_image_url()
    member_count, alumni_count = profilemod.get_club_member_count(engine)
    return render_template('home.html', CASValue=response[0], validation=response[1], img=img, member_count=member_count, alumni_count=alumni_count)

# ---------------------- END POINTS FOR MEMBERS ------------------------

# members site which displays all members
@app.route('/members', methods=['GET', 'POST'])
def members():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    user_id = response[0]
    user = profilemod.get_profile_from_id(engine, user_id)
    img = user.get_profile_image_url()
    return render_template('members.html', img=img, validation=response[1])

#endpoint to get all user profiles (only accessed via AJAX)
@app.route('/memberlist')
def member_list():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    name = request.args.get("name", None)
    year = request.args.get("year", None)
    major = request.args.get("major", None)
    industry = request.args.get("industry", None)
    status_filter = int(request.args.get("filter", None))

    members = profilemod.get_profiles_from_club_filtered(engine, name, year, status_filter,major, industry)
    return render_template("member_list.html", members=members)

#page to see a specific profile
@app.route('/profile')
def profiles():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    user_id = request.args.get("net_id", None)
    user = profilemod.get_profile_from_id(engine, user_id)
    cover_net_id = response[0]
    cover_user = profilemod.get_profile_from_id(engine, cover_net_id)
    img = cover_user.get_profile_image_url()
    return render_template('profile.html', user=user, img=img, validation=response[1])

#page to see and edit your own profile
@app.route('/myprofile', methods=["GET", "POST"])
def myProfile():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    user_id = response[0]
    user = profilemod.get_profile_from_id(engine, user_id)
    img = user.get_profile_image_url()
    if request.method == 'POST':
        print(request.form.get('notifications'))
        profilemod.edit_profile(engine, user_id, request.form)
        return redirect(url_for('members'))
    return render_template('myprofile.html', user=user, img=img, validation=response[1])

#endpoint to change a profile image
@app.route("/upload_profile_image_page")
def profile_image_url():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    cover_user = profilemod.get_profile_from_id(engine, response[0])
    img = cover_user.get_profile_image_url()
    return render_template("profile_image_upload.html", validation=response[1], img=img)

#endpoint to save a prof pic on cloudinary
@app.route("/upload_profile_image", methods=['POST', 'GET'])
def upload_profile_image():
    file_cloudinary_link = ""

    cloudinary.config(cloud_name = 'clubnet', api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']

    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        file_cloudinary_link = upload_result['url']
        if file_cloudinary_link != None:
            response = validate_user()
            profilemod.edit_profile_image(engine, response[0], file_cloudinary_link)
            print("updated with a cloudinary link")
            return redirect(url_for('home'))

    return jsonify(upload_result)

# ---------------------- END POINTS FOR ANNOUNCEMENTS ------------------

# endpoint to view announcements
@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    page_number = request.args.get("page_number", None)

    if page_number:
        page_number = int(page_number)
    else:
        page_number = 1

    filter = request.args.get("filter", None)
    post_values, num_pages = postsmod.get_posts(engine, user_id = response[0], filter=filter, page=page_number, total_rows = True)
    net_id = response[0]
    user = profilemod.get_profile_from_id(engine, net_id)
    img = user.profile_image_url
    members = profilemod.get_profiles_from_club(engine)
    isAdmin = adminmod.is_admin(engine, net_id)
    return render_template('announcements.html', posts=post_values, img=img, validation=response[1], isAdmin=isAdmin, user=user, filter=filter, netid = net_id, page_number=page_number, num_pages=num_pages)

# internal endpoint to handle filtering
@app.route('/get_announcements')
def get_announcements():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    filter = request.args.get("filter", None)
    netid = request.args.get("id", None)
    page_number = request.args.get("page_number", None)
    print("page pls", page_number)
    if page_number:
        page_number = int(page_number)
    else:
        page_number = 1
    post_values, num_pages = postsmod.get_posts(engine, response[0], filter, page_number, True)
    isAdmin = adminmod.is_admin(engine, netid)
    return render_template('announcement_list.html', posts=post_values, isAdmin=isAdmin, page_number=page_number, num_pages=num_pages)

# endpoint to delete a post
@app.route('/announcements/delete', methods=['GET', 'POST', 'DELETE'])
def delete_post():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    post_id = request.args.get("post_id", None)
    postsmod.delete_post(engine, post_id)
    return redirect(url_for('announcements'))

# ednpoint to like a post
@app.route('/announcements/like', methods=['GET'])
def like():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    post_id = request.args.get("post_id", None)
    postsmod.like(engine, post_id, response[0])
    return redirect(url_for('announcements'))

# ednpoint to unlike a post
@app.route('/announcements/unlike', methods=['GET'])
def unlike():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    post_id = request.args.get("post_id", None)
    postsmod.unlike(engine, post_id, response[0])
    return redirect(url_for('announcements'))

# endpoint to comment on a post
@app.route('/announcements/comment', methods=['GET'])
def comment():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))

    comment = request.args.get("comment-input", None)
    post_id = request.args.get("post_id", None)
    postsmod.comment(engine, post_id, response[0], comment)
    return redirect(url_for('announcements'))

# form to create a new post
@app.route('/form', methods=['GET', 'POST'])
def render_form():
    if request.method == 'POST':
        # make the post
        # then send them to add image
        response = validate_user()
        id = postsmod.make_request(engine, request.form.get('Post Title'),request.form.get('Post Description'), response[0])
        return redirect(url_for('base_upload',post_id=id))
    return render_template("form.html")

#page to add an image to a post
@app.route("/upload_post_image_page")
def base_upload():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    post_id = request.args.get('post_id')
    cover_user = profilemod.get_profile_from_id(engine, response[0])
    img = cover_user.get_profile_image_url()

    # sends email to admins for new posts suggested
    admins = adminmod.get_admins(engine)
    recipientlist = []
    for each_admin in admins:
        if each_admin.get_email() != "None":
            email = each_admin.get_email()
            recipientlist.append(email)

    message = Message("New Post Suggested on ClubNet!",sender ='ClubNetPrinceton@gmail.com', recipients = recipientlist)
    message.body = 'You are being notified because a user has suggested a new post in Club Soccer on ClubNet! \n \n To approve or decline, go to https://clubnet.onrender.com/adminmod.\n \n '
    message.body += "Best regards,\n"
    message.body += "The ClubNet Team\n"
    message.body += "clubnet.onrender.com"
    mail.send(message)
    print('sent an email to admins')

    return render_template("image_upload.html", post_id=post_id, validation=response[1], img=img)

#endpoint to add an image to a post
@app.route("/upload_post_image", methods=['POST', 'GET'])
def upload_file():
    file_cloudinary_link = ""
    post_id = request.args.get('post_id')
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
        print(jsonify(upload_result))
        file_cloudinary_link = upload_result['url']
        if file_cloudinary_link != None:
            postsmod.add_image(engine, post_id, file_cloudinary_link)
            return redirect(url_for('home'))
    return jsonify(upload_result)

# ---------------------- END POINTS FOR ADMIN --------------------------

# main landing page for admin with most of the functionality
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    pendingRequests = adminmod.get_requests(engine)
    postRequests = postsmod.get_post_requests(engine)
    user_id = response[0]
    user = profilemod.get_profile_from_id(engine, user_id)
    img = user.get_profile_image_url()
    members = profilemod.get_profiles_from_club(engine)
    all_members = 'mailto:'
    students = 'mailto:'
    alumni = 'mailto:'
    for member in members:
        if member.get_email() != "None":
                all_members += member.get_email() + ','
                if member.is_alumni():
                    alumni += member.get_email() + ','
                else:
                    students += member.get_email() + ','

    return render_template('admin.html', members=members, requests=pendingRequests, posts = postRequests, validation=response[1], img=img, all_members = all_members, students = students, alumni = alumni)

#admin accept user
@app.route('/admin/accept', methods=['GET'])
def admin_accept_page():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))

    user_id = request.args.get("user_id", None)
    email = adminmod.get_request_email(engine, user_id)
    adminmod.approve_request(engine, user_id)
    print("sucessfully approved")

    # sends email to user if they have newly been validated
    message = Message("Request Approved on ClubNet!",sender ='ClubNetPrinceton@gmail.com', recipients = [email])
    message.body = 'You are being notified because your request to join Club Soccer on ClubNet has been approved! \n \n To log in, go to https://clubnet.onrender.com.\n \n '
    message.body += "Best regards,\n"
    message.body += "The ClubNet Team\n"
    message.body += "clubnet.onrender.com"
    mail.send(message)
    print("SENT AN EMAIL")
    return redirect(url_for('admin_page'))

# admin deny user
@app.route('/admin/deny', methods=['GET'])
def admin_deny_page():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))

    user_id = request.args.get("user_id", None)
    adminmod.delete_request(engine, user_id)
    return redirect(url_for('admin_page'))

#admin remove user
@app.route('/admin/remove_user', methods=["POST"])
def remove_user():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    user_id = request.form.get("user_id", None)
    adminmod.remove_user(engine, user_id)
    return redirect(url_for('admin_page'))

# remove admin privileges
@app.route('/admin/remove_admin', methods=["POST"])
def remove_admin():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    net_id = request.form.get("user_id", None)
    adminmod.remove_admin(engine, net_id)
    return redirect(url_for('admin_page'))

#give admin privileges
@app.route('/admin/make_admin', methods=["POST"])
def make_admin():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    user_id = request.form.get("user_id", None)
    officer_position = request.form.get("off_pos", None)
    adminmod.make_admin(engine, user_id, officer_position)
    return redirect(url_for('admin_page'))

#accept post request
@app.route('/admin/accept_post', methods=["GET"])
def accept_post():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    post_id = request.args.get("post_id", None)


    postsmod.approve_post_request(engine, post_id)
    recipientlist = []
    for person in profilemod.get_profiles_from_club(engine):
        if person.get_email() != "None":
            if(person.get_notifications() == "true"):
                email = person.get_email()
                recipientlist.append(email)
    print(recipientlist)

    message = Message("New Post on ClubNet!",sender ='ClubNetPrinceton@gmail.com', recipients = recipientlist)
    message.body = 'You are being notified because a new post has been made for Club Soccer on ClubNet! \n \n To view the contents of the new post, go to https://clubnet.onrender.com/announcements.\n \n '
    message.body += "Best regards,\n"
    message.body += "The ClubNet Team"
    message.body += "clubnet.onrender.com"
    mail.send(message)
    print("SENT AN EMAIL")

    return redirect(url_for('admin_page'))

#reject post request
@app.route('/admin/deny_post', methods=["GET"])
def deny_post():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    if response[1] == VALIDATED:
        return redirect(url_for("home"))
    post_id = request.args.get("post_id", None)
    postsmod.reject_request(engine, post_id)
    return redirect(url_for('admin_page'))


# --------------------MISCELLANEOUS-------------------------------------

# function to validate a user's status as 1 of 4 possible states
def validate_user():

    # send request to CAS and return/print validation status
    user_id = CASClient().Authenticate()
    is_in_club = profilemod.validate(engine, user_id)
    if is_in_club:
        if adminmod.is_admin(engine, user_id):
            print(f'validated {user_id} as admin')
            return (user_id, ADMIN)
        else:
            print(f'validated {user_id} as member')
            return (user_id, VALIDATED)
    else:
        is_in_requests = adminmod.check_request(engine, user_id)
        if is_in_requests:
            print(f'validated {user_id} as requested')
            return (user_id, REQUEST)
        else:
            print(f'validated {user_id} as invalid')
            return (user_id, INVALID)

@app.route('/donations')
def donations():
    response = validate_user()
    if response[1] == INVALID:
        return redirect(url_for('invalid'))
    if response[1] == REQUEST:
        return redirect(url_for('pending_request'))
    user_id = response[0]
    user = profilemod.get_profile_from_id(engine, user_id)
    img = user.get_profile_image_url()
    return render_template('donations.html', img=img, validation=response[1])

# -------------------------MAIN-----------------------------------------
if __name__ == '__main__':
    app.run(host='localhost', port=5555, debug=True)

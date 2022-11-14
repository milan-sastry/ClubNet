import database
import os
import sqlalchemy.orm
import sqlalchemy

DATABASE_URL = os.getenv('DB_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


class Profile:
    user_id = None
    name = None
    email = None
    profile_image_url = None
    class_year = None
    major = None
    team_position = None
    favorite_team = None
    hometown = None
    job_title = None
    user_company = None

    def __init__(self, row):
        self.user_id = row.user_id
        self.name = row.name
        self.email = row.email
        self.profile_image_url = row.profile_image_url
        self.class_year = row.class_year
        self.major = row.major
        self.team_position = row.team_position
        self.favorite_team = row.favorite_team
        self.hometown = row.hometown
        self.job_title = row.job_title
        self.user_company = row.user_company

# ---------------------------EDIT----------------------------------------

    def edit_name(self, name):
        self.name = name

    def edit_email(self, email):
        self.email = email

    def edit_profile_image_url(self, profile_image_url):
        self.profile_image_url = profile_image_url

    def edit_class_year(self, class_year):
        self.class_year = class_year

    def edit_major(self, major):
        self.major = major

    def edit_team_position(self, team_position):
        self.team_position = team_position

    def edit_favorite_team(self, favorite_team):
        self.favorite_team = favorite_team

    def edit_hometown(self, hometown):
        self.hometown = hometown

    def edit_job_title(self, job_title):
        self.job_title = job_title

    def edit_user_company(self, user_company):
        self.user_company = user_company

# ---------------------------GET-----------------------------------------

    def get_user_id(self):
        return self.user_id
        
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_profile_image_url(self):
        return self.profile_image_url

    def get_class_year(self):
        if self.class_year:
            return self.class_year
        else: 
            return ""

    def get_major(self):
        if self.major:
            return self.major
        else: 
            return ""

    def get_team_position(self):
        if self.team_position:
            return self.team_position
        else: 
            return ""

    def get_favorite_team(self):
        if self.favorite_team:
            return self.favorite_team
        else: 
            return ""

    def get_hometown(self):
        if self.hometown:
            return self.hometown
        else: 
            return ""

    def get_job_title(self):
        if self.job_title:
            return self.job_title
        else: 
            return ""

    def get_user_company(self):
        if self.user_company:
            return self.user_company
        else: 
            return ""

# ---------------------------DELETE-------------------------------------

    def delete_user(self):
        pass
# ---------------------------VALIDATE-----------------------------------

def validate(user_id, club_id):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    bool = False

    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Users_Clubs).filter(
            database.Users_Clubs.username.ilike(user_id))
            # print(query)
            table = query.all()
            for row in table:
                # print("USER " + row.username + "OKAY " + str(row.club_id))
                if (row.club_id == club_id):
                    session.commit()
                    return True
            session.commit()
            
        return bool
    finally:
        engine.dispose()


def get_profile_from_id(user_id):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.User).filter(
            database.User.user_id == user_id).all()
            if len(query) > 0:
                profile = query[0]
                return Profile(profile)
            # else:
            #     # print("Wtfff", query)
            session.commit()
    finally:
        engine.dispose()


def get_profiles_from_club(club_id):
    profiles = []
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user_ids = session.query(database.Users_Clubs).filter(
                database.Users_Clubs.club_id == club_id).all()
            for user in user_ids:
                profile = session.query(database.User).filter(
                    database.User.user_id == user.username).all()
                if len(profile) > 0:
                    profile = Profile(session.query(database.User).filter(
                        database.User.user_id == user.username).all()[0])
                    profiles.append(profile)
            session.commit()
            return profiles
    finally:
        engine.dispose()

def edit_profile(user_id, data):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            response = session.query(database.User).filter(database.User.user_id == user_id).update({
                "class_year": data["class_year"],
                "major": data["major"],
                "team_position": data["team_position"], 
                "favorite_team": data["favorite_team"], 
                "hometown": data["hometown"],
                "job_title": data["job_title"],
                "user_company": data["user_company"]
            })
            session.commit()
            print("RESPONSEE", response)
            return True
    finally:
        engine.dispose()

def create_profile(user_id, name, year):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = database.User(user_id = user_id, name = name, year = year)
            session.add(user)
            session.commit()
    finally:
        engine.dispose()

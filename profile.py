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
        return self.class_year

    def get_major(self):
        return self.major

    def get_team_position(self):
        return self.team_position

    def get_favorite_team(self):
        return self.team_position

    def get_hometown(self):
        return self.hometown

    def get_job_title(self):
        return self.job_title

    def get_user_company(self):
        return self.user_company

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
            print(query)
            table = query.all()
            for row in table:
                print("USER " + row.username + "OKAY " + str(row.club_id))
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

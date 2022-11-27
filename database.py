#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: ClubNet
#-----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy
import os
from datetime import datetime
os.environ['DB_URL']="postgres://oxifvfuc:3Z_OtccJkuJzjE4je2oRnEe3LE47Ksgk@peanut.db.elephantsql.com/oxifvfuc"

Base = sqlalchemy.ext.declarative.declarative_base()
#-----------------------------------------------------------------------
class User (Base):
    __tablename__ = 'users'
    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    profile_image_url = sqlalchemy.Column(sqlalchemy.String)
    class_year = sqlalchemy.Column(sqlalchemy.Integer)
    major = sqlalchemy.Column(sqlalchemy.String)
    team_position = sqlalchemy.Column(sqlalchemy.String)
    favorite_team = sqlalchemy.Column(sqlalchemy.String)
    hometown = sqlalchemy.Column(sqlalchemy.String)
    job_title = sqlalchemy.Column(sqlalchemy.String)
    user_company = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------

class Users_Clubs (Base):
    __tablename__ = 'user_club_id'
    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    club_id = sqlalchemy.Column(sqlalchemy.Integer)

#-----------------------------------------------------------------------

class Posts(Base):
    __tablename__ = 'posts'
    post_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement = True, primary_key = True)
    club_image_url = sqlalchemy.Column(sqlalchemy.String)
    creator_id = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    likes = sqlalchemy.Column(sqlalchemy.Integer)

#-----------------------------------------------------------------------
class Post_Likes(Base):
    __tablename__ = 'likes'
    post_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement = True, primary_key = True)
    user_id = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------

class Requests(Base):
    __tablename__ = 'requests'
    request_timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False), primary_key = True)
    club_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.Integer)

#-----------------------------------------------------------------------
class Admins(Base):
    __tablename__ = 'admins'
    club_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key = True)
    officer_position = sqlalchemy.Column(sqlalchemy.String)


def init_database():
    CLUB_SOCC = 1
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    engine = sqlalchemy.create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    try:
        with sqlalchemy.orm.Session(engine) as session:
            user1 = User(user_id = "allenwu",
                        name = "Allen Wu",
                        email = "allenwu@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668493554/Screen_Shot_2022-11-15_at_1.25.45_AM_si6xir.png")
            session.add(user1)
            user2 = User(user_id = "renteria",
                        name = "Emilio Cano",
                        email = "emiliocanor@princeton.edu",
                        class_year = 2023,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1667797176/renteria_profile_picture.jpg")
            session.add(user2)
            user3 = User(user_id = "yparikh",
                        name = "Yash Parikh",
                        email = "yparikh@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668444358/IMG_4394_hcpx3y.jpg")
                        # profile_image_url = "https://picsum.photos/500/500")
            session.add(user3)
            user4 = User(user_id = "oguntola",
                        name = "Ayo Oguntola",
                        email = "oguntola@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668493633/Screen_Shot_2022-11-15_at_1.26.50_AM_ihanhi.png")
            session.add(user4)
            user5 = User(user_id = "edmo",
                        name = "Ed Mo",
                        email = "ed@princeton.edu",
                        class_year = 2022,
                        profile_image_url = "https://picsum.photos/500/500")
            session.add(user5)
            
            user_clubs1 = Users_Clubs(username = 'allenwu',
                                        club_id = CLUB_SOCC)
            session.add(user_clubs1)
            user_clubs2 = Users_Clubs(username = 'yparikh',
                                        club_id = CLUB_SOCC)
            session.add(user_clubs2)
            user_clubs3 = Users_Clubs(username = 'oguntola',
                                        club_id = CLUB_SOCC)
            session.add(user_clubs3)
            user_clubs4 = Users_Clubs(username = 'renteria',
                                        club_id = CLUB_SOCC)
            session.add(user_clubs4)
            user_clubs5 = Users_Clubs(username = 'edmo',
                                        club_id = CLUB_SOCC)
            session.add(user_clubs5)
            post1 = Posts(creator_id = "yparikh",
                        title = "hello",
                        description = "world",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.now(),
                        status = 0,
                        likes = 0
                        )
            session.add(post1)
            post1 = Posts(creator_id = "oguntola",
                        title = "goat",
                        description = "is ayo",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.now(),
                        status = 1,
                        likes = 0
                        )
            session.add(post1)
            post1 = Posts(creator_id = "renteria",
                        title = "prolly",
                        description = "struggling",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.now(),
                        status = 1,
                        likes = 0
                        )
            session.add(post1)
            admin1 = Admins(user_id = "renteria", club_id = CLUB_SOCC, officer_position = "president")
            session.add(admin1)
            admin2 = Admins(user_id = "yparikh", club_id = CLUB_SOCC, officer_position = "vice president")
            session.add(admin2)
            admin3 = Admins(user_id = "oguntola", club_id = CLUB_SOCC, officer_position = "tres")
            session.add(admin3)
            req1 = Requests(user_id = "tzypman",
                         request_timestamp = datetime.now(),
                         name = "Toby Zypman",
                         year = 2022,
                         club_id = CLUB_SOCC)
            req2 = Requests(user_id = "player2",
                         request_timestamp = datetime.now(),
                         club_id = CLUB_SOCC, name = "Stew Dent", year = 1776)
            session.add(req1)
            session.add(req2)
            session.commit()
    finally:
        engine.dispose()

if __name__ == '__main__':
    init_database()

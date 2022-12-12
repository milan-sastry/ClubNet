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
class Users_info(Base):
    __tablename__ = 'users_info'
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
    notifications = sqlalchemy.Column(sqlalchemy.String)
    industry = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------

class Approved_users(Base):
    __tablename__ = 'approved_users'
    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)

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
    comments = sqlalchemy.Column(sqlalchemy.Integer)

#-----------------------------------------------------------------------
class Post_Likes(Base):
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement = True, primary_key = True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------
class Comments(Base):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement = True, primary_key = True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.String)
    comment = sqlalchemy.Column(sqlalchemy.String)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))

#-----------------------------------------------------------------------

class Requests(Base):
    __tablename__ = 'requests'
    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key = True)

#-----------------------------------------------------------------------
class Admins(Base):
    __tablename__ = 'admins'
    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key = True)
    officer_position = sqlalchemy.Column(sqlalchemy.String)


def init_database():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    print("This will reset the ENTIRE database, including \ninformation from all existing users. \nAre you SURE you would like to proceed? \n[if so, type 'Yes!!!']")
    line = input()

    if line != 'Yes!!!':
        print("Execution cancelled.")
        return

    engine = sqlalchemy.create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    print("Database reset")
    Base.metadata.create_all(engine)

    try:
        with sqlalchemy.orm.Session(engine) as session:
            user1 = Users_info(user_id = "allenwu",
                        name = "Allen Wu",
                        email = "allenwu@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668493554/Screen_Shot_2022-11-15_at_1.25.45_AM_si6xir.png",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user1)
            user2 = Users_info(user_id = "renteria",
                        name = "Emilio Cano",
                        email = "emiliocanor@princeton.edu",
                        class_year = 2023,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1667797176/renteria_profile_picture.jpg",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user2)
            user3 = Users_info(user_id = "yparikh",
                        name = "Yash Parikh",
                        email = "yparikh@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668444358/IMG_4394_hcpx3y.jpg",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user3)
            user4 = Users_info(user_id = "oguntola",
                        name = "Ayo Oguntola",
                        email = "oguntola@princeton.edu",
                        class_year = 2024,
                        profile_image_url = "https://res.cloudinary.com/clubnet/image/upload/v1668493633/Screen_Shot_2022-11-15_at_1.26.50_AM_ihanhi.png",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user4)
            user5 = Users_info(user_id = "edmo",
                        name = "Ed Mo",
                        email = "chitrap@princeton.edu",
                        class_year = 2022,
                        profile_image_url = "https://picsum.photos/500/500",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user5)
            user6 = Users_info(user_id = "tzypman",
                        name = "Toby Zypman",
                        email = "abcdefg@gmail.com",
                        class_year = 2022,
                        profile_image_url = "https://picsum.photos/500/500",
                        major = "",
                        industry = "",
                        notifications = True)
            session.add(user6)
            user6 = Users_info(user_id = "player2",
                        name = "Stew Dent",
                        email = "abc@gmail.com",
                        class_year = 2020,
                        profile_image_url = "https://picsum.photos/500/500",
                        major = "",
                        industry = "",
                        notifications = False)
            session.add(user6)
            app_user1 = Approved_users(user_id = 'allenwu')
            session.add(app_user1)
            app_user2 = Approved_users(user_id = 'yparikh')
            session.add(app_user2)
            app_user3 = Approved_users(user_id = 'oguntola')
            session.add(app_user3)
            app_user4 = Approved_users(user_id = 'renteria')
            session.add(app_user4)
            app_user5 = Approved_users(user_id = 'edmo')
            session.add(app_user5)
            post1 = Posts(creator_id = "yparikh",
                        title = "hello",
                        description = "world",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.now(),
                        status = 0,
                        likes = 0,
                        comments = 0
                        )
            session.add(post1)
            post1 = Posts(creator_id = "oguntola",
                        title = "This post was already there",
                        description = "created by ayo",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.fromtimestamp(1670727192),
                        status = 1,
                        likes = 0,
                        comments = 0
                        )
            session.add(post1)
            post1 = Posts(creator_id = "renteria",
                        title = "Another post",
                        description = "this time by emilio",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.fromtimestamp(1670627192),
                        status = 1,
                        likes = 0,
                        comments = 0
                        )
            session.add(post1)
            post1 = Posts(creator_id = "edmo",
                        title = "Alumni Post",
                        description = "testing some comments stuff",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.fromtimestamp(1670527192),
                        status = 1,
                        likes = 0,
                        comments = 0
                        )
            session.add(post1)
            for i in range(1):
                post1 = Posts(creator_id = "edmo",
                        title = "Alumni Post",
                        description = "testing some comments stuff",
                        club_image_url = "https://picsum.photos/500/500",
                        timestamp = datetime.fromtimestamp(1670827192 - (i*1000000)),
                        status = 1,
                        likes = 0,
                        comments = 0
                        )
                session.add(post1)
            admin1 = Admins(user_id = "renteria", officer_position = "president")
            session.add(admin1)
            admin2 = Admins(user_id = "yparikh", officer_position = "vice president")
            session.add(admin2)
            admin3 = Admins(user_id = "oguntola", officer_position = "tres")
            session.add(admin3)
            admin4 = Admins(user_id = "allenwu", officer_position = "secretary")
            session.add(admin4)
            req1 = Requests(user_id = "tzypman")
            req2 = Requests(user_id = "player2")
            session.add(req1)
            session.add(req2)
            session.commit()
    finally:
        engine.dispose()

if __name__ == '__main__':
    init_database()

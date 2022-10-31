#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy
import os

#-----------------------------------------------------------------------

DATABASE_URL = os.getenv('DB_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
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
    __tablename__ = "posts"
    post_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement = True, primary_key = True)
    club_image_url = sqlalchemy.Column(sqlalchemy.String)
    creator_id = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))

#-----------------------------------------------------------------------

def init_database():
    CLUB_SOCC = 1

    engine = sqlalchemy.create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        user1 = User(user_id = "allenwu", 
                    name = "Allen Wu", 
                    email = "allenwu@princeton.edu")
        session.add(user1)
        user2 = User(user_id = "renteria", 
                    name = "Emilio Cano", 
                    email = "emiliocanor@princeton.edu")
        session.add(user2)
        user3 = User(user_id = "yparikh", 
                    name = "Yash Parikh", 
                    email = "yparikh@princeton.edu")
        session.add(user3)
        
        user_clubs1 = Users_Clubs(username = 'allenwu',
                                    club_id = CLUB_SOCC)
        session.add(user_clubs1)
        user_clubs2 = Users_Clubs(username = 'yparikh',
                                    club_id = CLUB_SOCC)
        session.add(user_clubs2)
        post1 = Posts(creator_id = "yparikh",
                    title = "hello",
                    description = "world")
        session.add(post1)
        session.commit()


if __name__ == '__main__':
    init_database()
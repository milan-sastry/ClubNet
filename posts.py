import os
import sqlalchemy.ext.declarative
import sqlalchemy
import database
import profile
from datetime import datetime


class Post:

    def __init__(self, db_row):
        self._post_id = db_row.post_id
        self._club_image_url = db_row.club_image_url
        self._creator_id = db_row.creator_id
        self._title = db_row.title
        self._description = db_row.description
        self._timestamp = db_row.timestamp
        self._status = db_row.status

    def get_post_id(self):
        return self._post_id

    def get_image_url(self):
        return self._club_image_url

    def get_creator_id(self):
        return self._creator_id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_timestamp(self):
        return self._timestamp
    
    def get_status(self):
        return self._status

#-----------------------------------------------------------------------

def make_request(post_title, post_description):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            post1 = database.Posts(creator_id="yparikh",
                                title=post_title,
                                description=post_description,
                                club_image_url="https://www.princeton.edu/~clubsocc/img/team_main.jpeg",
                                timestamp=datetime.now(),
                                status = 0)
            session.add(post1)
            session.commit()
            session.refresh(post1)
            return post1.post_id
    finally:
        engine.dispose()


def get_posts():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Posts).filter(database.Posts.status == 1)
            # print(query)
            table = query.all()
            list = []
            for row in table:
                # print(row)
                post = Post(row)
                user = profile.get_profile_from_id(post._creator_id)
                list.append({"post": post, "user": user})
            session.commit()
            return list
    finally:
        engine.dispose()

def add_image(post_id, post_img_url):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # print(post_netid)
            print(post_id)
            query = session.query(database.Posts).filter(
                    database.Posts.post_id == post_id)
            row = query.one()
            row.club_image_url = post_img_url
            print(post_img_url)
            session.commit()
    finally:
        engine.dispose()

def get_requests():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Posts).filter(database.Posts.status == 0)
            # print(query)
            table = query.all()
            list = []
            for row in table:
                # print(row)
                post = Post(row)
                user = profile.get_profile_from_id(post._creator_id)
                list.append(post)
            session.commit()
            return list
    finally:
        engine.dispose()

def approve_request(post_id):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # print(post_netid)
            print(post_id)
            query = session.query(database.Posts).filter(
                    database.Posts.post_id == post_id)
            row = query.one()
            row.status = 1
            session.commit()
    finally:
        engine.dispose()
    
def reject_request(post_id):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    delete_post(post_id)

def delete_post(post_id):
    DATABASE_URL = os.getenv('DB_URL')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # print(post_netid)
            print(post_id)
            stmt = sqlalchemy.delete(database.Posts).where((database.Posts.post_id == post_id))
            session.execute(stmt)
            session.commit()
            print("deleted")
    finally:
        engine.dispose()


# -----------------------------------------------------------------------

# For testing:
def _test():
    add_image(1, "https://res.cloudinary.com/clubnet/image/upload/v1668410349/gfcmsvzylqxuumuqpmhy.png")
    print(get_posts())

if __name__ == '__main__':
    _test()

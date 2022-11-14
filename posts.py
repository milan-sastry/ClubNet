import os
import sqlalchemy.ext.declarative
import sqlalchemy
import database


class Post:

    def __init__(self, db_row):
        self._post_id = db_row.post_id
        self._club_image_url = db_row.club_image_url
        self._creator_id = db_row.creator_id
        self._title = db_row.title
        self._description = db_row.description
        self._timestamp = db_row.timestamp
    
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

# -----------------------------------------------------------------------

def make_posts(text):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            post1 = database.Posts(creator_id="yparikh",
                                title="hello",
                                description=text,
                                club_image_url="https://www.princeton.edu/~clubsocc/img/team_main.jpeg")
            session.add(post1)
            session.commit()
            print("added to database")
    finally:
        engine.dispose()


def get_posts():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Posts)
            # print(query)
            table = query.all()
            list = []
            for row in table:
                # print(row)
                post = Post(row)
                list.append(post)
            session.commit()
            return list
    finally:
        engine.dispose()

# -----------------------------------------------------------------------

# For testing:
def _test():
    make_posts("yoooooo")
    # print("made a post")
    get_posts()


if __name__ == '__main__':
    _test()

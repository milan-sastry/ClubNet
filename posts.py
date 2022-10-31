import os
import sqlalchemy.ext.declarative
import sqlalchemy
import database


#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def make_posts(text):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    with sqlalchemy.orm.Session(engine) as session:
        post1 = database.Posts(creator_id = "yparikh",
                    title = "hello",
                    description = text)
        session.add(post1)
        session.commit()
        print("added to database")

def get_posts():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)
    with sqlalchemy.orm.Session(engine) as session:
        # print("im getting this username of " + username)
        query = session.query(database.Posts)
        print(query)
        table = query.all()
        list = []
        for row in table:
            print(row.__dict__)
            list.append(row)
        return list



#-----------------------------------------------------------------------

# For testing:
def _test():
    make_posts("yoooooo")
    print("made a post")
    get_posts()


if __name__ == '__main__':
    _test()

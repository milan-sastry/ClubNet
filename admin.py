import os
import sqlalchemy.ext.declarative
import sqlalchemy
import database
from sqlalchemy import delete


#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# test this
# add in a login to the invalidated
# and then figure out the button stuff so they are actually clickable
def delete_request(user_id, club_id):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)

    with sqlalchemy.orm.Session(engine) as session:
        stmt = delete(database.Requests).where(database.Requests.user_id == user_id)
        session.commit()
        print("deleted")

def approve_request(user_id, club_id):
    delete_request(user_id, club_id)
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = sqlalchemy.create_engine(DATABASE_URL)

    with sqlalchemy.orm.Session(engine) as session:
        validatedUser = database.Users_Clubs(username = "yparikh",
                    club_id = 1)
        session.add(validatedUser)
        session.commit()
        print("added to database")

def get_requests():
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


    engine = sqlalchemy.create_engine(DATABASE_URL)
    with sqlalchemy.orm.Session(engine) as session:
        query = session.query(database.Requests)
        table = query.all()
        list = []
        for row in table:
            print(row.__dict__)
            list.append(row)
        return list



#-----------------------------------------------------------------------

# For testing:
def _test():
    print(get_requests())
    delete_request("yparikh",1)
    print(get_requests())


if __name__ == '__main__':
    _test()

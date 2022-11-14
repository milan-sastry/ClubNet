import os
import sqlalchemy.ext.declarative
import sqlalchemy
import database
from datetime import datetime
from sqlalchemy import delete


class Request:
    def __init__(self, row):
        self._request_timestamp = row.request_timestamp
        self._club_id = row.club_id
        self._user_id = row.user_id
        self._name = row.name
        self._year = row.year

    def get_request_timestamp(self):
        return self._request_timestamp
    
    def get_club_id(self):
        return self._club_id
    
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name
    
    def get_year(self):
        return self._year


#-----------------------------------------------------------------------
DATABASE_URL = os.getenv('DB_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
#-----------------------------------------------------------------------

# test this
# add in a login to the invalidated
# and then figure out the button stuff so they are actually clickable
# fix navbar information
def delete_request(user_id, club_id):
    if user_id is None:
        return
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            stmt = delete(database.Requests).where((database.Requests.user_id == user_id)&(database.Requests.club_id == club_id))
            session.execute(stmt)
            session.commit()
            print("deleted")
    finally:
        engine.dispose()

def approve_request(user_id, club_id):
    if user_id is None:
        return

    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            validatedUser = database.Users_Clubs(username = user_id,
                        club_id = club_id)
            session.add(validatedUser)
            session.commit()
            print("added to database")
        
        delete_request(user_id, club_id)
    finally:
        engine.dispose()

def get_requests():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Requests)
            table = query.all()
            list = []
            for row in table:
                user = Request(row)
                list.append(user)
            return list
    finally:
        engine.dispose()
    
def create_request(user_id, club_id):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if check_request(user_id, club_id):
                print("request already exists")
                return 
            else:
                new_user = database.User(user_id = user_id)
                new_request = database.Requests(request_timestamp = datetime.now(), user_id = user_id, club_id = club_id)
                session.add(new_user)
                session.add(new_request)
                session.commit()
                print("Request added")
                return
    finally:
        engine.dispose()

def check_request(user_id, club_id):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Requests).where((database.Requests.user_id == user_id)&(database.Requests.club_id == club_id))
        
            if query.first() is not None:
                print(f"request already exists for {user_id}")
                return True
            else:
                print(f'no request for {user_id}')
                return False
    finally:
        engine.dispose()

def is_admin(user_id, club_id):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Admins).where((database.Admins.user_id == user_id)&(database.Admins.club_id == club_id))
            if query.first() is not None:
                return True
            else:
                return False
    finally:
        engine.dispose()

#-----------------------------------------------------------------------

# For testing:
def _test():
    print(get_requests())
    approve_request('yparikh',1)
    print(get_requests())


if __name__ == '__main__':
    _test()

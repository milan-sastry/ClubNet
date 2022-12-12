import sqlalchemy.ext.declarative
import sqlalchemy
import database
import profiles
from sqlalchemy import delete

class Administrator:
    def __init__(self, row):
        self.user_id = row.user_id
        self.officer_position = row.officer_position
        self.name = row.name
        self.email = row.email
    
    def get_user_id(self):
        return self.user_id

    def get_officer_position(self):
        return self.officer_position

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

class Request:
    def __init__(self, row):
        self._user_id = row[0]
        self._name = row[1]
        self._year = row[3]
        self._email = row[2]
    
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name
    
    def get_year(self):
        return self._year
    
    def get_email(self):
        return self._email

# test this
# add in a login to the invalidated
# and then figure out the button stuff so they are actually clickable
# fix navbar information
def delete_request(engine, user_id):
    if user_id is None:
        return
    with sqlalchemy.orm.Session(engine) as session:
            stmt = delete(database.Requests).where(database.Requests.user_id == user_id)
            session.execute(stmt)
            session.commit()
            print("deleted")

def approve_request(engine, user_id):
    if user_id is None:
        return
    with sqlalchemy.orm.Session(engine) as session:
            validatedUser = database.Approved_users(user_id = user_id)
            session.add(validatedUser)
            session.query(database.Users_info).filter(database.Users_info.user_id == user_id).update({
                    "notifications": True,
            })
            session.commit()
            print("added to database")
    delete_request(engine, user_id)


def get_requests(engine):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Requests.user_id, database.Users_info.name, database.Users_info.email, database.Users_info.class_year).filter(database.Requests.user_id == database.Users_info.user_id)
            print(query)
            table = query.all()
            list = []
            for row in table:
                print(row)
                user = Request(row)
                list.append(user)
            return list
    
def create_request(engine, user_id):
    
    if check_request(engine, user_id):
        print('request already exists for {user_id}')
        return 

    with sqlalchemy.orm.Session(engine) as session:
        new_request = database.Requests(user_id = user_id)
        session.add(new_request)
        session.commit()
        print('Request added for {user_id}')
        return

def check_request(engine, user_id):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Requests).where(database.Requests.user_id == user_id)
        
            if query.first() is not None:
                print(f"request already exists for {user_id}")
                return True
            else:
                print(f'no request for {user_id}')
                return False

def is_admin(engine, user_id):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Admins).where(database.Admins.user_id == user_id)
            if query.first() is not None:
                return True
            else:
                return False

def make_admin(engine, user_id, officer_position):
    if not profiles.validate(engine, user_id):
        print(f"user {user_id} is not in club")
        return
    if is_admin(engine, user_id):
        print(f"user {user_id} is already admin for club")
        return
    new_admin = database.Admins(user_id = user_id, officer_position = officer_position)
    with sqlalchemy.orm.Session(engine) as session:
            session.add(new_admin)
            session.commit()

def remove_admin(engine, user_id):
    if not is_admin(engine, user_id):
        print(f"user {user_id} is not admin for club")
        return
    with sqlalchemy.orm.Session(engine) as session:
            stmt = delete(database.Admins).where(database.Admins.user_id == user_id)
            session.execute(stmt)
            session.commit()

def remove_user(engine, user_id):
    if not profiles.validate(engine, user_id):
        print(f"user {user_id} is not in club")
        return
    remove_admin(engine, user_id)
    with sqlalchemy.orm.Session(engine) as session:
            stmt = delete(database.Approved_users).where((database.Approved_users.user_id == user_id))
            session.execute(stmt)
            session.commit()

def get_request_email(engine, user_id):
    with sqlalchemy.orm.Session(engine) as session:
        query = session.query(database.Users_info.email).filter(database.Users_info.user_id == user_id)
        table = query.one()
        print(table[0])
        return table[0]

def get_admins(engine):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Admins.user_id, database.Users_info.name, database.Users_info.email, database.Admins.officer_position).filter(database.Admins.user_id == database.Users_info.user_id)
            table = query.all()
            list = []
            for row in table:
                admin = Administrator(row)
                list.append(admin)
            session.commit()
            return list

#-----------------------------------------------------------------------

# For testing:
def _test():
    print(get_requests())
    approve_request('yparikh')
    print(get_requests())
    print(get_admins())


if __name__ == '__main__':
    _test()

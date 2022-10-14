import os
import sqlalchemy.ext.declarative
import sqlalchemy


#-----------------------------------------------------------------------

DATABASE_URL = os.getenv('DB_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

Base = sqlalchemy.ext.declarative.declarative_base()

class Users_Clubs (Base):
    __tablename__ = 'user_club_id'
    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    club_id = sqlalchemy.Column(sqlalchemy.Integer)

engine = sqlalchemy.create_engine(DATABASE_URL)

#-----------------------------------------------------------------------

def get_club_sports(username):

    users = []
    with sqlalchemy.orm.Session(engine) as session:
        query = session.query(Users_Clubs).filter(
            Users_Clubs.username.ilike(username))
        print(query)
        table = query.all()
        for row in table:
            print(row.club_id)
            users.append(row)

    return users

#-----------------------------------------------------------------------

# For testing:

def _test():
    books = get_club_sports('yparikh')

if __name__ == '__main__':
    _test()

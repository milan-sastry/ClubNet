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

def get_club_status(username, club_id):

    bool = False
    with sqlalchemy.orm.Session(engine) as session:
        print("im getting this username of " + username)
        query = session.query(Users_Clubs).filter(
            Users_Clubs.username.ilike(username))
        print(query)
        table = query.all()
        for row in table:
            print("USER " + row.username + "OKAY " + str(row.club_id))
            if (row.club_id == club_id):
                print("yeah that's a hit for " + username)
                return True

    return bool

#-----------------------------------------------------------------------

# For testing:
def _test():
    isInClub = get_club_status("yparikh", 1)
    if isInClub:
        print("yeah he's that club")


if __name__ == '__main__':
    _test()

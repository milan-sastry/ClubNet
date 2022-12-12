import sqlalchemy.ext.declarative
import sqlalchemy
from flask_sqlalchemy import Pagination
from sqlalchemy import delete
import database
import profiles
from datetime import datetime
import math
class Post:

    def __init__(self, db_row):
        self._post_id = db_row.post_id
        self._club_image_url = db_row.club_image_url
        self._creator_id = db_row.creator_id
        self._title = db_row.title
        self._description = db_row.description
        self._timestamp = db_row.timestamp
        self._status = db_row.status
        self._likes = db_row.likes
        self._comments = db_row.comments

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

    def get_likes(self):
        return self._likes

    def get_comments(self):
        return self._comments

class Comment:

    def __init__(self, db_row):
        self._id = db_row.id
        self._post_id = db_row.post_id
        self._user_id = db_row.user_id
        self._comment = db_row.comment
        self._timestamp = db_row.timestamp

    def get_id(self):
        return self._id

    def get_post_id(self):
        return self._post_id

    def get_user_id(self):
        return self._user_id

    def get_comment(self):
        return self._comment

    def get_timestamp(self):
        return self._timestamp

#-----------------------------------------------------------------------

def make_request(engine, post_title, post_description, user_id):
    with sqlalchemy.orm.Session(engine) as session:
            post1 = database.Posts(creator_id=user_id,
                                title=post_title,
                                description=post_description,
                                club_image_url="https://www.princeton.edu/~clubsocc/img/team_main.jpeg",
                                timestamp=datetime.now(),
                                status = 0,
                                likes = 0,
                                comments = 0)
            session.add(post1)
            session.commit()
            return post1.post_id

def paginate(data, page, per_page):
    # Based on page and per_page info, calculate start and end index of items to keep
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Get the paginated list of items
    items = data[start_index:end_index]

    # Create Pagination object
    return Pagination(None, page, per_page, len(data), items)

def get_posts(engine, user_id, filter=None, page=1, total_rows=False):
    with sqlalchemy.orm.Session(engine) as session:
            num_rows = session.query(database.Posts).count()
            query = session.query(database.Posts).filter(database.Posts.status == 1).order_by(database.Posts.timestamp.desc()).limit(5).offset((page - 1) * 5)
            table = query.all()
            list = []
            for row in table:
                # print(row)
                post = Post(row)
                user = profiles.get_profile_from_id(engine, post._creator_id, session)
                isLiked = len(session.query(database.Post_Likes).filter(database.Post_Likes.post_id == post._post_id and database.Post_Likes.user_id == user_id).all()) > 0
                comment_query = session.query(database.Comments).filter(database.Comments.post_id == post._post_id).order_by(database.Comments.timestamp.asc())
                comments_response = comment_query.all()
                comments = []
                for com in comments_response:
                    my_comment = Comment(com)
                    comment_user = profiles.get_profile_from_id(engine, my_comment._user_id, session)
                    comments.append({"comment": my_comment, "user": comment_user})
                if filter:
                    if filter == "members":
                        if user.get_class_year() > 2022:
                            list.append({"post": post, "user": user, "isLiked": isLiked, "comments": comments})
                    else:
                        if user.get_class_year() < 2023:
                            list.append({"post": post, "user": user, "isLiked": isLiked, "comments": comments})
                else:
                    list.append({"post": post, "user": user, "isLiked": isLiked, "comments": comments})
            session.commit()
            if total_rows:
                return list, math.ceil(num_rows / 5)
            else:
                return list

def add_image(engine, post_id, post_img_url):
    with sqlalchemy.orm.Session(engine) as session:
            # print(post_netid)
            print(post_id)
            query = session.query(database.Posts).filter(
                    database.Posts.post_id == post_id)
            row = query.one()
            row.club_image_url = post_img_url
            print(post_img_url)
            session.commit()

def get_post_requests(engine):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Posts).filter(database.Posts.status == 0)
            table = query.all()
            list = []
            for row in table:
                post = Post(row)
                list.append(post)
            session.commit()
            return list

def approve_post_request(engine, post_id):
    with sqlalchemy.orm.Session(engine) as session:
            # print(post_netid)
            print(post_id)
            query = session.query(database.Posts).filter(
                    database.Posts.post_id == post_id)
            row = query.one()
            row.status = 1
            session.commit()

def reject_request(engine, post_id):
    delete_post(engine, post_id)

def delete_post(engine, post_id):
    with sqlalchemy.orm.Session(engine) as session:
            print(post_id)
            stmt = sqlalchemy.delete(database.Posts).where((database.Posts.post_id == post_id))
            session.execute(stmt)
            session.commit()
            print("deleted")

def like(engine, post_id, user_id):
    with sqlalchemy.orm.Session(engine) as session:
            response = session.query(database.Post_Likes).filter(database.Post_Likes.post_id == post_id and database.Post_Likes.user_id == user_id).all()
            if len(response) == 0:
                session.query(database.Posts).filter(database.Posts.post_id == post_id).update({
                    "likes": database.Posts.likes + 1,
                })
                post_like = database.Post_Likes(post_id=post_id, user_id=user_id)
                session.add(post_like)
                session.commit()
            return True

def unlike(engine, post_id, user_id):
    with sqlalchemy.orm.Session(engine) as session:
            response = session.query(database.Post_Likes).filter(database.Post_Likes.post_id == post_id and database.Post_Likes.user_id == user_id).all()
            if len(response) != 0:
                stmt = delete(database.Post_Likes).where((database.Post_Likes.user_id == user_id)&(database.Post_Likes.post_id == post_id))
                session.execute(stmt)
                session.query(database.Posts).filter(database.Posts.post_id == post_id).update({
                    "likes": database.Posts.likes - 1,
                })
                session.commit()

            return True

def comment(engine, post_id, net_id, comment):
    with sqlalchemy.orm.Session(engine) as session:
            session.query(database.Posts).filter(database.Posts.post_id == post_id).update({
                "comments": database.Posts.comments + 1,
            })
            post_comment = database.Comments(post_id=post_id, user_id=net_id, comment=comment, timestamp=datetime.now())
            session.add(post_comment)
            session.commit()
            session.refresh(post_comment) #sus
            return True

# this function is never used btw
def get_post_by_id(engine, post_id):
    with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.Posts).filter(database.Posts.post_id == post_id)
            # print(query)
            table = query.all()
            for row in table:
                # print(row)
                post = Post(row)
            session.commit()
            return post

#-----------------------------------------------------------------------

# For testing:
def _test():
    # add_image(1, "https://res.cloudinary.com/clubnet/image/upload/v1668410349/gfcmsvzylqxuumuqpmhy.png")
    for item in get_posts():
        print(item['post'].get_timestamp())
    print(get_posts())

if __name__ == '__main__':
    _test()

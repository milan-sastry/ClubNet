import cloudinary
import os
import cloudinary.uploader
import cloudinary.api
import sqlalchemy.orm
import sqlalchemy
import database

def add_image(post_netid, post_img_url):
    DATABASE_URL = os.getenv('DB_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    CLOUDINARY_URL =  os.getenv('CLOUDINARY_URL')
    config = cloudinary.config(secure=True)

    # upload an image
    netid = post_netid
    public_id = netid + "_profile_picture"
    cloudinary.uploader.upload(post_img_url, public_id = public_id, overwrite = True)

    # save the url
    img_url = cloudinary.CloudinaryImage(public_id).build_url()
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(database.User).filter(
                    database.User.user_id.ilike(netid))
            row = query.one()
            row.profile_image_url = img_url
            return img_url
            session.commit()
    finally:
        engine.dispose()

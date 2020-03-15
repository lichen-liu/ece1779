from common_lib import s3, database, utility

def delete_photo_from_s3_and_database(photo_id, photo_name):
    saved_photo_file_name = str(photo_id) + utility.get_file_extension(photo_name)
    photo_s3_key = s3.PHOTOS_DIR + saved_photo_file_name
    thumbnail_s3_key = s3.THUMBNAILS_DIR + saved_photo_file_name
    rectangle_s3_key = s3.RECTANGLES_DIR + saved_photo_file_name

    s3.delete_object(key=photo_s3_key)
    s3.delete_object(key=thumbnail_s3_key)
    s3.delete_object(key=rectangle_s3_key)

    database.delete_photo(photo_id)
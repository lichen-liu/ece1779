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


def delete_all_photos_from_s3_and_database():
    print('Deleting Table ece1779.photo ...')
    database.delete_photo_table()
    print('    Succeeded')

    print('Deleting ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' ...')
    s3.delete_directory_content(directory=s3.ROOT_DIR)
    s3.create_directories_if_necessary()
    print('    Succeeded')


def delete_everything_from_s3_and_database():
    print('Deleting ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' ...')
    s3.delete_directory_content(directory=s3.ROOT_DIR)
    s3.create_directories_if_necessary()
    print('    Succeeded')

    print('Dropping Schema ece1779 ...')
    database.drop_schema()
    print('    Succeeded')

    print('Creating Schema ece1779 ...')
    database.create_schema()
    print('    Succeeded')
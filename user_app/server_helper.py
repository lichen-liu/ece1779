#!venv/bin/python

import shutil
import os
import argparse
import database
import utility
import s3


def delete_data():
    print('Deleting Table Photo ...')
    database.delete_photo_table()
    print('    Succeeded')

    print('Deleting ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' ...')
    s3.delete_directory_content(directory=s3.ROOT_DIR)
    s3.create_directories_if_necessary()
    print('    Succeeded')


def delete_all():
    delete_data()

    print('Deleting Account Photo ...')
    database.delete_account_table()
    print('    Succeeded')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--delete_data', help='Delete all user data (database and S3)', action='store_true')
    parser.add_argument(
        '--delete_all', help='Delete all user data and accounts (database and S3)', action='store_true')
    parser.add_argument(
        '--account_table', help='Print the Account table from the database', action='store_true')
    parser.add_argument(
        '--photo_table', help='Print the Photo table from the database', action='store_true')
    parser.add_argument('--storage_info', help='Print the ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' directory size', action='store_true')

    args = parser.parse_args()

    s3.init()

    if args.delete_data:
        delete_data()
        print()

    if args.delete_all:
        delete_all()
        print()

    if args.account_table:
        print('ACCOUNT TABLE:')
        rows = database.get_account_table()
        for row in rows:
            print(row)
        print()

    if args.photo_table:
        print('PHOTO TABLE:')
        rows = database.get_photo_table()
        for row in rows:
            print(row)
        print()

    if args.storage_info:
        size, num_directory, num_file, _ = s3.get_bucket_content_size(key=s3.ROOT_DIR)
        size_str = utility.convert_bytes_to_human_readable(size)
        print(s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + '  -----  ' + size_str + 
            ' (' + str(num_file) + ' files, ' + str(num_directory) + ' dirs)')
        print()

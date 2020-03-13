#!venv/bin/python

import shutil
import os
import argparse
from common_lib import database, utility, s3


def reset_data():
    print('Deleting Table ece1779.photo ...')
    database.delete_photo_table()
    print('    Succeeded')

    print('Deleting ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' ...')
    s3.delete_directory_content(directory=s3.ROOT_DIR)
    s3.create_directories_if_necessary()
    print('    Succeeded')


def reset_all():
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--reset_data', help='Reset all user data (RDS MySQL and S3)', action='store_true')
    parser.add_argument(
        '--reset_all', help='Reset all user data and accounts (RDS MySQL and S3)', action='store_true')
    parser.add_argument(
        '--account_table', help='Print ece1779.account from the RDS MySQL', action='store_true')
    parser.add_argument(
        '--photo_table', help='Print ece1779.photo from the RDS MySQL', action='store_true')
    parser.add_argument('--storage_info', help='Print the ' + s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + ' directory size', action='store_true')

    args = parser.parse_args()

    s3.create_bucket_if_necessary()

    if args.reset_data:
        reset_data()
        print()

    if args.reset_all:
        reset_all()
        print()

    if args.account_table:
        print('ece1779.account:')
        rows = database.get_account_table()
        for row in rows:
            print(row)
        print()

    if args.photo_table:
        print('ece1779.photo:')
        rows = database.get_photo_table()
        for row in rows:
            print(row)
        print()

    if args.storage_info:
        size, num_directory, num_file = s3.get_bucket_content_size(key=s3.ROOT_DIR)
        size_str = utility.convert_bytes_to_human_readable(size)
        print(s3.get_s3_path_in_string(key=s3.ROOT_DIR, bucket_name=s3.BUCKET) + '  -----  ' + size_str + 
            ' (' + str(num_file) + ' files, ' + str(num_directory) + ' dirs)')
        print()

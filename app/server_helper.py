#!venv/bin/python

import shutil
import os
import argparse
import database, directory, utility


def delete_data():
    print('Deleting Table Photo ...')
    database.delete_photo_table()
    print('    Succeeded')

    print('Deleting ' + directory.get_root_dir_path(True) + ' ...')
    if os.path.exists(directory.get_root_dir_path(True)):
        shutil.rmtree(directory.get_root_dir_path(True))
    print('    Succeeded')


def delete_all():
    delete_data()

    print('Deleting Account Photo ...')
    database.delete_account_table()
    print('    Succeeded')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--delete_data', help='Delete all user data (database and filesystem)', action='store_true')
    parser.add_argument('--delete_all', help='Delete all user data and accounts (database and filesystem)', action='store_true')
    parser.add_argument('--account_table', help='Print the Account table from the database', action='store_true')
    parser.add_argument('--photo_table', help='Print the Photo table from the database', action='store_true')
    parser.add_argument('--storage_info', help='Print the ' + directory.get_root_dir_path(False) + ' directory size', action='store_true')
    
    args = parser.parse_args()
    
    if args.delete_data:
        delete_data()

    if args.delete_all:
        delete_all()

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
        root_dir_path = directory.get_root_dir_path(True)
        size_str = utility.convert_bytes_to_human_readable(utility.get_dir_size(root_dir_path))
        print(root_dir_path + '  -----  ' + size_str)

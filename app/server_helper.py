import shutil
import os
import database, directory


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
    delete_all()
from flask import render_template, redirect, request
from manager_app import webapp
from common_lib import s3, database, utility
import urllib

@webapp.route('/api/table/ece1779_account', methods=['GET'])
def table_ece1779_account_handler():
    table = database.get_account_table()
    return render_table_page(title='ece1779.account', title_row=['id', 'username', 'password_hash', 'salt'], table=table)


@webapp.route('/api/table/ece1779_photo', methods=['GET'])
def table_ece1779_photo_handler():
    table = database.get_photo_table()
    return render_table_page(title='ece1779.photo', title_row=['id', 'account_id', 'name'], table=table)


@webapp.route('/api/table/s3_filesystem', methods=['GET'])
def table_s3_filesystem_handler():
    path=urllib.parse.unquote(request.args.get('key'))
    
    table = s3.list_bucket_content(directory=path, recursive=False)    
    
    size_table = [(row[0], *s3.get_bucket_content_size(key=row[0])[0:3]) for row in table]

    readable_table = [(row[0], utility.convert_bytes_to_human_readable(row[1]), row[2], row[3]) for row in size_table]
    
    return render_table_page(title=path, title_row=['key', 'size', 'num_directory', 'num_file'], table=readable_table,
        description='Total Size: ' + utility.convert_bytes_to_human_readable(s3.get_bucket_content_size(key=path)[0]))


def render_table_page(title, title_row, table, description=None):
    return render_template('table.html', 
        title=title,
        title_row=title_row,
        table=table,
        description=description)
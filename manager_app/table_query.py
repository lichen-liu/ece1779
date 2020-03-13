from flask import render_template, redirect, request, url_for
from manager_app import webapp
from common_lib import s3, database, utility
import urllib


@webapp.route('/api/table/ece1779_account', methods=['GET'])
def table_ece1779_account_handler():
    table = database.get_account_table()
    return render_table_page(title='ece1779.account', title_row=('id', 'username', 'password_hash', 'salt'), table=table)


@webapp.route('/api/table/ece1779_photo', methods=['GET'])
def table_ece1779_photo_handler():
    table = database.get_photo_table()
    return render_table_page(title='ece1779.photo', title_row=('id', 'account_id', 'name'), table=table)


@webapp.route('/api/table/s3_filesystem', methods=['GET'])
def table_s3_filesystem_handler():
    request_key = request.args.get('key')
    if request_key is None:
        request_key = s3.ROOT_DIR
    path=urllib.parse.unquote(request_key)
    
    table = s3.list_bucket_content(directory=path, recursive=False)
    # print(str(table))
    # print(str(s3.get_bucket_content_size(key=path)))

    size_table = [(row[0], *s3.get_bucket_content_size(key=row[0])) for row in table]

    readable_table = [(row[0], utility.convert_bytes_to_human_readable(row[1]), row[2], row[3]) for row in size_table]
    action_handler_assigner_row = (lambda item, _: url_for('table_s3_filesystem_handler', key=urllib.parse.quote(item)) if s3.is_path_s3_directory(item) else None, None, None, None)
    
    return render_table_page(title=path, 
        title_row=('key', 'size', 'num_directory', 'num_file'), action_handler_assigner_row=action_handler_assigner_row,
        table=readable_table, description='Total Size: ' + utility.convert_bytes_to_human_readable(s3.get_bucket_content_size(key=path)[0]))


@webapp.route('/api/table/user_details', methods=['GET'])
def table_user_details_handler():
    account_table = database.get_account_table()
    user_details_table = list()
    
    for account_table_row in account_table:
        account_id, username, _, _ = account_table_row
        account_id = str(account_id)
        
        account_photo_table = database.get_account_photo(account_id)
        
        account_photos_count = 0
        account_photos_size = 0
        account_rectangles_count = 0
        account_rectangles_size = 0
        account_thumbnails_count = 0
        account_thumbnails_size = 0
        
        for account_photo_table_row in account_photo_table:
            photo_id, photo_name = account_photo_table_row
            saved_file_name = str(photo_id) + utility.get_file_extension(photo_name)

            if s3.is_object_existed(key=s3.PHOTOS_DIR + saved_file_name):
                account_photos_count += 1
                account_photos_size += s3.get_bucket_content_size(key=s3.PHOTOS_DIR + saved_file_name)[0]

            if s3.is_object_existed(key=s3.RECTANGLES_DIR + saved_file_name):
                account_rectangles_count += 1
                account_rectangles_size += s3.get_bucket_content_size(key=s3.RECTANGLES_DIR + saved_file_name)[0]

            if s3.is_object_existed(key=s3.THUMBNAILS_DIR + saved_file_name):
                account_thumbnails_count += 1
                account_thumbnails_size += s3.get_bucket_content_size(key=s3.THUMBNAILS_DIR + saved_file_name)[0]

        account_total_count = account_photos_count + account_rectangles_count + account_thumbnails_count
        account_total_size = account_photos_size + account_rectangles_size + account_thumbnails_size

        user_details_table.append(
            (account_id, username, 
            len(account_photo_table), account_total_count, utility.convert_bytes_to_human_readable(account_total_size),
            account_photos_count, utility.convert_bytes_to_human_readable(account_photos_size),
            account_rectangles_count, utility.convert_bytes_to_human_readable(account_rectangles_size),
            account_thumbnails_count, utility.convert_bytes_to_human_readable(account_thumbnails_size)))
    
    title_rows = ('account_id', 'username', 
        'num_photos', 'total_num_files', 'total_size',
        'num_photos_files', 'photos_size',
        'num_rectangles_files', 'rectangles_size',
        'num_thumbnails_files', 'thumbnails_size')

    ahs_account_id = lambda item, _: url_for('table_ece1779_account_handler', find_key='id', find_value=urllib.parse.quote(item))
    ahs_username = lambda item, _: url_for('table_ece1779_account_handler', find_key='username', find_value=urllib.parse.quote(item))
    ahs_num_photos = lambda item, row: url_for('table_ece1779_photo_handler', find_key='account_id', find_value=row[0])
    action_handler_assigner_row=(ahs_account_id, ahs_username, 
        ahs_num_photos, None, None,
        None, None,
        None, None,
        None, None)
    
    return render_table_page(title='User Details', title_row=title_rows, action_handler_assigner_row=action_handler_assigner_row, table=user_details_table)


def render_table_page(title, title_row, table, action_handler_assigner_row=None, description=None):
    '''
    :param action_handler_assigner_row: [lanbda item, row: GET_URL, None]
    '''
    if action_handler_assigner_row:
        assert(len(title_row) == len(action_handler_assigner_row))
    
    find_key = request.args.get('find_key')
    find_value = request.args.get('find_value')
    if find_key and find_value:
        find_key = urllib.parse.unquote(find_key)
        find_value = urllib.parse.unquote(find_value)
        assert(find_key in title_row)
        col_idx = title_row.index(find_key)
        table = list(filter(lambda row: str(row[col_idx]) == find_value, iter(table)))

    return render_template('table.html', 
        title=title,
        title_row=title_row,
        table=table,
        action_handler_assigner_row=action_handler_assigner_row,
        description=description)
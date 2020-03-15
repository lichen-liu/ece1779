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
    # {account_id: dict(key='username', 'num_photos', 'num_photos_files', 'photos_size', 'num_rectangles_files', 'rectangles_size', 'num_thumbnails_files', 'thumbnails_size')}
    user_details_dict = {row[0]: 
        {'username':row[1], 'num_photos_files':0, 'photos_size':0, 'num_rectangles_files':0, 'rectangles_size':0, 'num_thumbnails_files':0, 'thumbnails_size':0, 'num_photos':0} 
        for row in database.get_account_table()}
    for photo_table_row in database.get_photo_table():
        photo_id, account_id, photo_name = photo_table_row
        saved_file_name = str(photo_id) + utility.get_file_extension(photo_name)

        user_entry = user_details_dict[account_id]

        photo_size, _, photo_num_file = s3.get_bucket_content_size(key=s3.PHOTOS_DIR + saved_file_name)
        if photo_num_file == 1:
            user_entry['num_photos_files'] += 1
            user_entry['photos_size'] += photo_size

        rectangle_size, _, rectangle_num_file = s3.get_bucket_content_size(key=s3.RECTANGLES_DIR + saved_file_name)
        if rectangle_num_file == 1:
            user_entry['num_rectangles_files'] += 1
            user_entry['rectangles_size'] += rectangle_size

        thumbnail_size, _, thumbnail_num_file = s3.get_bucket_content_size(key=s3.THUMBNAILS_DIR + saved_file_name)
        if thumbnail_num_file == 1:
            user_entry['num_thumbnails_files'] += 1
            user_entry['thumbnails_size'] += thumbnail_size

        user_entry['num_photos'] += 1

    # 'account_id', 'username', 'num_photos', 'total_num_files', 'total_size', 'num_photos_files', 'photos_size', 'num_rectangles_files', 'rectangles_size', 'num_thumbnails_files', 'thumbnails_size'
    user_details_table = list()
    for user_details_dict_row in user_details_dict.items():
        account_id, user_entry = user_details_dict_row

        total_num_files = user_entry['num_photos_files'] + user_entry['num_rectangles_files'] + user_entry['num_thumbnails_files']
        total_size = user_entry['photos_size'] + user_entry['rectangles_size'] + user_entry['thumbnails_size']

        user_details_table.append((str(account_id), user_entry['username'], 
            user_entry['num_photos'], total_num_files, utility.convert_bytes_to_human_readable(total_size),
            user_entry['num_photos_files'], utility.convert_bytes_to_human_readable(user_entry['photos_size']),
            user_entry['num_rectangles_files'], utility.convert_bytes_to_human_readable(user_entry['rectangles_size']),
            user_entry['num_thumbnails_files'], utility.convert_bytes_to_human_readable(user_entry['thumbnails_size'])))
    
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
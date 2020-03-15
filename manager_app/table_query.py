from flask import render_template, redirect, request, url_for
from manager_app import webapp
from common_lib import s3, database, utility, combined_aws
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
    action_handler_assigner_row = (lambda item, _: url_for('table_s3_filesystem_handler', key=item) if s3.is_path_s3_directory(item) else None, None, None, None)
    
    return render_table_page(title=path, 
        title_row=('key', 'size', 'num_directory', 'num_file'), action_handler_assigner_row=action_handler_assigner_row,
        table=readable_table, description='Total Size: ' + utility.convert_bytes_to_human_readable(s3.get_bucket_content_size(key=path)[0]))


@webapp.route('/api/table/user_details', methods=['GET'])
def table_user_details_handler():
    description = request.args.get('description')
    if description:
        description = urllib.parse.unquote(description)

    # {userid: dict(key='username', 'num_photos', 'num_photos_files', 'photos_size', 'num_rectangles_files', 'rectangles_size', 'num_thumbnails_files', 'thumbnails_size')}
    user_details_dict = {row[0]: 
        {'username':row[1], 'num_photos_files':0, 'photos_size':0, 'num_rectangles_files':0, 'rectangles_size':0, 'num_thumbnails_files':0, 'thumbnails_size':0, 'num_photos':0} 
        for row in database.get_account_table()}

    s3_photos_list = {row[0]: row[1] for row in s3.list_bucket_content(directory=s3.PHOTOS_DIR, recursive=False)}
    s3_rectangles_list = {row[0]: row[1] for row in s3.list_bucket_content(directory=s3.RECTANGLES_DIR, recursive=False)}
    s3_thumbnails_list = {row[0]: row[1] for row in s3.list_bucket_content(directory=s3.THUMBNAILS_DIR, recursive=False)}

    for photo_table_row in database.get_photo_table():
        photo_id, userid, photo_name = photo_table_row
        saved_file_name = str(photo_id) + utility.get_file_extension(photo_name)

        user_entry = user_details_dict[userid]

        photo_size = s3_photos_list.get(s3.PHOTOS_DIR + saved_file_name)
        if photo_size:
            user_entry['num_photos_files'] += 1
            user_entry['photos_size'] += photo_size

        rectangle_size = s3_rectangles_list.get(s3.RECTANGLES_DIR + saved_file_name)
        if rectangle_size:
            user_entry['num_rectangles_files'] += 1
            user_entry['rectangles_size'] += rectangle_size

        thumbnail_size = s3_thumbnails_list.get(s3.THUMBNAILS_DIR + saved_file_name)
        if thumbnail_size:
            user_entry['num_thumbnails_files'] += 1
            user_entry['thumbnails_size'] += thumbnail_size

        user_entry['num_photos'] += 1

    # 'userid', 'username', 'num_photos', 'total_num_files', 'total_size', 'num_photos_files', 'photos_size', 'num_rectangles_files', 'rectangles_size', 'num_thumbnails_files', 'thumbnails_size'
    user_details_table = list()
    for user_details_dict_row in user_details_dict.items():
        userid, user_entry = user_details_dict_row

        total_num_files = user_entry['num_photos_files'] + user_entry['num_rectangles_files'] + user_entry['num_thumbnails_files']
        total_size = user_entry['photos_size'] + user_entry['rectangles_size'] + user_entry['thumbnails_size']

        user_details_table.append((str(userid), user_entry['username'], 
            user_entry['num_photos'], total_num_files, utility.convert_bytes_to_human_readable(total_size),
            user_entry['num_photos_files'], utility.convert_bytes_to_human_readable(user_entry['photos_size']),
            user_entry['num_rectangles_files'], utility.convert_bytes_to_human_readable(user_entry['rectangles_size']),
            user_entry['num_thumbnails_files'], utility.convert_bytes_to_human_readable(user_entry['thumbnails_size']),
            'Delete'))
    
    title_rows = ('userid', 'username', 
        'num_photos', 'total_num_files', 'total_size',
        'num_photos_files', 'photos_size',
        'num_rectangles_files', 'rectangles_size',
        'num_thumbnails_files', 'thumbnails_size', 'Delete User Photo')

    ahs_userid = lambda item, _: url_for('table_ece1779_account_handler', find_key='id', find_value=item)
    ahs_username = lambda item, _: url_for('table_ece1779_account_handler', find_key='username', find_value=item)
    ahs_num_photos = lambda item, row: url_for('table_ece1779_photo_handler', find_key='account_id', find_value=row[0])
    ahs_delete_user_photo = lambda _, row: url_for('table_delete_user_photos_handler', userid=row[0])
    action_handler_assigner_row=(ahs_userid, ahs_username, 
        ahs_num_photos, None, None,
        None, None,
        None, None,
        None, None, ahs_delete_user_photo)
    
    return render_table_page(title='User Details', title_row=title_rows, action_handler_assigner_row=action_handler_assigner_row, table=user_details_table, description=description)


@webapp.route('/api/table/delete_user_photos', methods=['GET'])
def table_delete_user_photos_handler():
    userid = request.args.get('userid')
    account_photo_table = database.get_account_photo(userid)
    if account_photo_table:
        for account_photo_row in account_photo_table:
            photo_id, photo_name = account_photo_row
            combined_aws.delete_photo_from_s3_and_database(photo_id, photo_name)
        description='Successfully deleted all {} photos from userid <{}>!'.format(len(account_photo_table), userid)
    else:
        description='Userid <{}> does not have any photos!'.format(userid)
    
    return redirect(url_for('table_user_details_handler', description=description))


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
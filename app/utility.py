import os

def convert_bytes_to_human_readable(num):
    """
    this function will convert bytes to MB.... GB... etc
    From: https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    """
    step_unit = 1024.0

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return '%3.1f %s' % (num, x)
        num /= step_unit


def get_file_extension(file_name):
    '''
    Return extension of a file, such as '.txt'
    '''
    _, file_extension = os.path.splitext(file_name)
    return file_extension

def split_file(src_file):
    CHUNK_SIZE = 50 * 1024 * 1024
    file_id = 0
    with open(src_file, 'rb') as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            with open(src_file + '.' + str(file_id), 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_id += 1
            chunk = f.read(CHUNK_SIZE)
    print(src_file + ' was split into ' + str(file_id) + ' files.')


def combine_files(src_files, dst_file):
    # Create an empty dst_file
    open(dst_file, 'wb').close()
    with open(dst_file, 'ab') as fout:
        for src_file in src_files:
            with open(src_file, 'rb') as fin:
                fout.write(fin.read())
    print(str(len(src_files)) + ' files were combined into ' + dst_file + '.')

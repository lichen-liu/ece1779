import io
import boto3
import botocore

'''Note:
- directory must end with '/', except for the root directory ''
- directory can have '' as name, as long as it ends with '/'
- file must have a name. It must not end with '/'
- file name can be the same as directory. But directory must end with '/', whereas file must not
'''

BUCKET = 'ece1779'
ROOT_DIR = 'data' + '/'
PHOTOS_DIR = ROOT_DIR + 'photos' + '/'
THUMBNAILS_DIR = ROOT_DIR + 'thumbnails' + '/'
RECTANGLES_DIR = ROOT_DIR + 'rectangles' + '/'


def is_path_s3_directory(key):
    if len(key) > 0:
        return key[-1] == '/'
    return True


def get_s3_path_in_string(key, bucket_name):
    return 's3://' + bucket_name +'/' + key


def is_bucket_existed(bucket_name=BUCKET):
    response = boto3.client('s3').list_buckets()

    if 'Buckets' in response:
        return bucket_name in [bucket['Name'] for bucket in response['Buckets']]
    return False


def create_bucket_if_necessary(bucket_name=BUCKET):
    if not is_bucket_existed(bucket_name):
        print('Creating bucket', bucket_name, '!')
        boto3.client('s3').create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})


def list_bucket_content(bucket_name=BUCKET, directory='', recursive=True):
    '''List the content in an S3 bucket directory (optional)

    :param bucket_name: Bucket to check
    :param directory: Directory to check. Optional. Does not support partial name
    :param recursive: True to list the content recursively, else only list the content inside dir
    :return: [(object, size)]
    '''
    assert(is_path_s3_directory(directory))

    paginator = boto3.client('s3').get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=directory)

    result = list()
    for item in pages.search('Contents'):
        if item is not None:
            key = item['Key']
            subkey = key[len(directory):]

            if len(subkey) == 0:
                continue

            if not recursive:
                slash_count = subkey.count('/')
                if slash_count > 1 or (slash_count == 1 and subkey[-1] != '/'):
                    continue

            result.append((key, item['Size']))

    return result


def get_bucket_content_size(key, debug=False, bucket_name=BUCKET):
    '''Get the size of an S3 bucket object

    :param bucket_name: Bucket to check
    :param key: Object to check. Does not support partial name
    :return: (size, num_directory, num_file, [object] if debug)
    '''
    paginator = boto3.client('s3').get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=key)

    size = 0
    l = list()
    dir_count = 0
    file_count = 0
    for item in pages.search('Contents'):
        if item is not None:
            k = item['Key']
            subkey = k[len(key):]

            if len(subkey) == 0 or len(key) == 0 or (len(key) > 0 and key[-1] == '/'):
                size += item['Size']

                if k[-1] == '/':
                    dir_count += 1
                else:
                    file_count += 1

                l.append(k)
    if debug:
        return (size, dir_count, file_count, l)
    else:
        return (size, dir_count, file_count)


def is_object_existed(key, bucket_name=BUCKET):
    '''Check whether an object exists in an S3 bucket object

    :param bucket_name: Bucket to check
    :param key: Object to check. Does not support partial name
    :return: True if found, else False
    '''
    paginator = boto3.client('s3').get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=key)

    for item in pages.search('Contents'):
        if item is not None:
            if item['Key'] == key:
                return True

    return False


def create_directory_if_necessary(directory, bucket_name=BUCKET):
    assert(is_path_s3_directory(directory))

    if not is_object_existed(key=directory, bucket_name=bucket_name):
        print('Creating directory', get_s3_path_in_string(key=directory, bucket_name=bucket_name) , '!')
        boto3.client('s3').put_object(Bucket=bucket_name, Key=directory)


def create_directories_if_necessary(bucket_name=BUCKET):
    create_directory_if_necessary(directory=ROOT_DIR, bucket_name=bucket_name)
    create_directory_if_necessary(directory=PHOTOS_DIR, bucket_name=bucket_name)
    create_directory_if_necessary(directory=THUMBNAILS_DIR, bucket_name=bucket_name)
    create_directory_if_necessary(directory=RECTANGLES_DIR, bucket_name=bucket_name)


def upload_file_bytes_object(key, file_bytes, bucket_name=BUCKET):
    '''Upload file bytes to an S3 bucket

    :param bucket_name: Bucket to upload to
    :param key: S3 object name
    :param file_bytes: file bytes object to upload
    :return: True if file was uploaded, else False
    '''
    return upload_file_object(key=key, file=io.BytesIO(file_bytes), bucket_name=bucket_name)


def upload_file_object(key, file, bucket_name=BUCKET):
    '''Upload a file to an S3 bucket

    :param bucket_name: Bucket to upload to
    :param key: S3 object name
    :param file: File-like object to upload, must be opened in binary mode
    :return: True if file was uploaded, else False
    '''

    try:
        boto3.client('s3').upload_fileobj(file, bucket_name, key)
    except botocore.exceptions.ClientError as e:
        print(str(e))
        return False
    return True


def get_object_url(key, bucket_name=BUCKET):
    '''Get a URL for object in S3 bucket

    :param bucket_name: Bucket to retrieve from
    :param key: S3 object name to retrieve
    :return: url for the object if object was found, else None
    '''

    if not is_object_existed(key=key, bucket_name=bucket_name):
        return None
    return boto3.client('s3').generate_presigned_url('get_object', ExpiresIn=3600, Params={'Bucket': bucket_name, 'Key': key})


def delete_directory_content(directory, bucket_name=BUCKET):
    assert(is_path_s3_directory(directory))

    s3 = boto3.client('s3')

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=directory)

    delete_us = dict(Objects=[])
    for item in pages.search('Contents'):
        if item is None:
           continue
        
        delete_us['Objects'].append(dict(Key=item['Key']))

        # flush once aws limit reached
        if len(delete_us['Objects']) >= 1000:
            s3.delete_objects(Bucket=bucket_name, Delete=delete_us)
            delete_us = dict(Objects=[])

    # flush rest
    if len(delete_us['Objects']):
        s3.delete_objects(Bucket=bucket_name, Delete=delete_us)


def delete_object(key, bucket_name=BUCKET):
    boto3.client('s3').delete_object(Bucket=bucket_name, Key=key)


# init()
# key = 'data/photos/DSCF0034.JP'
# print('key',key)
# try:
#     print('list_bucket_content', list_bucket_content(directory=key, recursive=True))
# except Exception as e:
#     print('list_bucket_content')

# try:
#     print('list_bucket_content', list_bucket_content(directory=key, recursive=False))
# except Exception as e:
#     print('list_bucket_content')

# try:
#     print('get_bucket_content_size', get_bucket_content_size(key=key))
# except Exception as e:
#     print('get_bucket_content_size')

# try:
#     print('is_object_existed', is_object_existed(key=key))
# except Exception as e:
#     print('is_object_existed')



# init()
# delete_directory_content(directory='')
# print(list_bucket_content(directory='', recursive=True))
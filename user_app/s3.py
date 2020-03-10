import boto3
import botocore

l_s3 = None

BUCKET = 'ece1779'
ROOT_DIR = 'data' + '/'
PHOTOS_DIR = ROOT_DIR + 'photos' + '/'
THUMBNAILS_DIR = ROOT_DIR + 'thumbnails' + '/'
RECTANGLES_DIR = ROOT_DIR + 'rectangles' + '/'


def init():
    global l_s3
    l_s3 = boto3.client('s3')

    # Remove the following
    create_bucket_if_necessary(BUCKET)
    create_directories_if_necessary(BUCKET)


def is_bucket_existed(bucket_name):
    response = l_s3.list_buckets()

    if 'Buckets' in response:
        return bucket_name in [bucket['Name'] for bucket in response['Buckets']]
    return False


def create_bucket_if_necessary(bucket_name):
    if not is_bucket_existed(bucket_name):
        print('Creating bucket', bucket_name, '!')
        l_s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})


def list_bucket_content(bucket_name):
    paginator = l_s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)

    result = list()
    for item in pages.search('Contents'):
        if item is not None:
           result.append(item['Key'])

    return result


def is_object_existed(bucket_name, key):
    response = l_s3.list_objects(Bucket=bucket_name, Prefix=key)
    return 'Contents' in response


def create_directory_if_necessary(bucket_name, dir_name):
    if not is_object_existed(bucket_name, dir_name):
        print('Creating directory', dir_name, 'in bucket', bucket_name, '!')
        l_s3.put_object(Bucket=bucket_name, Key=dir_name)


def create_directories_if_necessary(bucket_name):
    create_directory_if_necessary(bucket_name, ROOT_DIR)
    create_directory_if_necessary(bucket_name, PHOTOS_DIR)
    create_directory_if_necessary(bucket_name, THUMBNAILS_DIR)
    create_directory_if_necessary(bucket_name, RECTANGLES_DIR)


def upload_object(bucket_name, key, file):
    '''Upload a file to an S3 bucket

    :param bucket_name: Bucket to upload to
    :param key: S3 object name
    :param file: File to upload, must be opened in binary mode
    :return: True if file was uploaded, else False
    '''

    try:
        l_s3.upload_fileobj(file, bucket_name, key)
    except botocore.exceptions.ClientError as e:
        print(str(e))
        return False
    return True


def get_object_url(bucket_name, key):
    '''Get a URL for object in S3 bucket

    :param bucket_name: Bucket to retrieve from
    :param key: S3 object name to retrieve
    :return: url for the object if object was found, else None
    '''

    if not is_object_existed(bucket_name, key):
        return None
    return l_s3.generate_presigned_url('get_object', ExpiresIn=3600, Params={'Bucket': bucket_name, 'Key': key})


def delete_directory_content(bucket_name, directory):
    paginator = l_s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=directory)

    delete_us = dict(Objects=[])
    for item in pages.search('Contents'):
        if item is None:
           continue
        
        delete_us['Objects'].append(dict(Key=item['Key']))

        # flush once aws limit reached
        if len(delete_us['Objects']) >= 1000:
            l_s3.delete_objects(Bucket=bucket_name, Delete=delete_us)
            delete_us = dict(Objects=[])

    # flush rest
    if len(delete_us['Objects']):
        l_s3.delete_objects(Bucket=bucket_name, Delete=delete_us)


def delete_object(bucket_name, key):
    l_s3.delete_object(Bucket=bucket_name, Key=key)


'''
TODO: print number of non-dir objects
TODO: print size of dir
TODO: list_bucket_content filter out file only option
'''
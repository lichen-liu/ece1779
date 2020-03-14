import os

from user_app import webapp, directory, main
from common_lib import utility, s3, database


def init():
    '''
    All initialization should be done here
    '''
    
    print('INITIALIZE')

    # Initialize directories
    directory.create_directories_if_necessary()

    # Initialize S3
    s3.create_bucket_if_necessary()
    s3.create_directories_if_necessary()

    # Initialize RDS MySQL
    database.create_schema_if_necessary()

    # Initialize ec2_instance_id in main
    main.init()

    # Construct yolov3.weights if necessary
    yolov3_weights_dst_file = os.path.join(
        directory.get_yolo_dir_path(), 'yolov3.weights')
    if not os.path.exists(yolov3_weights_dst_file):
        yolov3_weights_chunk_files = [os.path.join(
            directory.get_yolo_dir_path(), 'yolov3.weights.' + str(i)) for i in range(0, 5)]
        utility.combine_files(yolov3_weights_chunk_files,
                              yolov3_weights_dst_file)
    # To split, run:
    # utility.split_file(yolov3_weights_dst_file)

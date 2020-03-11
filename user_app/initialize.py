import os

from user_app import webapp, directory, utility, s3


def init():
    '''
    All initialization should be done here
    '''
    
    print('INITIALIZE')

    # Initialize directories
    directory.create_directories_if_necessary()

    # Initialize s3
    s3.init()
    s3.create_directories_if_necessary()

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

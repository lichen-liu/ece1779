import os

from app import webapp, directory, utility, ibr_queue, image_batch_runner, image_pool_runner


def init():
    '''
    All initialization should be done here
    '''
    
    print('INITIALIZE')

    # Initialze directories
    directory.create_directories_if_necessary()

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

    image_processing_choice = webapp.config.get('IMAGE_PROCESSING_CHOICE')
    if image_processing_choice == 0:
        # Per-request version
        pass
    elif image_processing_choice == 1:
        # image_batch_runner version
        ibr_queue.init_queue()
        image_batch_runner.init_batch_runner()
        batch_runner = image_batch_runner.get_batch_runner()
        batch_runner.run()
    elif image_processing_choice == 2:
        # image_pool_runner version
        image_pool_runner.init(1, 4096, 5)
    else:
        assert(False)

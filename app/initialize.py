import os

from app import webapp, directory, utility, queue, image_batch_runner


def init():
    '''
    All initialization should be done here
    '''
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

    if webapp.config.get('USE_IMAGE_BATCH_RUNNER'):
        # Run the batch runner
        queue.init_queue()
        image_batch_runner.init_batch_runner()
        batch_runner = image_batch_runner.get_batch_runner()
        batch_runner.run()

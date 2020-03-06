from app import image_processing as bt_helper, yolo_net
import multiprocessing
from multiprocessing import Queue
import os


l_pool = None
l_queue = None


def init(num_workers, queue_size, batch_size):
    global l_queue
    global l_pool
    l_queue = multiprocessing.Queue(queue_size)
    l_pool = [multiprocessing.Process(target=pool_worker_main, args=(l_queue, batch_size), daemon=True) for _ in range(num_workers)]
    for worker in l_pool:
        worker.start()


def pool_worker_main(queue, batch_size):
    print(os.getpid(),'working')
    while True:
        tasks = queue_pop(queue, batch_size)
        print(os.getpid(), 'got', len(tasks), 'tasks')

        images = list()
        for task in tasks:
            source_path, _, _ = task
            images.append(bt_helper.load_cv_img(source_path))

        net = yolo_net.new_yolo_net()

        boxes_for_all_images, descriptions_for_all_images = bt_helper.detect_objects_on_images(images, net)
        for boxes, descriptions, image, task in zip(boxes_for_all_images, descriptions_for_all_images, images, tasks):
            _, thumbnail_dest_path, rectangled_dest_path = task
            rectangled_image = bt_helper.draw_rectangles(image, boxes, descriptions)
            thumbnail = bt_helper.generate_thumbnail_for_cv_img(rectangled_image)

            bt_helper.save_cv_img(rectangled_image, rectangled_dest_path)
            bt_helper.save_cv_img(thumbnail, thumbnail_dest_path)

            del rectangled_image
            del thumbnail

        del images
        del net


def send_image_task_to_pool(source_path, thumbnail_dest_path, rectangled_dest_path):
    try:
        l_queue.put_nowait((source_path, thumbnail_dest_path, rectangled_dest_path))
    except Queue.Full as _:
        return False
    except Exception as e:
        print('Unexpected exception: ' + str(e))
        return False
    else:
        return True


def queue_pop(queue, max_num):
    '''
    Block on the first item, and pop up to max_num of items
    '''
    result = list()
    result.append(queue.get(True))
    try:
        while len(result) < max_num:
            result.append(queue.get_nowait())
    except Queue.Empty as _:
        pass
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return result
from user_app import image_processing, ibr_queue, yolo_net
from user_app import image_processing as bt_helper
import time
import threading


class BatchRunner():
    def __init__(self, queue, batch_size):
        self._queue = queue
        self._batch_size = batch_size
        self._started = False
        self._net = yolo_net.new_yolo_net()

    def try_get_batch(self, batch_size):
        with self._queue.acquire_lock(use_timeout=False) as acquired:
            if(acquired):
                if not self._queue.has_task():
                    # Sleep on condition
                    self._queue.wait_task()
                return self._queue.pop(batch_size)

    def run_batch(self):
        while(True):
            tasks = self.try_get_batch(self._batch_size)
            images = []
            for task in tasks:
                images.append(bt_helper.load_cv_img(task.source_path))

            boxes_for_all_images, descriptions_for_all_images = bt_helper.detect_objects_on_images(
                images, self._net)
            for boxes, descriptions, image, task in zip(boxes_for_all_images, descriptions_for_all_images, images, tasks):

                rectangled_image = bt_helper.draw_rectangles(
                    image, boxes, descriptions)
                thumbnail = bt_helper.generate_thumbnail_for_cv_img(
                    rectangled_image)

                bt_helper.save_cv_img(
                    rectangled_image, task.rectangled_dest_path)
                bt_helper.save_cv_img(thumbnail, task.thumbnail_dest_path)

    def run(self):
        if not self._started:
            batch_thread = threading.Thread(target=self.run_batch, daemon=True)
            batch_thread.start()
            self._started = True


l_batch_runner = None


def init_batch_runner():
    global l_batch_runner
    l_batch_runner = BatchRunner(ibr_queue.get_queue(), 5)


def get_batch_runner():
    return l_batch_runner

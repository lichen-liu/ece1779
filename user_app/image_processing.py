import os

import numpy
import cv2

# # Get rid of warning messages
# import sys
# stderr = sys.stderr
# stdout = sys.stdout
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.stderr = open(os.devnull, 'w')
# sys.stdout = open(os.devnull, 'w')
# sys.stdwarn = open(os.devnull, 'w')
# import cvlib as cv
# sys.stderr = stderr
# sys.stdout = stdout

from user_app import directory, yolo_net
from common_lib import utility, s3


def draw_rectangles_on_cv_image(cv_img, boxes, descriptions):
    assert(len(boxes) == len(descriptions))
    for box, description in zip(boxes, descriptions):
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])
        cv2.rectangle(cv_img, (x, y), (x + w, y + h), [0, 0, 0], 4)
        cv2.putText(cv_img, description, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)
    return cv_img


def detect_objects_on_cv_images(cv_imgs, net):
    layer_outputs_for_images = net.pass_forward(cv_imgs)
    boxes_for_all_images, descriptions_for_all_images = extract_boxes_and_descriptions_for_cv_images(layer_outputs_for_images,
                                                                                                  cv_imgs)

    return boxes_for_all_images, descriptions_for_all_images


def extract_boxes_and_descriptions_for_cv_images(layer_outputs, cv_imgs):
    boxes_for_all_images = []
    descriptions_for_all_images = []

    #OpenCV is stupid
    # Single image and multiple images gives different structure
    for index in range(len(cv_imgs)):
        boxes, descriptions = extract_boxes_and_descriptions_for_cv_image_from_all_outputs_layers(
            layer_outputs, index, cv_imgs[index], len(cv_imgs) == 1)

        boxes_for_all_images.append(boxes)
        descriptions_for_all_images.append(descriptions)

    return boxes_for_all_images, descriptions_for_all_images


def extract_boxes_and_descriptions_for_cv_image_from_all_outputs_layers(layer_outputs, img_index, cv_img, single_image, target_confidence=0.5, target_threshold=0.3):
    original_height = cv_img.shape[0]
    original_width = cv_img.shape[1]

    boxes = []
    confidences = []
    class_ids = []

    shape_adjustments = numpy.array(
        [original_width, original_height, original_width, original_height])

    for layer_output in layer_outputs:

        if not single_image:
            layer_output = layer_output[img_index]
        l_boxes, l_confidences, l_class_ids = get_detections_from_a_layer(
            layer_output, shape_adjustments)

        boxes += l_boxes
        confidences += l_confidences
        class_ids += l_class_ids

    idxs = cv2.dnn.NMSBoxes(
        boxes, confidences, target_confidence, target_threshold)
    if len(idxs) > 0:
        idxs = idxs.flatten()

    labels = load_labels()
    boxes = [boxes[i] for i in idxs]
    descriptions = ['{}: {:.4f}'.format(
        labels[class_ids[i]], confidences[i]) for i in idxs]
    return boxes, descriptions


def get_detections_from_a_layer(layer_output_for_image, shape_adjustments, target_confidence=0.5):
    end_index_of_box_shape = 4
    start_index_of_scores = end_index_of_box_shape + 1

    boxes_for_image_at_layer = []
    confidences_for_image_at_layer = []
    class_ids_for_image_at_layer = []

    for detection in layer_output_for_image:

        scores = detection[start_index_of_scores:]
        class_id = numpy.argmax(scores)
        confidence = scores[class_id]

        if confidence > target_confidence:
            (center_x, center_y, width, height) = (
                detection[0:end_index_of_box_shape] * shape_adjustments).astype('int')
            x = int(center_x - (width / 2))
            y = int(center_y - (height / 2))

            boxes_for_image_at_layer.append([x, y, int(width), int(height)])
            confidences_for_image_at_layer.append(float(confidence))
            class_ids_for_image_at_layer.append(class_id)

    return boxes_for_image_at_layer, confidences_for_image_at_layer, class_ids_for_image_at_layer


def load_labels():
    labels_path = os.path.join(directory.get_yolo_dir_path(), 'coco.names')
    return open(labels_path).read().strip().split('\n')


def generate_thumbnail_for_cv_image(image, matching_size=120, inter=cv2.INTER_AREA):
    dim = None
    large_side = None

    (h, w) = image.shape[:2]
    if h > w:
        large_side = h
    else:
        large_side = w

    ratio = matching_size / float(large_side)
    dim = (int(w * ratio), int(h * ratio))

    resized = cv2.resize(image, dim, interpolation=inter)

    vertical_border = (matching_size - dim[1]) // 2
    horizonta_border = (matching_size - dim[0]) // 2
    return cv2.copyMakeBorder(resized, vertical_border, vertical_border, horizonta_border, horizonta_border, cv2.BORDER_CONSTANT, value=[255, 255, 255])


def detect_and_draw_rectangles_on_cv_image(cv_bytes):
    cv_img_list = []
    cv_img_list.append(cv_bytes)
    net = yolo_net.new_yolo_net()
    boxes, descriptions = detect_objects_on_cv_images(cv_img_list, net)
    return draw_rectangles_on_cv_image(cv_bytes, boxes[0], descriptions[0])


def convert_cv_bytes_to_file_bytes(format, cv_bytes):
    return cv2.imencode(format, cv_bytes)[1]


def convert_file_bytes_to_cv_bytes(file_bytes):
    return cv2.imdecode(numpy.fromstring(file_bytes, numpy.uint8), cv2.IMREAD_COLOR)
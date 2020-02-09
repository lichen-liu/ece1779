import numpy as np
import cv2
import os
from app import directory, account, yolo_net

nets = {}

def draw_rectangles(cv_img, boxes, descriptions):
    assert(len(boxes) == len(descriptions))
    for box, description in zip(boxes, descriptions):
        (x,y) = (box[0],box[1])
        (w,h) = (box[2],box[3])
        cv2.rectangle(cv_img, (x, y), (x + w, y + h), [0,0,0], 2)
        cv2.putText(cv_img, description, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,0], 2)
    return cv_img

def detect_objects(cv_img, target_confidence = 0.5, target_threshold = 0.3):

    net = yolo_net.load_yolo_net(account.account_get_logged_in_user())
    layer_outputs = net.pass_forward(cv_img)
    
    boxes = []
    confidences = []
    class_ids = []

    shape_adjustments = np.array([cv_img.shape[1], cv_img.shape[0], cv_img.shape[1], cv_img.shape[0]])
    end_index_of_box_shape = 4
    start_index_of_scores = end_index_of_box_shape + 1 

    for output in layer_outputs:
        for detection in output:
           
            scores = detection[start_index_of_scores:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > target_confidence:
                (center_x, center_y, width, height) = (detection[0:end_index_of_box_shape] * shape_adjustments).astype("int")
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
 
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, target_confidence, target_threshold)
    if len(idxs) > 0:
        idxs = idxs.flatten()

    labels = load_labels()
    boxes = [boxes[i] for i in idxs]
    descriptions = ["{}: {:.4f}".format(labels[class_ids[i]], confidences[i]) for i in idxs]
    return boxes, descriptions

def load_labels():
    labels_path = os.path.join(directory.get_yolo_directory(),"coco.names")
    return open(labels_path).read().strip().split("\n")
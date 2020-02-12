import os
import cv2
from app import directory

# Unfortunately net created by cv2.dnn is not thread safe, thus EACH user...
# https://answers.opencv.org/question/205222/is-dnn-supports-threading/
# ... will need a seperate yolo net object instantiated and persist in the memory...
# ... the drawback is that it occupies a lot of memory ...
# ... another solution is to load a yolo net every time a request come
# ... another solution is to lock a global yolo net

class YoloNet:
    def __init__(self, net):
        self._net = net
        layer_names = self._net.getLayerNames()
        self._output_layers = [layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]
    def pass_forward(self, images):
        blob = cv2.dnn.blobFromImages(images, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self._net.setInput(blob)
        return self._net.forward(self._output_layers)

weights_path = os.path.join(directory.get_yolo_dir_path(), "yolov3.weights")
config_path = os.path.join(directory.get_yolo_dir_path(), "yolov3.cfg")
net = YoloNet(cv2.dnn.readNetFromDarknet(config_path, weights_path))

def load_yolo_net():
    return net
    
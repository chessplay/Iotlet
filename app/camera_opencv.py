import cv2
from base_camera import BaseCamera
import numpy as np



CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('./MobileNetSSD_deploy.prototxt.txt', "./MobileNetSSD_deploy.caffemodel")
class Camera(BaseCamera):

    video_source = "rtmp://localhost:1935/live/film"
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        count = 0
        while True:
            # read current frame
            _, img = camera.read()
            img=cv2.resize(img,(300,300))
            if count % 30 == 0:
                (h, w) = img.shape[:2]
                blob=cv2.dnn.blobFromImage(img,0.007843,(300,300),127.5)
                net.setInput(blob)
                detections=net.forward()
                for i in np.arange(0, detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > 0.2:
                        idx = int(detections[0, 0, i, 1])
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                        print("[INFO] {}".format(label))
                        cv2.rectangle(img, (startX, startY), (endX, endY),COLORS[idx], 2)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(img, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                #img=cv2.resize(img,(320,240),interpolation=cv2.INTER_AREA)
            if count%2==0:
                yield cv2.imencode('.png', img)[1].tobytes()
            count = count + 1


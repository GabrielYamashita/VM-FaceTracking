
# import cv2
# from cvzone.PIDModule import PID
# from cvzone.FaceDetectionModule import FaceDetector
# from Detectors import Detectors

# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


# detectorFace = FaceDetector()
# detector = Detectors()
# # For a 640x480 image center target is 320 and 240

# while True:
#     success, img = cap.read()
#     img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

#     h, w, _ = img.shape

#     xPID = PID([1, 0.000000000001, 1], w // 2)
#     yPID = PID([1, 0.000000000001, 1], 65)
#     zPID = PID([1, 0.000000000001, 1], h // 2, axis=1, limit=[-100, 100])

#     img, bboxs = detectorFace.findFaces(img)
#     img, d = detector.FaceDistance(img, False, True)

#     if bboxs:
#         x, y, w, h = bboxs[0]["bbox"]
#         cx, cy = bboxs[0]["center"]

#         xVal = int(xPID.update(cx))
#         zVal = int(zPID.update(cy))

#         xPID.draw(img, [cx, cy])
#         zPID.draw(img, [cx, cy])

#     if d:
#         yVal = int(yPID.update(d))

#         # zPID.draw(img, )

#         cv2.putText(img, f'x:{xVal} , y:{yVal} z:{zVal}', (x, y - 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

import time

def wait(n):
    time.sleep(n)

start = time.time()
wait(5)
end = time.time()

print(end-start)


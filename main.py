
# Imports
import cv2
from Camera import Camera
from PID import FacePID
from Detectors import Detectors


# Incialização de Objetos
camLoc = 1
camAPI = cv2.CAP_DSHOW
config = [True, False, True] # showFps, showDraw, showAreaBox

cam = Camera(camLoc, camAPI, config=config) 
detector = Detectors()
PID = FacePID(detector, [0.5, 0.04, 0.3])


# Loop Principal
cam.run(PID)
cam.release()
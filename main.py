
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
PID = FacePID(detector)


# Loop Principal
cam.run(PID)
cam.release()
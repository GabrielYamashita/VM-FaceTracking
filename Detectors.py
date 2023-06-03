
import cv2

from cvzone import FPS
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone import putTextRect



fpsReader = FPS()

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

class Detectors:
   def __init__(self):
      self.handDetector = HandDetector(detectionCon=0.8, maxHands=1)
      self.faceDetector = FaceDetector()
      self.faceMeshDetector = FaceMeshDetector(maxFaces=1)
      self.initColors()


   def initColors(self):
      self.BLUE = (255,0,0)
      self.GREEN = (0,255,0)
      self.RED = (0,0,255)

      self.MAGENTA = (255, 0, 255)
      self.CYAN = (255, 255, 0)
      self.YELLOW = (0, 255, 255)

      self.LIGHT_GRAY = (192, 192, 192)
      self.GRAY = (128, 128, 128)
      self.DARK_GRAY = (64, 64, 64)

      self.WHITE = (255, 255, 255)
      self.BLACK = (0, 0, 0)


   def HandDetector(self, img, draw=True, areaBox=False):
      if draw == True:
         hands, img = self.handDetector.findHands(img)

      elif draw == False:
         hands = self.handDetector.findHands(img, draw=False)

      centerHand = [0,0]
      areaHand = 0
      bboxHand = [0,0,0,0]
      typeHand = 0

      if hands:
         if hands[0]:
            hand = hands[0]

            xHand, yHand, wHand, hHand = hand['bbox']
            areaHand = wHand*hHand

            centerHand = list(hand['center']) # Centros X e Y
            bboxHand = list(hand['bbox']) # Origem em X, Origem em Y, Largura, Altura | Bounding Box 
            typeHand = hand['type'] # Lado da Mão | Esquerda ou Direita

            if areaBox == True:
               cv2.rectangle(img, (xHand,yHand), (xHand+wHand, yHand+hHand), self.RED, 2) # imagem, começo do retângulo, final do retângulo, cor, espessura
               cv2.circle(img, (centerHand[0], centerHand[1]), 5, self.GREEN, -1) # imagem, coord do centro, raio, cor, grossura

      return img, [ centerHand, areaHand, bboxHand, typeHand ] # 0: Centros = cx, cy, 1: Área = area, 2: Bounding Box = x,y,w,h, 3: Lado da Mão = typeHand


   def handCommand(self):
      pass


   def FaceDetector(self, img, draw=True, areaBox=False):
      img, bboxs = self.faceDetector.findFaces(img, draw=draw)

      centerFaces = []
      areaFaces = []
      bboxFaces = []

      if bboxs:
         for bbox in bboxs:
            cxFace, cyFace = bbox['center']
            xFace, yFace, wFace, hFace = bbox['bbox']
            areaFace = wFace*hFace

            centerFaces.append([cxFace, cyFace]) # Centros X e Y
            areaFaces.append(areaFace) # Área da Face
            bboxFaces.append(bbox['bbox']) # Origem em X, Origem em Y, Largura, Altura | Bounding Box 

      if len(areaFaces) != 0:
         i = areaFaces.index(max(areaFaces)) # Índice da Cara com Maior Área

         if areaBox == True:
            cv2.rectangle(img, (xFace,yFace), (xFace+wFace, yFace+hFace), self.RED, 2) # imagem, começo do retângulo, final do retângulo, cor, espessura
            cv2.circle(img, (centerFaces[i][0], centerFaces[i][1]), 5, self.GREEN, -1) # imagem, coord do centro, raio, cor, grossura

         return img, [centerFaces[i], areaFaces[i], bboxFaces[i]] # 0: Centros = cx,cy, 1: Área = area, 2: Bounding Box = x,y,w,h

      else:
         return img, [ [0,0], 0, [0,0,0,0] ] # 0: Centros = 0,0, 1: Área = 0, 2: Bounding Box = 0,0,0,0


   def FaceDistance(self, img, draw=True, areaBox=False):
      img, faces = self.faceMeshDetector.findFaceMesh(img, draw=draw)
      d = None

      if faces:
         face = faces[0]
         pointLeft = face[145]
         pointRight = face[374]

         # Face Mesh Detector
         w, _ = self. faceMeshDetector.findDistance(pointLeft, pointRight)

         # Finding Focal Distance (f)
         # W = 6.3
         # d = 50
         # f = (w*d)/W
         # print(f) # cam 0: 627, cam 1: 674

         # Finding Distance (d)
         W = 6.3 # distância média entre os dois olhos
         f = 674 # distância focal
         d = (W*f)/w

         if areaBox == True:
            cv2.line(img, pointLeft, pointRight, (0,200,0), 3)
            cv2.circle(img, pointLeft, 5, (255,0,255), cv2.FILLED)
            cv2.circle(img, pointRight, 5, (255,0,255), cv2.FILLED)

            putTextRect(img, f"Depth: {int(d)}cm", (face[10][0]-100, face[10][1]-50), scale=2)

      return img, d



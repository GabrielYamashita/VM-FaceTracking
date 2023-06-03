
import cv2
from cvzone.PIDModule import PID
from Detectors import Detectors
from MoveRobot import Robot

class FacePID:
    def __init__(self, kPID=[1, 0.000000000001, 1]):
        self.kPID = kPID
        self.detector = Detectors()
        self.ur5 = Robot('169.254.66.125', 30000)


    def calculaErro(self, img, xTarget, yTarget, zTarget, draw, areaBox):
        # PID de X Y Z
        xPID = PID(self.kPID, xTarget) # w//2
        yPID = PID(self.kPID, yTarget) # depth = 65
        zPID = PID(self.kPID, zTarget, axis=1) # h//2

        # Offsets X Y Z
        xValue, yValue, zValue = 0, 0, 0
        offsets = [xValue, yValue, zValue]

        # Detector da Face
        img, infoFace = self.detector.FaceDetector(img, draw=draw, areaBox=areaBox) # recebimento de imagem e dados da Face
        centerFace, area, bboxFace = infoFace # desempacotamento das informações
        xFace, yFace, wFace, hFace = bboxFace # desempacotamento das informações da Bounding Box

        # Detector da Distância da Face
        img, d = self.detector.FaceDistance(img, draw=draw, areaBox=areaBox)

        # Update do Valor de X e Z
        if infoFace != [ [0,0], 0, [0,0,0,0] ]:
            offsets[1] = -int(yPID.update(centerFace[0]))
            offsets[2] = -int(zPID.update(centerFace[1]))

            # Desenha Eixos de X e Z
            if draw or areaBox:
                yPID.draw(img, centerFace)
                zPID.draw(img, centerFace)

        # Update do Valor em Y
        if d != None:
            offsets[0] = int(xPID.update(d)) # eixo y | distância do yTarget

        # Mostra os Valores de Offset em X, Y e Z
        if infoFace != [ [0,0], 0, [0,0,0,0] ] and d != None and (draw or areaBox):
            cv2.putText(img, f'x:{offsets[0]} , y:{offsets[1]} z:{offsets[2]}', (xFace, yFace - 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        self.setOffsets(offsets[0], offsets[1], offsets[2])

        return img, offsets


    def setOffsets(self, x, y, z):
        if x <= 25 and x >= -25:
            # print("PAROU EM X")
            self.ur5.setpointDiffX(0)
        else:
            # print("MOVENDO EM -X")
            self.ur5.setpointDiffX(x)

        if y <= 100 and y >= -100:
            # print("PAROU EM Y")
            self.ur5.setpointDiffY(0)
        else:
            # print("MOVENDO EM -Y")
            self.ur5.setpointDiffY(y)

        if z <= 100 and z >= -100:
            # print("PAROU EM Z")
            self.ur5.setpointDiffZ(0)
        else:
            # print("MOVENDO EM -Z")
            self.ur5.setpointDiffZ(z)

        print(self.ur5.x, self.ur5.y, self.ur5.z)

        # self.MoveRobot.sendCommand()




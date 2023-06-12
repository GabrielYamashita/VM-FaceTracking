
import cv2
from cvzone.PIDModule import PID
from simple_pid import PID as PIDtest
# from Detectors import Detectors
from MoveRobot import Robot

class FacePID:
    def __init__(self, detector, kPID=[1, 0.000000000001, 1]):
        self.kPID = kPID
        self.detector = detector
        self.ur5 = Robot('169.254.66.125', 30000)

    
    def sendHandCommand(self, img, draw, areaBox):
        img, infoHand = self.detector.HandDetector(img, draw=draw, areaBox=areaBox) # recebimento de imagem e dados da Mão
        centerHand, areaHand, bboxHand, typeHand, fingers = infoHand # desempacotamento das informações
        xHand, yHand, wHand, hHand = bboxHand # desempacotamento das informações da Bounding Box
        # print(fingers)

        comando = self.detector.handCommand(fingers)
        self.ur5.setHandCommand(comando)

        return img, comando


    def calculaErro(self, img, xTarget, yTarget, zTarget, draw, areaBox):
        # PID de X Y Z
        xPID = PID(self.kPID, xTarget) # w//2
        yPID = PID(self.kPID, yTarget) # depth = 65
        zPID = PID(self.kPID, zTarget, axis=1) # h//2

        xPIDteste = PIDtest(self.kPID[0], self.kPID[1], self.kPID[2], setpoint=xTarget) # w//2
        yPIDteste = PIDtest(self.kPID[0], self.kPID[1], self.kPID[2], setpoint=yTarget) # depth = 65
        zPIDteste = PIDtest(self.kPID[0], self.kPID[1], self.kPID[2], setpoint=zTarget) # h//2

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
            # offsets[1] = int(-yPID.update(centerFace[0]))
            # offsets[2] = int(-zPID.update(centerFace[1]))
            offsets[1] = int(yPIDteste(centerFace[0]))
            offsets[2] = int(zPIDteste(centerFace[1]))

            # Desenha Eixos de X e Z
            if draw or areaBox:
                yPID.draw(img, centerFace)
                zPID.draw(img, centerFace)

        # Update do Valor em Y
        if d != None:
            # offsets[0] = int(xPID.update(d)) # eixo y | distância do yTarget
            offsets[0] = int(xPIDteste(d)) # eixo y | distância do yTarget

        # Mostra os Valores de Offset em X, Y e Z
        if infoFace != [ [0,0], 0, [0,0,0,0] ] and d != None and (draw or areaBox):
            cv2.putText(img, f'x:{offsets[0]} , y:{offsets[1]} z:{offsets[2]}', (xFace, yFace - 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        self.setOffsets(offsets[0], offsets[1], offsets[2])

        return img, offsets


    def setOffsets(self, x, y, z):
        if x <= 15 and x >= -15:
            # print("PAROU EM X")
            self.ur5.setpointDiffX(0)
        else:
            # print("MOVENDO EM X")
            self.ur5.setpointDiffX(x)

        if y <= 50 and y >= -50:
            # print("PAROU EM Y")
            self.ur5.setpointDiffY(0)
        else:
            # print("MOVENDO EM Y")
            self.ur5.setpointDiffY(y)

        if z <= 50 and z >= -50:
            # print("PAROU EM Z")
            self.ur5.setpointDiffZ(0)
        else:
            # print("MOVENDO EM Z")
            self.ur5.setpointDiffZ(z)

        # print(self.ur5.x, self.ur5.y, self.ur5.z)

        self.ur5.sendCommand()




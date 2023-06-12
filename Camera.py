
import cv2
from cvzone import FPS
from PID import PID

class Camera:
    def __init__(self, cam, api, config=[True, False, False]):
        self.cap = cv2.VideoCapture(cam, api)
        self.fpsReader = FPS()
        self.showFps, self.showDraw, self.showAreaBox = config
        self.initColors()
        self.stopCamera = False
        self.currFrame = 0


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


    def run(self, PID):
        print("- Câmera Ligada")

        while not self.stopCamera:
            # Inicia a Câmera
            success, img = self.cap.read()
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.wImg, self.hImg, _ = img.shape

            # Execução do Detector
            if self.skipFrame(1):
                self.operation(img, PID, self.showDraw, self.showAreaBox)

            # Desenha Eixos
            # if self.showDraw == True:
            #     cyImg, cxImg = (int(self.wImg/2), int(self.hImg/2)) # Centro da Imagem
            #     cv2.line(img, (0, cyImg), (self.hImg, cyImg), self.MAGENTA, 1) # Linha Eixo X
            #     cv2.line(img, (cxImg, 0), (cxImg, self.wImg), self.MAGENTA, 1) # Linha Eixo Y

            # Mostra o FPS
            if self.showFps:
                fps, img = self.fpsReader.update(img, pos=(20,40), color=self.GREEN, scale=2, thickness=2)

            # Mostra a Imagem
            cv2.imshow(f"Face Detection", img)

            # Checa Tecla Pressionada
            key = cv2.waitKey(1)
            if key == ord('q'): # Saída
                self.stopCamera = True

            elif key == ord('f'): # fps
                self.updateValue('fps')

            elif key == ord('d'): # draw
                self.updateValue('draw')

            elif key == ord('a'): # areaBox
                self.updateValue('areaBox')


    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

        print("- Câmera Desliga")


    def skipFrame(self, qntFrames):
        self.currFrame += 1
            
        if self.currFrame != qntFrames:
            return False

        else:
            self.currFrame = 0
            return True

    def updateValue(self, value):
        self.showFps = not self.showFps if value == "fps" else self.showFps # Inverte Estado do 
        self.showDraw = not self.showDraw if value == "draw" else self.showDraw # Inverte Estado do draw
        self.showAreaBox = not self.showAreaBox if value == "areaBox" else self.showAreaBox  # Inverte Estado do areaBox
        # print(f"{value} changed to:", getattr(self, value))


    def operation(self, img, PID, draw, areaBox):
        # Recebe Comando Pela Mão
        img, comando = PID.sendHandCommand(img, draw, areaBox)
        # print(comando)


        # Calcula Erro com PID da Face
        # Baseado na Base do Rôbo
        x = 85
        y = self.hImg // 2
        z = self.wImg // 2
        img, offsets = PID.calculaErro(img, x, y, z, draw, areaBox)
        # print(offsets)




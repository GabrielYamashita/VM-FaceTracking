
import time
import socket

class Robot:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

        self.x = 0
        self.y = 0
        self.z = 0
        self.command = 0


    def setpointDiffX(self, X):
        self.x = X


    def setpointDiffY(self, Y):
        self.y = Y


    def setpointDiffZ(self, Z):
        self.z = Z

    
    def setHandCommand(self, command):
        self.command = command


    def sendCommandTest(self):
        print("\nconnect()")
        print(f"Sent: ({self.x}, {self.y}, {self.z})")
        print("disconnect()\n")


    def sendCommand(self):
        self.connect()

        DATA = f'({self.x},{self.y},{self.z},{self.command})'
        # print(DATA)

        try:
            # msg = self.c.recv(1024)
            # print(f"Message: {msg}")

            # if (msg == b'asking_for_data'):
            self.c.send(bytes(DATA, 'ascii'))
            # print (f'Sent {DATA}')
    
        except socket.error as socketerror:
            pass

        self.disconnect()


    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(5)
        self.c, addr = self.s.accept()

        # print("Connected")


    def disconnect(self):
        self.c.close()
        self.s.close()

        # print("Disconnected\n")

import random

def main():
    robo = Robot('169.254.66.125', 30000)

    while True:
        # pos = [0,0,0]
        # i = 0
        # while i < 2:
        #     offset = random.randint(-200, 200)
        #     # print(offset)

        #     if offset not in range(-100, 100):
        #         pos[i] = offset
        #         i+=1

        # pos = input("Coords: ").split(" ")

        x, y, z = [int(x) for x in input("Coords: ").split()]

        robo.setpointDiffX(x)
        robo.setpointDiffY(y)
        robo.setpointDiffZ(z)

        robo.sendCommand()

if __name__ == '__main__':
    main()


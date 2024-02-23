import pyfirmata
from constants import UP, DOWN



class DeathRod:
    def __init__(self, board, pin_num):
        self.position = UP
        self.servo = board.get_pin('d:{}:s'.format(pin_num))


    def go_down(self):

        self.servo.write(90)
        self.position = DOWN


    def go_up(self):

        self.servo.write(0)
        self.position = UP
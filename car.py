import pyfirmata
import time
import constants
# Create a new board, specifying the serial port
class Servo:
    def __init__(self, board, pin, direction = 1):
        self.pin = board.get_pin('d:'+str(pin)+':s')
        self.direction = direction

    def move(self, speed: int):
        # speed = 0 is stop
        # speed = 100 is forward
        # speed = -100 is backward
        speed = int(speed * self.direction)
        speed = int(((speed/100)*90)+90)
        self.pin.write(speed)

    def stop(self):
        self.pin.write(90)

class Car:
    def __init__(self, servo_left_forward: Servo, servo_right_forward: Servo, servo_left_backward: Servo, servo_right_backward: Servo, servo_death_rod: Servo):
        self.servos = [servo_left_forward, servo_right_forward, servo_left_backward, servo_right_backward]
        self.death_rod = servo_death_rod
        self.direction = [0,0]
        self.stop()
        
    def move(self, speed: int, move_time: float = 0):
        # speed = 0 is stop
        # speed = 100 is forward
        # speed = -100 is backward
        self.direction = [constants.MOVE_CODE, speed]
        if speed != 0:
            self.servos[0].move(speed)
            self.servos[1].move(speed)
            self.servos[2].move(speed)
            self.servos[3].move(speed)
        else:
            self.servos[0].stop()
            self.servos[1].stop()
            self.servos[2].stop()
            self.servos[3].stop()
        
        if move_time != 0:
            time.sleep(move_time)
            self.stop()

    def rotate(self, speed: int, move_time: float = 0):
        # speed = 0 is stop
        # speed = 100 is right
        # speed = -100 is left
        self.direction = [constants.TURN_CODE, speed]
        if speed != 0:
            self.servos[0].move(-speed)
            self.servos[1].move(speed)
            self.servos[2].move(-speed)
            self.servos[3].move(speed)
        
        else:
            self.servos[0].stop()
            self.servos[1].stop()
            self.servos[2].stop()
            self.servos[3].stop()
        
        if move_time != 0:
            time.sleep(move_time)
            self.stop()
    
    def stop(self):
        self.direction = [constants.NOTHING_CODE, 0]
        self.servos[0].stop()
        self.servos[1].stop()
        self.servos[2].stop()
        self.servos[3].stop()
        
    def move_death_rod(self, position: int):
        if position == constants.UP:
            if self.death_rod.position == constants.DOWN:
                self.death_rod.go_up()
        else:
            if self.death_rod.position == constants.UP:
                self.death_rod.go_down()
        time.sleep(1)



if __name__ == '__main__':
    board = pyfirmata.Arduino('COM5')
    pins = [3,2,4,5]
    directions = [1,-1,-1,-1]
    servos = [Servo(board, pin, direction) for pin, direction in zip(pins, directions)]
    car = Car(*servos)
    car.move(100, 10)
    

import pyfirmata
import time
import car
import keyboard
import constants

def main():
    # Set up the board with bluetooth
    port = 'COM3'
    board = pyfirmata.Arduino(port)
    # Set up the pins
    pins = [3,2,4,5]
    directions = [-1,1,-1,1]
    servos = [car.Servo(board, pin, direction) for pin, direction in zip(pins, directions)]
    mycar = car.Car(*servos)
    print("connected")
    i = 0
    while True:
        if keyboard.is_pressed('w'):
            if mycar.direction != constants.MOVE_FORWARD:
                mycar.move(100)
        elif keyboard.is_pressed('s'):
            if mycar.direction != constants.MOVE_BACKWARD:
                mycar.move(-100)
        elif keyboard.is_pressed('a'):
            if mycar.direction != constants.TURN_LEFT:
                mycar.rotate(-100)
        elif keyboard.is_pressed('d'):
            if mycar.direction != constants.TURN_RIGHT:
                mycar.rotate(100)
        else:
            if mycar.direction != constants.STOP:
                mycar.stop()
        time.sleep(0.01)
        
        
if __name__=="__main__":
    main()
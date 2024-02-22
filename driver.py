import pyfirmata
import time
import car
import keyboard


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
            mycar.move(100)
            keyboard.wait('w')
            mycar.stop()
            print("w")
        elif keyboard.is_pressed('s'):
            mycar.move(-100)
            keyboard.wait('s')
            mycar.stop()
            print("s")
        elif keyboard.is_pressed('a'):
            mycar.rotate(-100)
            keyboard.wait('a')
            mycar.stop()
        elif keyboard.is_pressed('d'):
            mycar.rotate(100)
            keyboard.wait('d')
            mycar.stop()
        else:
            mycar.stop()
        time.sleep(0.01)
        
        
if __name__=="__main__":
    main()
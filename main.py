import pyfirmata
import time
# Create a new board, specifying the serial port
board = pyfirmata.Arduino('/dev/ttyACM0')

# contiuous servo pin 2
pin = board.get_pin('d:2:s')

# Set the servo to max speed forward
while True:
    pin.write(180)
    time.sleep(2)
    pin.write(0)
    time.sleep(2)
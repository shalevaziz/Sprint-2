import pyfirmata
import time
import car
import keyboard
import constants

class Autonumous():
    def __init__(self, car: car.Car):
        self.car = car
        self.car.stop()
        self.cur_pos = constants.START_POS
        self.cur_direction = constants.WEST
    
    def move_x_blocks(self, direction:int = 1, blocks:int = 1):
        # direction = 1 is forward
        # direction = -1 is backward
        moved = blocks * direction
        self.car.move(100*direction, constants.TIME_FOR_1_CUBE * blocks)
        if self.cur_direction == constants.NORTH:
            self.cur_pos[0] -= moved
        elif self.cur_direction == constants.SOUTH:
            self.cur_pos[0] += moved
        elif self.cur_direction == constants.EAST:
            self.cur_pos[1] += moved
        elif self.cur_direction == constants.WEST:
            self.cur_pos[1] -= moved
    
    def rotate_to_direction(self, direction:int):
        # direction = 1 is right
        # direction = -1 is left
        right_rotations = (direction - self.cur_direction) % 4
        left_rotations = (self.cur_direction - direction) % 4
        if right_rotations < left_rotations:
            self.car.rotate(100*direction, constants.TIME_FOR_90_DEG * right_rotations)
        else:
            self.car.rotate(-100*direction, constants.TIME_FOR_90_DEG * left_rotations)
        self.cur_direction = direction
    
    
    def move_to(self, pos: list):
        # pos is a list of 2 integers
        # pos[0] is the row number
        # pos[1] is the column number
        row = pos[0] - self.cur_pos[0]
        col = pos[1] - self.cur_pos[1]
        if row == 0:
            if col < 0:
                self.rotate_to_direction(constants.NORTH)
            if col > 0:
                self.rotate_to_direction(constants.SOUTH)
            self.move_x_blocks(1, abs(col))
        elif col == 0:
            if row < 0:
                self.rotate_to_direction(constants.WEST)
            if row > 0:
                self.rotate_to_direction(constants.EAST)
            self.move_x_blocks(1, abs(row))
    
    def convert_col(self, col:str):
        return ord(col) - ord('A') + 1
    
    def run_autonomous(self, commands: list[tuple[int,int]]):
        # commands is a list of tuples
        # each list is a position to move to
        updated_commands = [(self.convert_col(col), row) for col, row in commands]
        for command in updated_commands:
            self.move_to(command)
            time.sleep(0.1)
            

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
    
    # Autonomous
    auto = Autonumous(mycar)
    location_lst = [("B", 3), ("J", 3), ("J", 9), ("B", 9), ("B", 10)]
    auto.run_autonomous(location_lst)
    
    # Teleop
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
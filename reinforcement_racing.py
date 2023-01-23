
import os
import time
import numpy as np

class SimpleCar:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.velocity = 0
        self.policy = lambda x,y: (1, 0)

    def view(self, world):
        return 0
    
    def update(self, world):
        acceleration, angle = self.policy(self.velocity, self.view(world))
        self.turn(angle)
        self.velocity += acceleration
        if not collide(self.position, self.velocity*self.orientation, world):
            self.position += self.velocity*self.orientation
            self.policy = lambda x,y: (1,0)
        else: 
            self.velocity = 0
            self.policy = lambda x,y: (1, -np.pi/2)

    def turn(self, angle):
        self.orientation = np.dot(np.array([[np.cos(angle), -np.sin(angle)], 
                         [np.sin(angle),  np.cos(angle)]]), self.orientation)


class LearningCar:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.velocity = 0
        architecture = [4,25,25,2]
        self.policy = lambda x,y: (1, 0)

    def view(self, world):
        returnValue = np.array([0,0,0])
        viewDirections = [-np.pi/4, 0, np.pi/4]
        for i, viewDirection in enumerate(viewDirection):
            rayPosition = self.position
            step = self.turn(viewDirection, self.orientation)
            while not collide(rayPosition, step, world):
                returnValue[i] += 1
                rayPosition += step
        return returnValue
        
    
    def update(self, world):
        acceleration, angle = self.policy(self.velocity, self.view(world))
        self.orientation = self.turn(angle, self.orientation)
        self.velocity += acceleration
        if not collide(self.position, self.velocity*self.orientation, world):
            self.position += self.velocity*self.orientation
            self.policy = lambda x,y: (1,0)
        else: 
            self.velocity = 0
            self.policy = lambda x,y: (1, -np.pi/2)

    def turn(self, angle, orientation):
        return np.dot(np.array([[np.cos(angle), -np.sin(angle)], 
                         [np.sin(angle),  np.cos(angle)]]), orientation)

def collide(position, step, world):
    return squaredistance((position+step)[0], (position+step)[1], 20, 20) > world.outer**2 or squaredistance((position+step)[0], (position+step)[1],20, 20) < world.inner



class World:
    def __init__(self, inner, outer, goal=20):
        self.inner = inner
        self.outer = outer
        self.goal = goal
        self.frame = 0
        # TODO: make world have defined coordinate middle (now assumed to be (20, 20) by car collide)

    def draw(self, car, dimx = 80, dimy = 40):
        self.frame += 1
        os.system('clear')
        for y in range(dimy):
            for x in range(dimx):
                if (squaredistance(x/2, y, dimx/4, dimy/2) > self.inner**2) and (squaredistance(x/2, y, dimx/4, dimy/2) < (self.inner+2)**2):
                    print("X", end="")
                elif (squaredistance(x/2, y, dimx/4, dimy/2) > self.outer**2) and (squaredistance(x/2, y, dimx/4, dimy/2) < (self.outer+2)**2):
                    print("X", end="")
                elif within1x1(x/2, y, car.position[0], car.position[1]):
                    print("O", end="")
                else:
                    print(".", end="")
            print("")
        print("="*80)
        time.sleep(0.1)

def within1x1(x,y, carx, cary):
    return x-0.5<=carx and x+0.5>carx and y-0.5<=cary and y+0.5>cary

def squaredistance(positionx, positiony, centerx, centery):
    return (positionx-centerx)**2 + (positiony-centery)**2


w = World(5, 18)
car = SimpleCar(np.array([12.0, 28.0 ]), np.array([1,0 ]))
while True:
    w.draw(car)
    car.update(w)
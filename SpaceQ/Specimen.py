import numpy as np
import random, math
from SpaceGame import SpaceGame

def activation(value):
    return 0 if value < 0 else value

class Specimen:
    def __init__(self):
        # inputs:
        # 10x (asteroid x, y, xVel, yvel, radius) = 60
        # outputs:
        # movex, movey, aimx, aimy, shoot = 5
        self.NINPUTS = 25
        self.NOUTPUTS = 5
        self.NINTER = 0
        self.INTERSIZE = 10
        
        self.inputLayer =  np.zeros((self.INTERSIZE, self.NINPUTS)) 
        self.interLayers = np.zeros((self.INTERSIZE, self.INTERSIZE, self.NINTER)) 
        self.outputLayer = np.zeros((self.NOUTPUTS,  self.INTERSIZE)) 

        #rate = 1.0
        #for i in range(self.INTERSIZE):
        #    for j in range(self.NINPUTS):
        #        self.inputLayer[i, j] = random.gauss(0.0, rate)

        #for i in range(self.INTERSIZE):
        #    for j in range(self.INTERSIZE):
        #        for k in range(self.NINTER):
        #            self.interLayers[i, j, k] = random.gauss(0.0, rate)

        #for i in range(self.NOUTPUTS):
        #    for j in range(self.INTERSIZE):
        #        self.outputLayer[i, j] = random.gauss(0.0, rate)

        self.inputValues =  np.zeros((self.NINPUTS))
        self.outputValues = np.zeros((self.NOUTPUTS))

    def evaluate(self):
        terms = np.array([activation(np.dot(self.inputValues, self.inputLayer[i, :])) for i in range(self.INTERSIZE)])
        for i in range(self.NINTER):
            terms = np.array([activation(np.dot(terms, self.interLayers[j, :, i])) for j in range(self.INTERSIZE)])
        self.outputValues = np.array([np.dot(terms, self.outputLayer[i, :]) for i in range(self.NOUTPUTS)])

    def mutate(self):
        RATE = 1.0
        PROB = 0.05
        for i in range(self.INTERSIZE):
            for j in range(self.NINPUTS):
                if(random.random() < PROB):
                    self.inputLayer[i, j] += random.gauss(0.0, RATE)

        for i in range(self.INTERSIZE):
            for j in range(self.INTERSIZE):
                for k in range(self.NINTER):
                    if(random.random() < PROB):
                        self.interLayers[i, j, k] += random.gauss(0.0, RATE)    

        for i in range(self.NOUTPUTS):
            for j in range(self.INTERSIZE):
                if(random.random() < PROB):
                    self.outputLayer[i, j] += random.gauss(0.0, RATE)

    def calc_fitness(self, doRender=False):
        game = SpaceGame()
        return game.run(specimen=self, doRender=doRender)

    def apply_input(self, game):
        ship = game.playerShip

        asteroids = sorted(game.asteroids, key=lambda a: a.position.distance_squared_to(ship.position))
        if len(asteroids) > 5: asteroids = asteroids[0:4]

        for i in range(len(asteroids)):
            self.inputValues[5 * i + 0] = asteroids[i].position.x - ship.position.x
            self.inputValues[5 * i + 1] = asteroids[i].position.y - ship.position.y
            self.inputValues[5 * i + 2] = asteroids[i].moveDirection.x if abs(asteroids[i].moveDirection.x) > 0.5 else 0
            self.inputValues[5 * i + 3] = asteroids[i].moveDirection.y if abs(asteroids[i].moveDirection.y) > 0.5 else 0
            self.inputValues[5 * i + 4] = asteroids[i].radius

        for i in range(len(asteroids) * 5, 5 * 5):
            self.inputValues[i] = 0.0

        self.evaluate()

        ship.moveDirection.x = self.outputValues[0]
        ship.moveDirection.y = self.outputValues[1]
        ship.rotation = -math.degrees(math.atan2(self.outputValues[3], self.outputValues[2]))
        ship.isShooting = self.outputValues[4] > 0.5

import numpy as np
import random, math, pygame, json
from SpaceGame import SpaceGame

def activation(value):
    return 0 if value < 0 else value

OFFSETS = [
    pygame.Vector2(x, y) for x in [-800, 0, 800] for y in [-800, 0, 800]
    ]

def min_offset(point1, point2):
    candidates = (point2 - point1 + v for v in OFFSETS)
    return min(candidates, key=lambda v:v.length_squared())

class Specimen:
    def __init__(self):
        # inputs:
        # 10x (asteroid x, y, xVel, yvel, radius) = 60
        # outputs:
        # movex, movey, aimx, aimy, shoot = 5
        self.NINPUTS = 25
        self.NOUTPUTS = 5
        self.NINTER = 1
        self.INTERSIZE = 15
        
        self.inputLayer =  np.zeros((self.NINPUTS, self.INTERSIZE)) 
        self.interLayers = np.zeros((self.INTERSIZE, self.INTERSIZE, self.NINTER)) 
        self.outputLayer = np.zeros((self.INTERSIZE, self.NOUTPUTS)) 

        self.inputBias =   np.zeros((self.INTERSIZE))
        self.interBiases = np.zeros((self.INTERSIZE, self.NINTER))
        self.outputBias =  np.zeros((self.NOUTPUTS))

        self.inputValues =  np.zeros((self.NINPUTS))
        self.outputValues = np.zeros((self.NOUTPUTS))

    def save(self, filename):
        fs = open(filename, "w")
        json.dump({
            "inputLayer": self.inputLayer.tolist(),
            "interLayers": self.interLayers.tolist(),
            "outputLayer": self.outputLayer.tolist(),
            "inputBias": self.inputBias.tolist(),
            "interBiases": self.interBiases.tolist(),
            "outputBias": self.outputBias.tolist()
        }, fs)
        fs.close()

    def load(self, filename):
        fs = open(filename, "r")
        data = json.load(fs)
        self.inputLayer = np.array(data["inputLayer"])
        self.interLayers = np.array(data["interLayers"])
        self.outputLayer = np.array(data["outputLayer"])
        self.inputBias = np.array(data["inputBias"])
        self.interBiases = np.array(data["interBiases"])
        self.outputBias = np.array(data["outputBias"])
        print(self.inputLayer.shape, self.interLayers.shape, self.outputLayer.shape)
        print(self.inputBias.shape, self.interBiases.shape, self.outputBias.shape)
        fs.close()

    def evaluate(self):
        terms = np.dot(self.inputValues, self.inputLayer) + self.inputBias
        for i in range(self.NINTER):
            terms = np.array([activation(np.dot(terms, self.interLayers[j, :, i])) for j in range(self.INTERSIZE)]) + self.interBiases[:, i]
        self.outputValues = np.dot(terms, self.outputLayer) + self.outputBias

    def mutate(self):
        RATE = 1.0
        PROB = 0.05

        for i in range(self.NINPUTS):
            for j in range(self.INTERSIZE):
                if(random.random() < PROB):
                    self.inputLayer[i, j] += random.gauss(0.0, RATE)
        for i in range(self.INTERSIZE):
            for j in range(self.INTERSIZE):
                for k in range(self.NINTER):
                    if(random.random() < PROB):
                        self.interLayers[i, j, k] += random.gauss(0.0, RATE)    
        for i in range(self.INTERSIZE):
            for j in range(self.NOUTPUTS):
                if(random.random() < PROB):
                    self.outputLayer[i, j] += random.gauss(0.0, RATE)

        for i in range(self.INTERSIZE):
            if(random.random() < PROB):
                    self.inputBias[i] += random.gauss(0.0, RATE)
        for i in range(self.INTERSIZE):
            for j in range(self.NINTER):
                if(random.random() < PROB):
                        self.interBiases[i, j] += random.gauss(0.0, RATE)
        for i in range(self.NOUTPUTS):
            if(random.random() < PROB):
                    self.outputBias[i] += random.gauss(0.0, RATE)

    def calc_fitness(self, doRender=False):
        game = SpaceGame()
        return game.run(specimen=self, doRender=doRender)

    def apply_input(self, game):
        ship = game.playerShip

        offsets = {a:min_offset(ship.position, a.position) for a in game.asteroids}

        asteroids = sorted(game.asteroids, key=lambda a: offsets[a].length_squared())
        if len(asteroids) > 5: asteroids = asteroids[0:4]

        for i in range(len(asteroids)):
            self.inputValues[5 * i + 0] = offsets[asteroids[i]].x
            self.inputValues[5 * i + 1] = offsets[asteroids[i]].y
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

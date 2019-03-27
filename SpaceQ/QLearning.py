import numpy as np
import random

class QLearner:
    def __init__(self, nStates, nActions, alpha=0.1, gamma=0.8, epsilon=1.0, initialState=0):
        # alpha - learning rate
        # gamma - discount rate
        # epsilon - exploratoriness
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.nStates = nStates
        self.nActions = nActions
        self.qGrid = np.zeros((nStates, nActions))
        self.state = initialState

    def step(self, action, reward, newState=None):
        newState = self.state if newState == None else newState;
        self.qGrid[self.state, action] = (1.0 - alpha) * self.qGrid[self.state, action] + \
            alpha * (reward + self.gamma * max(self.qGrid[newState, :]))
        self.state = newState

    def chooseAction(self, forceBest=False):
        actions = self.qGrid[self.state, :]
        epsilon = 0.0 if forceBest else self.epsilon
        highest = max(actions)
        lowest = highest - epsilon
        candidates = (i for i in range(self.nActions) if lowest <= self.qGrid[self.state, i] <= highest)
        return random.choice(candidates)

testLearner = QLearner(5, 5);
import numpy as np
import random

class TDAgent:
    def __init__(self, states, actions, epsilon=0.7, alpha=0.1, gamma=0.1, epsilonDecay=0.9):
        self.q = {}
        self.actions = [i for i in range(actions)]
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilonDecay = epsilonDecay
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
    
    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
    
    def update(self, state, action, reward, newValue):
        currentQ = self.getQ(state, action)
        if currentQ == 0:
            self.q[(state, action)] = reward 
        else:
            self.q[(state, action)] = currentQ + self.alpha * (newValue - currentQ)
            
    def learn(self, state, action, reward, state2, action2):
        pass
        
    def act(self, state):
        if np.random.rand() < self.epsilon:
            action = random.choice(self.actions)
        else:
            q = [self.getQ(state, a) for a in self.actions] 
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [a for a in self.actions if q[a] == maxQ] 
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
            self.epsilon = self.epsilon * self.epsilonDecay
            
        return action

class SarsaAgent(TDAgent):
    
    def learn(self, state, action, reward, state2, action2):
        nextQ = self.getQ(state2, action2)
        self.update(state, action, reward, reward + self.gamma * nextQ)

class QLearnAgent(TDAgent):
    
    def learn(self, state, action, reward, state2, _):
        maxQ = max([self.getQ(state2, a) for a in self.actions])
        self.update(state, action, reward, reward + self.gamma * maxQ)

class ExpectedSarsaAgent(TDAgent):
    
    def learn(self, state, action, reward, state2):
        meanQ = mean([self.getQ(state2, a) for a in self.actions])
        self.updateQ(state, action, reward, reward + self.gamma * meanQ)


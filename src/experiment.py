# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:58:48 2015

@author: Netbook
"""

#from qLearningAgent import QLearningAgent
#from Environment import SimpleEnvironment
#
#env = SimpleEnvironment()
#agent = QLearningAgent(0.2,0.4)
#
#for k in range(1000):
#    #print 20*'='
#    state = env.getState()
#    #print "Current state: ", state
#    action=agent.selectAction(state)
#    #print "Selected action: ", action
#    newState,reward=env.applyAction(action)
#    #print "New state: ",newState, "\tReward: ",reward
#    agent.update(state,action,newState,reward)
#    #print 'Updated Q[',state,',',action,']: ', agent.QValues[(state,action)]
#    
#print 'Q[(2,4),(-1,-1)]: ', agent.QValues[(2,4),(-1,-1)]
#print 'Q[(1,1),(-1,-1)]: ', agent.QValues[(1,1),(-1,-1)]

from qLearningAgent import ApproximateQLearningAgent
from environment import MapStraight
import time

env = MapStraight([[0,4],[-7,-3.5]])

agent = ApproximateQLearningAgent(0.2,0.01,0.8,env.target)
env.start()


print "target:", env.target
for k in range(5000):
    #print 10*'='," iteration: ",k,10*'='
    state = env.getState()
    #print "Current state: ", state
    action=agent.selectAction(state)
    #print "Selected action: ", action
    newState,reward=env.applyAction(action)
    #print "New state: ",newState, "\tReward: ",reward
    if abs(reward)>40:
        print 10*'='," iteration: ",k,10*'='
        print "Reward: ",reward
    agent.update(state,action,newState,reward)
    #print 'Updated weights[',action,']: ', agent.QValues.weights[action]

env.stop()

print "Preparing optimal run..."
agent.eps=0.001
time.sleep(2)
env.start()
print "Running optimally"

for k in range(500):
    print 10*'='," iteration: ",k,10*'='
    state = env.getState()
    #print "Current state: ", state
    action=agent.selectAction(state)
    #print "Selected action: ", action
    newState,reward=env.applyAction(action)
    #print "New state: ",newState, "\tReward: ",reward
    agent.update(state,action,newState,reward)
    #print 'Updated weights[',action,']: ', agent.QValues.weights[action]

env.stop()
    
#print 'Q[(2,4),(-1,-1)]: ', agent.QValues[(2,4),(-1,-1)]
#print 'Q[(1,1),(-1,-1)]: ', agent.QValues[(1,1),(-1,-1)]
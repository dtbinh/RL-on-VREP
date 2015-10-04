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

env = MapStraight()
agent = ApproximateQLearningAgent(0.5,0.01,1,env.target)
env.start()

for k in range(50):
    print 10*'='," iteration: ",k,10*'='
    state = env.getState()
    print "Current state: ", state
    action=agent.selectAction(state)
    print "Selected action: ", action
    newState,reward=env.applyAction(action)
    print "New state: ",newState, "\tReward: ",reward
    agent.update(state,action,newState,reward)
    print 'Updated weights[',action,']: ', agent.QValues.weights[action]

env.stop()
    
#print 'Q[(2,4),(-1,-1)]: ', agent.QValues[(2,4),(-1,-1)]
#print 'Q[(1,1),(-1,-1)]: ', agent.QValues[(1,1),(-1,-1)]
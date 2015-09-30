# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 13:53:49 2015

@author: Netbook
"""

from tools import ZeroDict
import random

class QLearningAgent:
    
    def __init__(self,eps,alpha,discount=1):
        self.actions=((-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1))
        self.QValues = ZeroDict()
        self.eps=eps
        self.alpha=alpha
        self.discount=discount
        
    def getBestActionMaxQValue(self,state):
        maxQValue = -10000000000
        bestAction = None
        for action in self.actions:
            if self.QValues[(state,action)]>maxQValue:
                maxQValue = self.QValues[(state,action)]
                bestAction = action
        return (bestAction,maxQValue)
        
        
    def selectAction(self,state):  
        r=random.uniform(0,1)
        if r<self.eps:
            return self.actions[random.randint(0,len(self.actions)-1)]
        else:
            bestAction = self.getBestActionMaxQValue(state)[0]
            return bestAction
    
    def update(self, state, action, newState, reward):
        
        oldQValue=self.QValues[(state,action)]
        if newState==None:
            maxNewQValue=0
        else:
            maxNewQValue=self.getBestActionMaxQValue(newState)[1]
        
        self.QValues[(state,action)]=(1-self.alpha)*(oldQValue)+self.alpha*(reward+self.discount*maxNewQValue)
        
    def takeNewAction(self,env):
        state = env.getState()
        action=self.selectAction(self,state)
        newState,reward=env.applyAction(action)
        self.update(state,action,newState,reward)
        
        
        
        
            
            
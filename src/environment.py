# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:44:43 2015

@author: Netbook
"""

class SimpleEnvironment:
    def __init__(self):
        self.rewards=[[10]+4*[-1],5*[-1],5*[-1]]
        self.initState = [2,4]
        self.state = self.initState

    
    def applyAction(self,action):
        
        if self.state==[0,0]:
            self.reset()
            return None,self.rewards[0][0]
    
        newState=[0,0]
        newState[0] = self.state[0]+action[0]
        newState[1] = self.state[1]+action[1]
        
        if newState[0]<0:
            newState[0]=0
        if newState[0]>=len(self.rewards):
            newState[0]=len(self.rewards)-1
        
        if newState[1]<0:
            newState[1]=0
        if newState[1]>=len(self.rewards[0]):
            newState[1]=len(self.rewards[0])-1
        
        reward = self.rewards[self.state[0]][self.state[1]]
        self.state = newState
        
        return tuple(newState),reward
        
    def getState(self):
        return tuple(self.state)
        
    def reset(self):
        self.state = self.initState

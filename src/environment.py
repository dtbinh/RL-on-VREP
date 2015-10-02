# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:44:43 2015

@author: Netbook
"""
import vrep
from robot import Robot

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

class MapStraight:
    def __init__(self):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,2)
        if clientID==-1:
            raise Exception('Could not connect to API server')
            
        
        errorCodeCar,car = vrep.simxGetObjectHandle(clientID,'nakedAckermannSteeringCar',vrep.simx_opmode_oneshot_wait)
        
        if (errorCodeCar!=0):
                raise Exception('Could not get car handle')
        
        returnCode,position=vrep.simxGetObjectPosition(clientID,car,-1,vrep.simx_opmode_oneshot_wait)
        returnCode,orientation=vrep.simxGetObjectOrientation(clientID,car,-1,vrep.simx_opmode_oneshot_wait)
        
        
        errorCodeTarget,target = vrep.simxGetObjectHandle(clientID,'Target',vrep.simx_opmode_oneshot_wait)
        
        if (errorCodeTarget!=0):
                raise Exception('Could not get target handle')
        
        returnCode,targetPosition=vrep.simxGetObjectPosition(clientID,target,-1,vrep.simx_opmode_oneshot_wait)        
        
        if (returnCode!=0):
                raise Exception('Could not get target position')
                
        self.car = car
        
        self.clientID = clientID
        
        self.initState = [position[0],position[1],orientation[1],0,0]
        
        self.redPenalty = -5
        self.boundaries = [[-3, 7],[-7, 7]]
        
        self.redBoundaries=[1.5,2.5]
        
        self.state = self.initState
        self.robot = Robot(clientID)
        
        self.target = [targetPosition[0],targetPosition[1]]
        
    def start(self):
        returnCode = vrep.simxStartSimulation(self.clientID,vrep.simx_opmode_oneshot)
        if (returnCode>1):
            print "returnCode: ", returnCode
            raise Exception('Could not start')
        returnCode=vrep.simxSynchronous(self.clientID,True)
        
        for k in range(10): #Run to steps to step through initial "drop"
            returncode = vrep.simxSynchronousTrigger(self.clientID)
            
        if (returnCode!=0):
            raise Exception('Could not set synchronous mode')
                
    def stop(self):
        returnCode = vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_oneshot)
        self.robot.reset()
        if (returnCode>1):
            print "returnCode: ", returnCode
            raise Exception('Could not stop')
                
    def getState(self):
        returnCode,position=vrep.simxGetObjectPosition(self.clientID,self.car,-1,vrep.simx_opmode_oneshot_wait)
        returnCode,orientation=vrep.simxGetObjectOrientation(self.clientID,self.car,-1,vrep.simx_opmode_oneshot_wait)
        return [position[0],position[1],orientation[1],self.robot.desiredWheelRotSpeed,self.robot.desiredSteeringAngle]
                
    def calculateReward(self):
        if self.state[0]>self.redBoundaries[0] and self.state[0]<self.redBoundaries[1]:
            penalty=0
        else:
            penalty=-5
        
        return -(abs(self.state[0]-self.target[0])+abs(self.state[1]-self.target[1]))+penalty


    def applyAction(self, action):
        reward = self.calculateReward()
        self.robot.applyAction(action)
        returncode = vrep.simxSynchronousTrigger(self.clientID)
        newState = self.getState()
        self.state = newState
        return tuple(newState),reward
        
        
        
                
        
        
        
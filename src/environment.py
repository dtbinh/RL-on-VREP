# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:44:43 2015

@author: Netbook
"""
import vrep
import math
from robot import Robot

import time

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
    def __init__(self, initRobotPosition=[2.5, -6.5], boundaries=[[-3, 7],[-7, 7]], redPenalty = 0, rewardStrategy = 'Differential', actionStrategy = 'Absolute',verbose = False):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,2)
        if clientID==-1:
            raise Exception('Could not connect to API server')
            
        
        errorCodeCar,car = vrep.simxGetObjectHandle(clientID,'nakedAckermannSteeringCar',vrep.simx_opmode_oneshot_wait)
        
        errorCodeFrontRight,fr = vrep.simxGetObjectHandle(clientID,'Cylinder7',vrep.simx_opmode_oneshot_wait)
        errorCodeBackRight,br = vrep.simxGetObjectHandle(clientID,'Cylinder3',vrep.simx_opmode_oneshot_wait)
        
        if (errorCodeCar!=0):
                raise Exception('Could not get car handle')
                
        returnCode=vrep.simxSetObjectPosition(clientID,car,-1,[initRobotPosition[0],initRobotPosition[1],0.1],vrep.simx_opmode_oneshot_wait)
        
        returnCode,position=vrep.simxGetObjectPosition(clientID,car,-1,vrep.simx_opmode_oneshot_wait)
        
        returnCode,positionFR=vrep.simxGetObjectPosition(clientID,fr,-1,vrep.simx_opmode_oneshot_wait)
        returnCode,positionBR=vrep.simxGetObjectPosition(clientID,br,-1,vrep.simx_opmode_oneshot_wait)
        
        theta=math.atan2(positionFR[1]-positionBR[1],positionFR[0]-positionBR[0])
        
        errorCodeTarget,target = vrep.simxGetObjectHandle(clientID,'Target',vrep.simx_opmode_oneshot_wait)
        
        if (errorCodeTarget!=0):
                raise Exception('Could not get target handle')
        
        returnCode,targetPosition=vrep.simxGetObjectPosition(clientID,target,-1,vrep.simx_opmode_oneshot_wait)        
        
        if (returnCode!=0):
                raise Exception('Could not get target position')
                
        self.verbose = verbose
                
        self.car = car
        
        self.fr = fr
        self.br = br
        
        self.clientID = clientID

        self.boundaries = boundaries
        
        self.redBoundaries=[1.5,2.5]
        
        self.robot = Robot(clientID)
        
        self.target = [targetPosition[0],targetPosition[1]]
        
        self.initState = [position[0],position[1],theta,1*(self.redBoundaries[0]>position[0] or position[0]>self.redBoundaries[1]),0,0]
        
        self.state = self.initState
        
        self.wininngRadius = 0.5
        
        self.redPenalty = redPenalty
        
        self.rewardStrategy = rewardStrategy        
        
        self.actionStrategy = actionStrategy
        
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
        returnCode,positionFR=vrep.simxGetObjectPosition(self.clientID,self.fr,-1,vrep.simx_opmode_oneshot_wait)
        returnCode,positionBR=vrep.simxGetObjectPosition(self.clientID,self.br,-1,vrep.simx_opmode_oneshot_wait)
        
        theta=math.atan2(positionFR[1]-positionBR[1],positionFR[0]-positionBR[0])
        return [position[0],position[1],theta,1*(self.redBoundaries[0]>position[0] or position[0]>self.redBoundaries[1]),self.robot.desiredWheelRotSpeed,self.robot.desiredSteeringAngle]
                
    def calculateRewardSingle(self):
        if self.state[0]<self.boundaries[0][0] or self.state[0]>self.boundaries[0][1] or self.state[01]<self.boundaries[1][0] or self.state[1]>self.boundaries[1][1]:
            return -50
        
        elif abs(self.target[0]-self.state[0])+abs(self.target[1]-self.state[1])<self.wininngRadius:
            return 50
            
        else:
            return -(abs(self.state[0]-self.target[0])+abs(self.state[1]-self.target[1]))+self.redPenalty*self.state[3]
            
    def calculateRewardPair(self,newState):
        if self.state[0]<self.boundaries[0][0] or self.state[0]>self.boundaries[0][1] or self.state[01]<self.boundaries[1][0] or self.state[1]>self.boundaries[1][1]:
            return -50
        
        elif abs(self.target[0]-self.state[0])+abs(self.target[1]-self.state[1])<self.wininngRadius:
            return 50
            
        else:
            dOld=abs(self.state[0]-self.target[0])+abs(self.state[1]-self.target[1])
            dNew=abs(newState[0]-self.target[0])+abs(newState[1]-self.target[1])
            return dOld-dNew+self.redPenalty*newState[3]
    


    def applyAction(self, action):
        if self.state[0]<self.boundaries[0][0] or self.state[0]>self.boundaries[0][1] or self.state[1]<self.boundaries[1][0] or self.state[1]>self.boundaries[1][1] or (abs(self.target[0]-self.state[0])+abs(self.target[1]-self.state[1]))<self.wininngRadius:
            reward = self.calculateRewardSingle()            
            if self.verbose:            
                print "Terminal state: ", self.state, " - Reward: ", reward          
            self.state = self.initState
            self.stop()
            time.sleep(0.1) #100ms delay between stopping and starting to avoid problems
            self.start()
            return None,reward
        if (self.actionStrategy == 'Absolute'):
            self.robot.applyActionAbsolute(action)
        elif (self.actionStrategy == 'Differential'):
            self.robot.applyActionIncremental(action)
        else:
            print "Not valid action strategy"
            return
        returncode = vrep.simxSynchronousTrigger(self.clientID)
        newState = self.getState()
        if (self.rewardStrategy == 'Differential'):
            reward = self.calculateRewardPair(newState)
        elif (self.rewardStrategy == 'Absolute'):
            reward = self.calculateRewardSingle()
        else:
            print "Not valid reward strategy"
            return
        if self.verbose:
            print "From state: ", self.state, " applied action: ", action, " got reward: ", reward
        self.state = newState
        return tuple(newState),reward
        
        
        
                
        
        
        
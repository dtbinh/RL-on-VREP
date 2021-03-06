# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:02:02 2015

@author: a.porichis
"""
import vrep
import math

    
class Robot:
    
    def __init__(self,clientID):
        self.desiredSteeringAngle=0
        self.desiredWheelRotSpeed=0
        
        self.steeringAngleDx=2*math.pi/180
        self.wheelRotSpeedDx=1
        
        self.d=0.755
        self.l=2.5772
        
        self.clientID=clientID
        
        self.absSpeed={-1:-3,0:0,1:3}
        self.absAngle={-1:-8*math.pi/180,0:0,1:8*math.pi/180}
        
        
        errorCodeML,ml = vrep.simxGetObjectHandle(clientID,'nakedCar_motorLeft',vrep.simx_opmode_oneshot_wait)
        errorCodeMR,mr = vrep.simxGetObjectHandle(clientID,'nakedCar_motorRight',vrep.simx_opmode_oneshot_wait)
        errorCodeSL,sl = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringLeft',vrep.simx_opmode_oneshot_wait)
        errorCodeSR,sr = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringRight',vrep.simx_opmode_oneshot_wait)
        
        self.ml = ml
        self.mr = mr
        self.sl = sl
        self.sr = sr
    
    def reset(self):
        self.desiredSteeringAngle=0
        self.desiredWheelRotSpeed=0        

    def applyActionIncremental(self,action):
        if action[0]!=0:
            self.desiredWheelRotSpeed=self.desiredWheelRotSpeed+action[0]*self.wheelRotSpeedDx
            if self.desiredWheelRotSpeed>10*self.wheelRotSpeedDx:
                self.desiredWheelRotSpeed = 10*self.wheelRotSpeedDx
            elif self.desiredWheelRotSpeed<-10*self.wheelRotSpeedDx:
                self.desiredWheelRotSpeed = -10*self.wheelRotSpeedDx

            returnCode=vrep.simxSetJointTargetVelocity(self.clientID,self.ml,self.desiredWheelRotSpeed,vrep.simx_opmode_oneshot)
            returnCode=vrep.simxSetJointTargetVelocity(self.clientID,self.mr,self.desiredWheelRotSpeed,vrep.simx_opmode_oneshot)
            
        if action[1]!=0:
            self.desiredSteeringAngle=self.desiredSteeringAngle+action[1]*self.steeringAngleDx

            if self.desiredSteeringAngle>10*self.steeringAngleDx:
                self.desiredSteeringAngle = 10*self.steeringAngleDx
            elif self.desiredSteeringAngle<-10*self.steeringAngleDx:
                self.desiredSteeringAngle = -10*self.steeringAngleDx            
            
            steeringAngleLeft=math.atan(self.l/(-self.d+self.l/math.tan(self.desiredSteeringAngle+0.00001)))
            steeringAngleRight=math.atan(self.l/(self.d+self.l/math.tan(self.desiredSteeringAngle+0.00001)))
                
            returnCode=vrep.simxSetJointTargetPosition(self.clientID,self.sl,steeringAngleLeft,vrep.simx_opmode_oneshot)
            returnCode=vrep.simxSetJointTargetPosition(self.clientID,self.sr,steeringAngleRight,vrep.simx_opmode_oneshot)
    
    def applyActionAbsolute(self,action):
        self.desiredWheelRotSpeed=self.absSpeed[action[0]]
        self.desiredSteeringAngle=self.absAngle[action[1]]
        
        returnCode=vrep.simxSetJointTargetVelocity(self.clientID,self.ml,self.desiredWheelRotSpeed,vrep.simx_opmode_oneshot)
        returnCode=vrep.simxSetJointTargetVelocity(self.clientID,self.mr,self.desiredWheelRotSpeed,vrep.simx_opmode_oneshot)
        
        steeringAngleLeft=math.atan(self.l/(-self.d+self.l/math.tan(self.desiredSteeringAngle+0.00001)))
        steeringAngleRight=math.atan(self.l/(self.d+self.l/math.tan(self.desiredSteeringAngle+0.00001)))
                
        returnCode=vrep.simxSetJointTargetPosition(self.clientID,self.sl,steeringAngleLeft,vrep.simx_opmode_oneshot)
        returnCode=vrep.simxSetJointTargetPosition(self.clientID,self.sr,steeringAngleRight,vrep.simx_opmode_oneshot)

"""vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

errorCodeML,ml = vrep.simxGetObjectHandle(clientID,'nakedCar_motorLeft',vrep.simx_opmode_oneshot_wait)
errorCodeMR,mr = vrep.simxGetObjectHandle(clientID,'nakedCar_motorRight',vrep.simx_opmode_oneshot_wait)
errorCodeSL,sl = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringLeft',vrep.simx_opmode_oneshot_wait)
errorCodeSR,sr = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringRight',vrep.simx_opmode_oneshot_wait)

desiredSteeringAngle=0
desiredWheelRotSpeed=0

steeringAngleDx=2*math.pi/180
wheelRotSpeedDx=-1

d=0.755
l=2.5772

desiredWheelRotSpeed=desiredWheelRotSpeed+wheelRotSpeedDx
desiredSteeringAngle=desiredSteeringAngle+steeringAngleDx

steeringAngleLeft=math.atan(l/(-d+l/math.tan(desiredSteeringAngle)))
steeringAngleRight=math.atan(l/(d+l/math.tan(desiredSteeringAngle)))

returnCode=vrep.simxSetJointTargetPosition(clientID,sl,steeringAngleLeft,vrep.simx_opmode_oneshot_wait)
returnCode=vrep.simxSetJointTargetPosition(clientID,sr,steeringAngleRight,vrep.simx_opmode_oneshot_wait)

returnCode=vrep.simxSetJointTargetVelocity(clientID,ml,desiredWheelRotSpeed,vrep.simx_opmode_oneshot_wait)
returnCode=vrep.simxSetJointTargetVelocity(clientID,mr,desiredWheelRotSpeed,vrep.simx_opmode_oneshot_wait)"""


import numpy as np
import math
from datetime import datetime

class Glove():
    def __init__(self,sensor,acc_vect):
        self.sensor = sensor #gyro sensor is degrees/sec need to convert to radians
        self.mag_vect = np.array([1,0,0])
        self.acc_vect = acc_vect
        
        #position to the start attitude
        self.current_x = 0
        self.current_y = 0
        self.current_z = 0
        
        #speed to the start attitude not current
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        
        self.previousT = 0#?
        
        self.angle_x = 0  #radians
        self.angle_y = 0
        self.angle_z = 0
        self.angle_x,self.angle_y = AccVectorToRollPitchAngle(self.acc_vect)
        self.angle_z = Wrap360Rad(MagVectorToYawAngle(self.mag_vect,self.angle_x,self.angle_y))

        self.gyro_offset = np.array([-2.58,8.28,-0.84])

        self.acc_rest_count_x = 0
        self.acc_rest_count_y = 0
        self.acc_rest_count_z = 0

        self.perivious_accel_vect = []

        self.g = 9.80665

    def getPosition(self):
        return [self.current_x,self.current_y,self.current_z]

    def getSpeed(self):
        return [self.speed_x,self.speed_y,self.speed_z]

    def getAngle(self):
        return [math.degrees(self.angle_x),math.degrees(self.angle_y),math.degrees(self.angle_z)]

    def updateAttitude(self):
        if self.previousT == 0:
            gyro_x, gyro_y, gyro_z = self.sensor.gyro #需要再来一个陀螺仪的类?
            accel_x, accel_y, accel_z = self.sensor.acceleration
            self.previousT = datetime.now()
            return

        self.previousT = datetime.now()
        gyro_x, gyro_y, gyro_z = self.sensor.gyro #需要再来一个陀螺仪的类?
        accel_x, accel_y, accel_z = self.sensor.acceleration
        deltaT = (self.previousT - datetime.now()).total_seconds()
        
        deltaAngle_x = math.radians(gyro_filter((gyro_x - self.gyro_offset_x))*deltaT)
        deltaAngle_y = math.radians(gyro_filter((gyro_y - self.gyro_offset_y))*deltaT)
        deltaAngle_z = math.radians(gyro_filter((gyro_z - self.gyro_offset_z))*deltaT)
        
        #get the DCM matrix
        DCM = EulerAngleToDCM(deltaAngle_x,deltaAngle_y,deltaAngle_z)

        #update attitude vector
        self.mag_vect = np.dot(DCM,self.mag_vect)
        self.acc_vect = np.dot(DCM,self.acc_vect)

        self.angle_x,self.angle_y = AccVectorToRollPitchAngle(self.acc_vect)
        self.angle_z = Wrap360Rad(MagVectorToYawAngle(self.mag_vect,self.angle_x,self.angle_y))

        self.updateSpeed(accel_x, accel_y, accel_z,deltaT)

    def updateSpeed(self,accel_x, accel_y, accel_z,deltaT):
##        accel_x, accel_y, accel_z = self.sensor.acceleration #需要再来一个加速计的类
        
        DCM_T = EulerAngleToDCM_T(self.angle_x,self.angle_y,self.angle_z)
        accel_vect = np.subtract(np.dot(DCM_T,np.array([accel_x, accel_y, accel_z])),[0,0,self.g])
        
##        try:
        self.speed_x += accel_vect[0] * deltaT
        self.speed_y += accel_vect[1] * deltaT
        self.speed_z += accel_vect[2] * deltaT
##        except:
##            
##        self.perivious_accel_vect = accel_vect

        self.current_x += self.speed_x * deltaT
        
        if self.speed_x == 0:
            if accel_vect[0] != 0:
                self.acc_rest_count_x = 0
        else:
            if accel_vect[0] == 0:
                self.acc_rest_count_x += 1
            if self.acc_rest_count_x > 25:
                self.speed_x = 0
                self.acc_rest_count_x = 0

        if self.speed_y == 0:
            if accel_vect[1] != 0:
                self.acc_rest_count_y = 0
        else:
            if accel_vect[1] == 0:
                self.acc_rest_count_y += 1
            if self.acc_rest_count_y > 25:
                self.speed_y = 0
                self.acc_rest_count_y = 0        
        
        if self.speed_z == 0:
            if accel_vect[2] != 0:
                self.acc_rest_count_z = 0
        else:
            if accel_vect[2] == 0:
                self.acc_rest_count_z += 1
            if self.acc_rest_count_z > 25:
                self.speed_z = 0
                self.acc_rest_count_z = 0

                
                
def accel_vect_filter(accel_vect):
    for i in range(3):
        if abs(accel_vect[i]) < 0.001:
            accel_vect[i] = 0
            
def gyro_filter(gyro):
    if abs(gyro) < 0.3:
        return 0
    
def EulerAngleToDCM_T(x,y,z):
    cosX = math.cos(x)
    cosY = math.cos(y)
    cosZ = math.cos(z)
    sinX = math.sin(x)
    sinY = math.sin(y)
    sinZ = math.sin(z)
    DCM_T = np.array([[cosY*cosZ,-sinX*cosY,-sinY],
                   [sinZ*cosX+sinX*sinY*cosZ,cosX*cosZ - sinX*sinY*sinZ,sinX*cosY],
                   [-sinX*sinZ+sinY*cosX*cosZ,-sinX*cosZ-sinY*sinZ*cosX,cosX*cosY]],
                   dtype = 'float')
    return DCM_T

def EulerAngleToDCM(x,y,z):
    cosX = math.cos(x)
    cosY = math.cos(y)
    cosZ = math.cos(z)
    sinX = math.sin(x)
    sinY = math.sin(y)
    sinZ = math.sin(z)
    DCM = np.array([[cosY*cosZ,sinZ*cosX+sinX*sinY*cosZ,-sinX*sinZ+sinY*cosX*cosZ],
                   [-sinZ*cosY,cosX*cosZ - sinX*sinY*sinZ,-sinX*cosZ-sinY*sinZ*cosZ],
                   [-sinY,sinX*cosY,cosX*cosY]],
                   dtype = 'float')
    return DCM
        

def AccVectorToRollPitchAngle(acc_vect):
    acc_vect_n = normalize3(acc_vect[0],acc_vect[1],acc_vect[2])
    return [-math.asin(acc_vect_n[1]),math.atan2(acc_vect_n[0],acc_vect_n[2])]


def MagVectorToYawAngle(mag_vect,angle_x,angle_y):
    mag_vect_n = normalize3(mag_vect[0],mag_vect[1],mag_vect[2])
    DCM_T = EulerAngleToDCM_T(angle_x,angle_y,0)
    mag_vect_n = np.dot(DCM_T,np.array(mag_vect_n))
    return -math.atan2(mag_vect_n[1],mag_vect_n[0])
    
def Wrap360Rad(rad):
    if rad > 2* math.pi:
        rad -= 2* math.pi
    elif rad < 0:
        rad += 2* math.pi
    return rad

def normalize3(x,y,z):
    a = sum([x,y,z])
    return [x/a,y/a,z/a]

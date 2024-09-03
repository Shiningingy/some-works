import time
import board
import busio
import adafruit_lsm9ds1

import tkinter as tk
from tkinter import Label
import threading
from Glove import *
from Finger import *


# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

class testGui():
    def __init__(self):
        self.label = []
        
    def addlabel(self,new_label):
        self.label.append(new_label)

        

def Display(a):
    root = tk.Tk()
    label1 = Label(root,text = "angel_x = ")
    a.addlabel(label1)
    label2 = Label(root,text = "angel_y = ")
    a.addlabel(label2)
    label3 = Label(root,text = "angel_z = ")
    a.addlabel(label3)
    label4 = Label(root,text = "speed_x = ")
    a.addlabel(label4)
    label5 = Label(root,text = "speed_y = ")
    a.addlabel(label5)
    label6 = Label(root,text = "speed_z = ")
    a.addlabel(label6)
    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()
    label5.pack()
    label6.pack()
    root.mainloop()
    
a = testGui()
accel_x, accel_y, accel_z = sensor.acceleration
accel_vect_x,accel_vect_y,accel_vect_z = normalize3(accel_x, accel_y, accel_z)
gl = Glove(sensor,np.array([accel_vect_x,accel_vect_y,accel_vect_z]))
t = threading.Thread(target = Display,args = (a,))
t.setDaemon(True)
t.start()
time.sleep(1)
while True:
    gl.updateAttitude()
    angles = gl.getAngle()
    speeds = gl.getSpeed()
    a.label[0]["text"] = "angel_x = " + str(angles[0]) + "degrees"
    a.label[1]["text"] = "angel_y = " + str(angles[1]) + "degrees"
    a.label[2]["text"] = "angel_z = " + str(angles[2]) + "degrees"
    a.label[3]["text"] = "speed_x = " + str(speeds[0])
    a.label[4]["text"] = "speed_y = " + str(speeds[1])
    a.label[5]["text"] = "speed_z = " + str(speeds[2])
    time.sleep(0.0002)




    

##while True:
##    # Read acceleration, magnetometer, gyroscope, temperature.
##    accel_x, accel_y, accel_z = sensor.acceleration
##    mag_x, mag_y, mag_z = sensor.magnetic
##    gyro_x, gyro_y, gyro_z = sensor.gyro
##    accel_vect_x,accel_vect_y,accel_vect_z = normalize3(accel_x, accel_y, accel_z)
##    init_x = -math.arcsin(accel_vect_y)
##    init_y = math.arctan2(accel_vect_x,accel_vect_z)
##    mag_vect_x, mag_vect_y, mag_vect_z = normalize3(mag_x, mag_y, mag_z)
##    DCM_T = EulerAngleToDCM_T(init_x,init_y,0)
##    mag_vect_x, mag_vect_y, mag_vect_z = np.dot(DCM_T,array[mag_vect_x, mag_vect_y, mag_vect_z])
##    init_z = -math.arctan2(mag_vect_y,mag_vect_x)
##    print(toDegree(init_x))
##    print(toDegree(init_y))
##    print(toDegree(init_z))
##    time.sleep(1.0)

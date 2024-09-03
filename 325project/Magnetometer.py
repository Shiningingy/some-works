import numpy as np
from datetime import datetime

class Magnetometer:
    def __init__(self,sensor,filename = "MagnetometerData.txt"):
        self.sensor = sensor
        self.caliOffset_x = 0
        self.caliOffset_y = 0
        self.caliOffset_z = 0
        
        self.caliScale_x = 1
        self.caliScale_y = 1
        self.caliScale_z = 1
        
        self.earthMag = 0.4
        try:
            file = open(filename)
            data = file.readlines()
            data = [d.split('=')[1].split('\n')[0] for d in data]
            for i in range(len(data)):
                data[i] = float(data[i])
                
            self.caliOffset_x,self.caliOffset_y,self.caliOffset_z,self.caliScale_x,self.caliScale_y,self.caliScale_z,self.earthMag = data
            file.close()
        except:
            print("data file do not exist, please run the calibration!")




        self.data_x = 0
        self.data_y = 0
        self.data_z = 0
            

        

##    def magCaliDataInit(self,filename = None):
##        pass
##    #read file

    def magGetData(self):
        magRaw_x,magRaw_y,magRaw_z = self.sensor.magnetic
        
        self.data_x = (magRaw_x - self.caliOffseT_x) * self.caliScale_x;
        self.data_y = (magRaw_y - self.caliOffset_y) * self.caliScale_y;
        self.data_z = (magRaw_z - self.caliOffset_z) * self.caliScale_z;

        self.mag = self.mag * 0.99 + Pythagorous3(self.data_x, self.data_y, self.data_z) / self.earthMag * 0.01

        return self.data_x,self.data_y,self.data_z

    
    def magCalibration(self,Start = False):
        if Start:
            self.samples = [0] * 6 #Max_x,Min_x ... Max_z,Min_z
            self.cnt_m = 0
            self.cali_rotate_angle = 0
            self.new_offset = 0
            self.new_scale = 0
            self.earthMag_cali = 0
            self.should_cali = True
            self.cali_step = 1
            self.cali_success = False
            self.previousT = 0
        

        try:
            deltaT = (datetime.now() - self.previousT).total_seconds
        except:
            deltaT = (datetime.now()- datetime.now()).total_seconds
        self.previousT = datetime.now()

        if self.should_cali:
            magRaw_x,magRaw_y,magRaw_z = self.sensor.magnetic
            gyro_x,gyro_y,gyro_z = self.sensor.gyro
            if self.cali_step == 1:
                self.cali_rotate_angle += gyro_z * deltaT
            elif self.cali_step == 2:
                self.cali_rotate_angle += gyro_x * deltaT
                
        if self.cnt_m == 0:
            self.cali_step = 1
            self.cali_rotate_angle = 0
            self.cnt_m += 1
            
        elif self.cnt_m == 1:
            self.earthMag_cali = Pythagorous3(magRaw_x, magRaw_y, magRaw_z);
            for i in range(6):
                self.samples[i] = [magRaw_x,magRaw_y,magRaw_z]
            self.cnt_m += 1

        else:
            self.earthMag_cali = self.earthMag_cali * 0.998 + Pythagorous3(magRaw_x,magRaw_y,magRaw_z) * 0.002

            if (Pythagorous3(magRaw_x,magRaw_y,magRaw_z) < self.earthMag_cali * 1.5):
                if magRaw_x > self.samples[0][0]:
                    LowPassFilter1st(self.samples[0],[magRaw_x,magRaw_y,magRaw_z], 0.3)

                if magRaw_x < self.samples[1][0]:
                    LowPassFilter1st(self.samples[1],[magRaw_x,magRaw_y,magRaw_z], 0.3)                

                if magRaw_y > self.samples[2][1]:
                    LowPassFilter1st(self.samples[2],[magRaw_x,magRaw_y,magRaw_z], 0.3)

                if magRaw_y < self.samples[3][1]:
                    LowPassFilter1st(self.samples[3],[magRaw_x,magRaw_y,magRaw_z], 0.3)   

                if magRaw_z > self.samples[4][2]:
                    LowPassFilter1st(self.samples[4],[magRaw_x,magRaw_y,magRaw_z], 0.3)

                if magRaw_z < self.samples[5][2]:
                    LowPassFilter1st(self.samples[5],[magRaw_x,magRaw_y,magRaw_z], 0.3)
            else:
                self.earthMag_cali = self.earthMag_cali


##            if(self.cali_step == 1)
##               print(abs(self.cali_rotate_angle) / 72);
##            elif(self.cali_step == 2)
##               print((abs(self.cali_rotate_angle) + 360) / 72);
            
            if(self.cali_step == 1 and abs(self.cali_rotate_angle) > 360):
                self.cali_step = 2
                self.cali_rotate_angle = 0
                print("Magnetometer cali step1 done!")

            
            if(self.cali_step == 2 and abs(self.cali_rotate_angle) > 360):
                self.cnt_m = 0
                self.should_cali = False
                self.cali_step = 3
                self.cali_rotate_angle = 0
                self.earthMag_cali = 0
                print("Magnetometer cali step2 done!")

                for i in range(3):
                    self.earthMag_cali += Pythagorous3((self.samples[i*2][0] - self.samples[i*2+1][0]) * 0.5,
                                                       (self.samples[i*2][1] - self.samples[i*2+1][1]) * 0.5,
                                                       (self.samples[i*2][2] - self.samples[i*2+1][2]) * 0.5)

                self.earthMag_cali /= 3

                initBeta = []
                initBeta.append((self.samples[0][0] + self.samples[1][0]) * 0.5)
                initBeta.append((self.samples[2][1] + self.samples[3][1]) * 0.5)
                initBeta.append((self.samples[4][2] + self.samples[5][2]) * 0.5)
                initBeta.append(1/self.earthMag_cali)
                initBeta.append(1/self.earthMag_cali)
                initBeta.append(1/self.earthMag_cali)

                new_offset, new_scale = LevenbergMarquardt(self.samples,initBeta,self.earthMag_cali)

                if (new_scale[0] == None) or (new_scale[1] == None) or (new_scale[2] == None):
                    self.cali_success = False
                elif (abs(new_scale[0] - 1.0) > 0.8) or (abs(new_scale[1] - 1.0) > 0.8) or (abs(new_scale[2] - 1.0) > 0.8):
                    self.cali_success = False
                elif (abs(new_offset[0])> self.earthMag_cali*2) or (abs(new_offset[1])> self.earthMag_cali*2) or (abs(new_offset[2])> self.earthMag_cali*2):
                    self.cali_success = False
                else:
                    self.cali_success = True

                if self.cali_success:
                    self.caliOffset_x,self.caliOffset_y,self.caliOffset_z = new_offset
                    self.caliScale_x,self.caliScale_y,self.caliScale_z = new_scale
                    self.earthMag = self.earthMag_cali
                    print("cali success!")
                    file = open("MagnetometerData.txt",'w')   
                    file.write("caliOffset_x = " + str(self.caliOffset_x))
                    file.write("caliOffset_y = " + str(self.caliOffset_y))
                    file.write("caliOffset_z = " + str(self.caliOffset_z))
                    file.write("caliScale_x = " + str(self.caliScale_x))
                    file.write("caliScale_y = " + str(self.caliScale_y))
                    file.write("caliScale_z = " + str(self.caliScale_z))
                    file.write("earthMag = " + str(self.earthMag))
                    f.close()
                    
                self.cali_step = 0
                self.earthMag_cali = 0
                        
                        
                    

def Pythagorous3(x,y,z):
    a = np.array([x,y,z])
    return np.linalg.norm(x)







            

class lpf_data:
    def __init__(self):
        self.b0 = 0
        self.a1 = 0 
        self.a2 = 0
        self.preout_x = 0
        self.preout_y = 0
        self.preout_z = 0
        self.lastout_x = 0
        self.lastout_y = 0
        self.lastout_z = 0
        
    def setb0(self,b0):
        self.b0 = b0

    def seta1(self,a1):
        self.a1 = a1
        
    def seta2(self,a2):
        self.a2 = a2
        
    def setpreout_x(self,preout_x):
        self.preout_x = preout_x

    def setpreout_y(self,preout_y):
        self.preout_y = preout_y
        
    def setpreout_z(self,preout_z):
        self.preout_z = preout_z

    def setlastout_x(self,lastout_x):
        self.lastout_x = lastout_x

    def setlastout_y(self,lastout_y):
        self.lastout_y = lastout_y

    def setlastout_z(self,lastout_z):
        self.lastout_z = lastout_z

        
def normalize3(x,y,z):
    a = sum([x,y,z])
    return [x/a,y/a,z/a]


def EulerAngleToDCM_T(x,y,z):
    cosX = math.cos(x)
    cosY = math.cos(y)
    cosZ = math.cos(z)
    sinX = math.sin(x)
    sinY = math.sin(y)
    sinZ = math.sin(z)
    DCM_T = np.array([cosY*cosZ,-sinX*cosY,-sinY],
                   [sinZ*cosX+sinX*sinY*cosZ,cosXcosZ - sinX*sinY*sinZ,sinx*cosY],
                   [-sinX*sinZ+sinY*cosX*cosZ,-sinX*cosZ-sinY*sinZ*cosX,cosX*cosY],
                   dtype = 'float')
    return DCM_T

def EulerAngleToDCM(x,y,z):
    cosX = math.cos(x)
    cosY = math.cos(y)
    cosZ = math.cos(z)
    sinX = math.sin(x)
    sinY = math.sin(y)
    sinZ = math.sin(z)
    DCM = np.array([cosY*cosZ,sinZ*cosX+sinX*sinY*cosZ,-sinX*sinZ+sinY*cosX*cosZ],
                   [-sinZ*cosY,cosXcosZ - sinX*sinY*sinZ,-sinX*cosZ-sinY*sinZ*cosZ],
                   [-sinY,sinX*cosY,cosX*cosY],
                   dtype = 'float')
    return DCM

def Pythagorous3(x,y,z):
    a = np.array([x,y,z])
    return np.linalg.norm(x)

def AccVectorToRollPitchAngle(acc_vect):
    acc_vect_n = normalize3(acc_vect[0],acc_vect[1],acc_vect[2])
    return [-math.arcsin(acc_vect_n[1]),math.arctan2(acc_vect_n[0],acc_vect_n[2])]

def MagVectorToYawAngle(mag_vect,angle_x,angle_y):
    mag_vect_n = normalize3(acc_vect[0],acc_vect[1],acc_vect[2])
    DCM_T = EulerAngleToDCM_T(angle_x,angle_y,0)
    mag_vect_n = np.dot(DCM_T,np.array(mag_vect_n))
    return [-math.arctan2(mag_vect_n[1],mag_vect_n[0])]

def Wrap360Rad(rad):
    if rad > 2* math.pi:
        rad -= 2* math.pi
    elif rad < 0:
        rad += 2* math.pi
    return rad
    
    

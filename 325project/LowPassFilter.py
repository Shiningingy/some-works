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
        
def LowPassFilter1st(data,newData,coff):
    data[0] = data[0] * (1-coff) + newData[0] * coff
    data[1] = data[1] * (1-coff) + newData[1] * coff
    data[2] = data[2] * (1-coff) + newData[2] * coff
    
    
def LowPassFilter2ndFactorCal(deltaT,Fcut,lpf_data):
    a = 1/(2*math.pi*Fcut*deltaT)
    lpf_data.setb0(1 / (a*a + 3*a + 1))
    lpf_data.seta1((2*a*a + 3*a) / (a*a + 3*a + 1))
    lpf_data.seta2((a*a) / (a*a + 3*a + 1))
    return lpf_data

def LowPassFilter2nd(lpf_2nd,rawData):
    lpf_2nd_data = [0] * 3
    lpf_2nd_data[0] =  rawData.x * lpf_2nd.b0 + lpf_2nd.lastout_x * lpf_2nd.a1 - lpf_2nd.preout_x * lpf_2nd.a2
    lpf_2nd_data[1] =  rawData.y * lpf_2nd.b0 + lpf_2nd.lastout_y * lpf_2nd.a1 - lpf_2nd.preout_y * lpf_2nd.a2
    lpf_2nd_data[2] =  rawData.z * lpf_2nd.b0 + lpf_2nd.lastout_z * lpf_2nd.a1 - lpf_2nd.preout_z * lpf_2nd.a2

    lpf_2nd.preout_x = lpf_2nd.lastout_x
    lpf_2nd.preout_y = lpf_2nd.lastout_y
    lpf_2nd.preout_z = lpf_2nd.lastout_z

    lpf_2nd.lastout_x = lpf_2nd_data[0]
    lpf_2nd.lastout_y = lpf_2nd_data[1]
    lpf_2nd.lastout_z = lpf_2nd_data[2]

    return lpf_2nd_data 

    

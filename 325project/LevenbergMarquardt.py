def LevenbergMarquardt(inputData,initBeta,length):
    cnt=0
    eps=1e-10
    change=100
    changeTemp=100
    data=[None]*3
    beta=[None]*6
    delta=[None]*6
    JtR=[None]*6
    JtJ=[]
    scale = [None]*3
    offset = [None]*3
    for i in range(6):
        JtJ.append([None]*6)
    
    for i in range(6):
        beta[i]=initBeta[i]
    global lm_lambda
    lm_lambda=0.1
    while change>eps:
        JtR,JtJ=ResetMatrices(JtR,JtJ)
        for i in range(6):
            data[0]=inputData[i][0]#x value
            data[1]=inputData[i][1]#y value
            data[2]=inputData[i][2]#z value
            JtR,JtJ=UpdateMatrices(JtR,JtJ,beta,data)
        delta=GaussEliminateSolveDelta(JtR, JtJ, delta)
        changeTemp=delta[0]*delta[0]+delta[0]*delta[0]+delta[1]*delta[1]+delta[2]*delta[2]+delta[3]*delta[3]/(beta[3]*beta[3])+delta[4]*delta[4]/(beta[4]*beta[4])+delta[5]*delta[5]/(beta[5]*beta[5])
        if changeTemp<change:
            lm_lambda/=3
            for i in range(6):
                beta[i]-=delta[i];
                change=changeTemp
        else:
            lm_lambda*=3
            if lm_lambda<0:
                lm_lambda=0
            if lm_lambda>1e10:
                lm_lambda=1e10
        cnt+=1
        if cnt>1000:
            break
    scale[0]=beta[3]*length
    scale[1]=beta[4]*length
    scale[2]=beta[5]*length
    offset[0]=beta[0]
    offset[1]=beta[1]
    offset[2]=beta[2]
    return scale,offset

def UpdateMatrices(JtR,JtJ,beta,data):
    residual=1
    jacobian=[None]*6
    for j in range(3):
        b=beta[3+j]
        dx=data[j]-beta[j]
        residual-=b*b*dx*dx
        jacobian[j]=2*b*b*dx
        jacobian[3+j]=-2*b*dx*dx
    for j in range(6):
        JtR[j]+=jacobian[j]*residual
        for k in range(6):
            JtJ[j][k]+=jacobian[j]*jacobian[k]
    return JtR,JtJ

def ResetMatrices(JtR,JtJ):
    for j in range(6):
        JtR[j]=0
        for k in range(6):
            JtJ[j][k]=0
    return JtR,JtJ

def GaussEliminateSolveDelta(JtR,JtJ,delta):
    for i in range(6):
        JtJ[i][i]+=lm_lambda
    for a in range(6):
        for j in range(a+1,6):
            mu=JtJ[a][j]/JtJ[a][a]
            if mu!=0:
                JtR[j]-=mu*JtR[a];
                for k in range(6):
                    JtJ[k][j]-=mu*JtJ[k][a]
    for b in range(5,-1,-1):
        JtR[b]/=JtJ[b][b]
        JtJ[b][b]=1
        for c in range(b):
            mu=JtJ[b][c]
            JtR[c]-=mu*JtR[b]
            JtJ[b][c]=0
    for d in range(6):
        delta[d]=JtR[d]
    return delta


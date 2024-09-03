class Finger():
    def __init__(self,mcp=None,resist,label=-1):
        self.label = label
        self.mcp = mcp
        self.resist = resist
        
    def getState(self):
        return round(self.resist*(1.023/self.mcp.read_adc(self.label)-1).2) #to x k Ohm



class HandAction():
    def __init__(self,thumb=None,forefinger=None,middlefinger=None):
        self.thumb = thumb
        self.forefinger = forefinger
        self.middlefinger = middlefinger
        self.current_action = 0 #0 = No action
                                #1 = l_press 2 = l_release 3 = l_press_hold
                                #4 = r_press 5 = r_release 6 = r_press_hold
                                #7 = Zoom_in 8 = Zoom_out 9 = Zoom_in_hold 10 = Zoom_out_hold
        self.perivious_Zoom = thumb.getState()

    def getCurrent_Action(self):
        return self.current_action

    def updateAction(self):
        if self.current_action == 0:
            if self.forefinger.getState() > 45: #l_press
                self.current_action = 1
            elif self.middlefinger.getState() > 45: #r_press
                self.current_action = 4
        elif self.current_action == 1:
            if self.forefinger.getState() < 37: #l_release
                self.current_action = 2
            elif self.forefinger.getState() > 45: #l_press_hold
                self.current_action = 3
        elif self.current_action == 2:
            if self.forefinger.getState() < 37: #l_release
                self.current_action = 0
            elif self.forefinger.getState() > 45: #l_press
                self.current_action = 1
        elif self.current_action == 3:
            if self.forefinger.getState() < 37: #l_release
                self.current_action = 2
            elif self.thumb.getState() - self.perivious_Zoom > 0: #Zoom_in
                self.current_action = 7
        elif self.current_action == 4:
            if self.middlefinger.getState() < 37: #r_release
                self.current_action = 5
            elif self.middlefinger.getState() > 45: #r_press_hold
                self.current_action = 6
        elif self.current_action == 5:
            if self.middlefinger.getState() < 37: #r_release
                self.current_action = 0
            elif self.middlefinger.getState() > 45: #r_press
                self.current_action = 4
        elif self.current_action == 6:
            if self.middlefinger.getState() < 37: #r_release
                self.current_action = 4
            elif self.thumb.getState() - self.perivious_Zoom < 0: #Zoom_out
                self.current_action = 8         
        elif self.current_action == 7:
            if self.forefinger.getState() < 37: #l_release
                self.current_action = 2
            elif self.thumb.getState() - self.perivious_Zoom > 0: #Zoom_in
                self.current_action = 7
            else:
                self.current_action = 9
        elif self.current_action == 8:
            if self.middlefinger.getState() < 37: #r_release
                self.current_action = 4
            elif self.thumb.getState() - self.perivious_Zoom < 0: #Zoom_out
                self.current_action = 8
            else:
                self.current_action = 10
        elif self.current_action == 9:
            if self.forefinger.getState() < 37: #l_release
                self.current_action = 2
            elif self.thumb.getState() - self.perivious_Zoom > 0: #Zoom_in
                self.current_action = 7
        elif self.current_action == 10:
            if self.middlefinger.getState() < 37: #l_release
                self.current_action = 2
            elif self.thumb.getState() - self.perivious_Zoom < 0: #Zoom_out
                self.current_action = 8
        self.perivious_Zoom = thumb.getState()      
        
            
                



def action_Filter(fingerState):
    pass
    

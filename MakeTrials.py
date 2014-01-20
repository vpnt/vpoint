'''
Created on Jul 26, 2013

@author: anonymized
'''


import Square
import random
import math
import pprint
import datetime
import json


TECHNIQUES = { 0: 'NoTess',
               1: 'TessNoViz',
               2: 'TessViz'}

TARGET_NUM = { 0: 3,
               1: 6,
               2: 12}

RESIZE = [False, True]

numSubjects = 12
numRepetitions = 5 


APP_SIZE = (1200, 904)


RANDOM_SIZE_RANGE = (0.10, 0.35)
WINDOW_POSITION_MARGIN  = 0.1
MARGIN_X = APP_SIZE[0] * WINDOW_POSITION_MARGIN
MARGIN_Y = APP_SIZE[1] * WINDOW_POSITION_MARGIN

TARGET_WINDOW_POSITION_RANGE = (0.1, 0.9)
TARGET_WINDOW_SCALE_RANGE = 0.3





class Trial:
    trials = 0
    
    def __init__(self, 
                 subjectID,                 # id of the test subject
                 techniqueID,               # technique: widget 1-3 or pose
                 numTargets,                # number of targets shown in this trial 
                 resize):                   # resize task or not ? 
        self.subjectID = subjectID
        self.trialID = Trial.trials
        # increment instance counter
        Trial.trials += 1
        self.techniqueID  = techniqueID
        self.numTargets = numTargets
        self.resize = resize 
        
        #print self.resize
        
        
        # set as 10 - 35 % of screen width height 
        controlWindowW = random.randint(int(APP_SIZE[0] *  RANDOM_SIZE_RANGE[0]) , int(APP_SIZE[0] * RANDOM_SIZE_RANGE[1]))
        controlWindowH = random.randint(int(APP_SIZE[1] *  RANDOM_SIZE_RANGE[0]) , int(APP_SIZE[1] * RANDOM_SIZE_RANGE[1]))
        
        marginX = int(APP_SIZE[0] * WINDOW_POSITION_MARGIN)
        marginY = int(APP_SIZE[1] * WINDOW_POSITION_MARGIN)
        
        controlWindowX = random.randint(marginX, APP_SIZE[0] - marginX - controlWindowW)
        controlWindowY = random.randint(marginY, APP_SIZE[1] - marginY - controlWindowH) 
        
        self.controlWindow = [controlWindowX, controlWindowY, controlWindowW, controlWindowH]
        
        self.targetWindow = self.createTargetWindow(self.controlWindow, self.resize)
        
        

    
    def as_dict(self):
        ''' return trial as dictionary '''
        return {"trialId" : self.trialID,
                "subjectId" : self.subjectID,
                "techniqueId" : self.techniqueID,
                "numTargets" : self.numTargets,
                "controlWindow" : self.controlWindow,
                "targetWindow" : self.targetWindow,
                "resize": int(self.resize)
                }
        
    def __repr__(self):
        ''' return as object '''
        return  str(self.as_dict())
    

    def randShifted(self, w):
        sr = TARGET_WINDOW_SCALE_RANGE
        return int((1.0 - ((2.0*random.random() * sr) - sr )) * w)
    
    
    def createTargetWindow(self, controlWin, resize):
        ''' Creates a target window, using constraints set at the top of this file '''
        
        if (resize == False):
            x,y,w,h = controlWin
        else:
            x,y,w,h = controlWin
            # add a random size change to the control window 
            w = self.randShifted(w)
            h = self.randShifted(h)
            
        # shiftable space
        if x > APP_SIZE[0] / 2:
            maxDx = APP_SIZE[0] - x
        else:
            maxDx = x
            
        if y > APP_SIZE[1] / 2:
            maxDy = APP_SIZE[1] - x
        else:
            maxDy = y
            
        # now calculdate the dx, dx
        
        
        if (maxDx < 0):
            # to the left
            dx = random.randint(int(maxDx * TARGET_WINDOW_POSITION_RANGE[1] + MARGIN_X), 
                                int(maxDx * TARGET_WINDOW_POSITION_RANGE[0] + MARGIN_X))
        else:
            # to the right 
            dx = random.randint(int(maxDx * TARGET_WINDOW_POSITION_RANGE[0] - MARGIN_X), 
                                int(maxDx * TARGET_WINDOW_POSITION_RANGE[1] - MARGIN_X))
            
        if (maxDy < 0):
            # to the left
            dy = random.randint(int(maxDy * TARGET_WINDOW_POSITION_RANGE[1] + MARGIN_Y), 
                                int(maxDy * TARGET_WINDOW_POSITION_RANGE[0] + MARGIN_Y))
        else:
            # to the right 
            dy = random.randint(int(maxDy * TARGET_WINDOW_POSITION_RANGE[0] - MARGIN_Y), 
                                int(maxDy * TARGET_WINDOW_POSITION_RANGE[1] - MARGIN_Y))
            
        return [dx, dy, w,h]
        
        
        
    
    
if __name__=="__main__":
    userTests = { } 
    techniques_square = Square.Square(len(TECHNIQUES.keys()))
    target_num_square = Square.Square(len(TARGET_NUM.keys()))
    resize_square = Square.Square(len(RESIZE))
    
    
    print target_num_square
    
    for userID in range(numSubjects):
        trials = [] 
        userTests[str(userID)] = trials
        print "Userid",userID
        # technique
        trialCtr = 0
        for technique_idx in techniques_square[userID % (len(techniques_square) - 1)]:
#            technique_tr = []
           
            for s in resize_square[userID % 2]:
                resizing = s
                # print technique_idx
                # repetitions
#                print "\t\t", resizing
                for r in range(numRepetitions):
                    # target values (ensure some separation of trial selection
                    # therefore +r
                    
                    for numTargetsIdx in target_num_square[(userID+r) % (len(target_num_square) - 1)]:
                        tValue = TARGET_NUM[numTargetsIdx]
#                        print ".",
                        
                        # pose stick (id = 0) and joysticks (id > 0) have different trial classes
                        trials.append( Trial(userID, technique_idx, tValue, resizing) ); 
                        trialCtr+=1
#                    print ""
                        
#                trials.append(trials)
            print "\tTechnique %d --> total %d" % (technique_idx,  len(trials))
        print "Total Overall",trialCtr, len(trials)
        print
            
            
    # warmup trials
#    warmup_trials = [ Trial(-1, 0, TARGET_NUM[t], False ) for t in range(len(TARGET_NUM.keys())) ]
#    warmup_trials += [ Trial(-1, 1, TARGET_NUM[t], False ) for t in range(len(TARGET_NUM.keys())) ]
    warmup_trials = [ Trial(-1, 2, TARGET_NUM[t], False )for t in range(len(TARGET_NUM.keys())) ]
#    warmup_trials += [ Trial(-1, 0, TARGET_NUM[t], True ) for t in range(len(TARGET_NUM.keys())) ]
#    warmup_trials += [ Trial(-1, 1, TARGET_NUM[t], True ) for t in range(len(TARGET_NUM.keys())) ]
    warmup_trials += [ Trial(-1, 2, TARGET_NUM[t], True )for t in range(len(TARGET_NUM.keys())) ]

    userTests["-1"] = warmup_trials
    
    now = datetime.datetime.now()

    
    pp = pprint.PrettyPrinter(width = 100)
    formatted = "# Finger Pose User Study definition file\n"
    formatted+= "#     Generated: " + datetime.date.today().isoformat() +"-"+now.strftime("%H-%M") +  "\n"
    formatted += "TRIALS = "  + pp.pformat(userTests)
    
    # print formatted
    # output as python module 
    f = open('Trials.py', 'w')
    f.write(formatted)
    f.close() 
    
    f = open('trials.json', 'w')
    son =  "["+json.dumps( str(userTests) )[1:-1]+"]"
    son = son.replace("'",'"')
    #print son
    f.write(son)
    f.close()
    
    
    # pp.pprint(son)
    
    #print "JSON Representation"
    #print pp.pformat(son)
    
        
        
    
        
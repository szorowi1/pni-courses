from numpy import ceil
from psychopy import clock, core, event, logging, visual

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define useful functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def QuitTask():
    W.close()
    core.quit()
    
def CheckForEscape():
    '''Check for 'escape' key.'''
    KeyPress = event.getKeys()
    if 'escape' in KeyPress: QuitTask()
    event.clearEvents()
    
def FixationBlock(sec):
    '''Block of fixation cross for XX seconds.'''
    
    ## Draw/log fixation cross.
    fix.draw()
    W.logOnFlip(level=logging.EXP, msg='Fixation cross')
    W.flip()
    
    ## Wait.
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        ## Check keys.
        CheckForEscape()
        
def HyperventilateBlock(sec):
    '''Block of hyperventilation for XX seconds.'''
   
    ## Prepare instructions.
    instr = ['Inhale','Inhale','Exhale','Exhale']
    instr = instr * (sec // 4) + instr[:sec % 4]

    ## Log onset of breath hold.
    logging.log(level=logging.EXP, msg='Hyperventilate')    
    
    ## Run breath-hold task.
    digit = 999
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        ## Get integer time of count.
        s = ceil(timer.getTime())
        
        ## If 1s has elapsed, update.
        if s < digit:
            digit = int(s)
            TopLine.setText(instr[sec-digit])
            TopLine.draw()
            BottomLine.setText('%0.0f' %(1 + digit % 2))
            BottomLine.draw()
            W.logOnFlip(level=logging.EXP, msg=instr[sec-digit])
            W.flip()
            
        ## Check keys.
        CheckForEscape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## Define block structure.
blocks = [FixationBlock, HyperventilateBlock, FixationBlock, HyperventilateBlock,
          FixationBlock, HyperventilateBlock, FixationBlock, HyperventilateBlock,
          FixationBlock, HyperventilateBlock, FixationBlock, HyperventilateBlock,
          FixationBlock]
timing = [10, 20, 40, 20, 40, 20, 40, 20, 40, 20, 40, 20, 40]
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Open log file.
msg = 'Initializing HYPERVENTILATE-CONTROL task.\n\nPlease enter subject ID.\n'
f = raw_input(msg)

## Open window.
W = visual.Window(fullscr=False, units='norm', color=[-1,-1,-1], autoLog=False)

## Prepare fixation cross.
fix = visual.GratingStim(W, mask='cross', units='norm', pos=(0,0), 
                         sf=0, size=(0.1,0.1), color=[1,1,1])

## Prepare text.
TopLine = visual.TextStim(W, units='norm', pos=(0,0.075), antialias=False, 
                          color=(1,1,1), autoLog=False)

BottomLine = visual.TextStim(W, units='norm', pos=(0,-0.075), antialias=False,
                             color=(1,1,1), autoLog = False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Wait for scanner.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## Before advancing to task, wait for scanner to
## send TTL pulse. To abort task, hit 'escape' key.

KeyPress, = event.waitKeys(keyList=['equal','escape'])
if KeyPress == 'escape': QuitTask()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Task.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## Run the task. To abort task, hit 'escape' key.
    
## Initialize logging.
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
logging.LogFile('%s-HYPERVENTILATE-CONTROL.log' %f, level=logging.EXP, filemode='w')
    
## Run task.
for block, sec in zip(blocks, timing): block(sec)
    
## Quit.
logging.log(level=logging.EXP, msg='Done')    
QuitTask()
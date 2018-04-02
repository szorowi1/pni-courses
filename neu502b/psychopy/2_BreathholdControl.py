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
        
def BreathHoldBlock(sec):
    '''Block of breathholding for XX seconds.'''
    
    ## Log onset of breath hold.
    logging.log(level=logging.EXP, msg='Breath hold')    
    
    ## Run breath-hold task.
    digit = 999
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        ## Get integer time of count.
        s = ceil(timer.getTime())
        
        ## If 1s has elapsed, update.
        if s < digit:
            digit = s
            BottomLine.setText('%0.0f' %digit)
            BottomLine.draw()
            TopLine.draw()
            W.flip()
            
        ## Check keys.
        CheckForEscape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## Define block structure.
blocks = [FixationBlock, BreathHoldBlock, FixationBlock, BreathHoldBlock,
          FixationBlock, BreathHoldBlock, FixationBlock, BreathHoldBlock,
          FixationBlock, BreathHoldBlock, FixationBlock, BreathHoldBlock,
          FixationBlock]
timing = [10, 20, 40, 20, 40, 20, 40, 20, 40, 20, 40, 20, 40]
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Open log file.
msg = 'Initializing BREATHHOLD-CONTROL task.\n\nPlease enter subject ID.\n'
f = raw_input(msg)

## Open window.
W = visual.Window(fullscr=False, units='norm', color=[-1,-1,-1], autoLog=False)

## Prepare fixation cross.
fix = visual.GratingStim(W, mask='cross', units='norm', pos=(0,0), 
                         sf=0, size=(0.1,0.1), color=[1,1,1])

## Prepare text.
TopLine = visual.TextStim(W, text='Breath Hold', units='norm', pos=(0,0.075), 
                          antialias=False, color=(1,1,1), autoLog=False)

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
logging.LogFile('%s-BREATHHOLD-CONTROL.log' %f, level=logging.EXP, filemode='w')
    
## Run task.
for block, sec in zip(blocks, timing): block(sec)
    
## Quit.
logging.log(level=logging.EXP, msg='Done')    
QuitTask()
from numpy import ceil
from psychopy import clock, core, event, logging, visual

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define useful functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def QuitTask():
    W.mouseVisible = True
    W.close()
    core.quit()
    
def CheckForEscape():
    '''Check for 'escape' key.'''
    KeyPress = event.getKeys(keyList=['escape'])
    if KeyPress: QuitTask()
    event.clearEvents()
    
def InstructionsBlock(sec):
    '''Present instructions for XX seconds.'''
    
    Instr = visual.TextStim(W, units='norm', pos=(0,0), antialias=False, bold=True, 
                            color=(139,0,0), colorSpace='rgb255', autoLog=False)
        
    ## Wait.
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        Instr.setText('%s in %0.0f' %(task, timer.getTime()))
        Instr.draw()
        W.flip()
        
        ## Check keys.
        CheckForEscape()
    
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
    
    ## Log onset of breath hold.
    logging.log(level=logging.EXP, msg='Hyperventilate')    
    
    ## Run breath-hold task.
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        Counter.setText('%0.0f' %(1 + ceil(timer.getTime()) % 2))
        Counter.draw()
        W.flip()
            
        ## Check keys.
        CheckForEscape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## Define block structure.
blocks = [FixationBlock, InstructionsBlock, HyperventilateBlock] * 6 + [FixationBlock]
timing = [7, 3, 20] + [37, 3, 20] * 5 + [40]
task = 'Hyperventilate'
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Open log file.
msg = 'Initializing HYPERVENTILATE-CONTROL task.\n\nPlease enter subject ID.\n'
f = raw_input(msg)

## Open window.
W = visual.Window(fullscr=True, units='norm', color=[-1,-1,-1], autoLog=False)
W.mouseVisible = False

## Prepare fixation cross.
fix = visual.GratingStim(W, mask='cross', units='norm', pos=(0,0), sf=0, size=(0.1,0.1), 
                         color=(139,0,0), colorSpace='rgb255')

## Prepare text.
Counter = visual.TextStim(W, units='norm', pos=(0,0), antialias=False, bold=True, 
                          color=(139,0,0), colorSpace='rgb255', autoLog = False)

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
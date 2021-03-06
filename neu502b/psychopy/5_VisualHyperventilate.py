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
        
def VisualHyperventilateBlock(rp, ap):
    '''Block of rotating checkerboard + breathhold.'''
    
    ## Prepare instructions.
    instr = ['Inhale','Inhale','Exhale','Exhale'] * 5
    
    ## Log onset of breath hold.
    logging.log(level=logging.EXP, msg='Hyperventilate')     
    
    ## Breath-hold only.
    timer = clock.CountdownTimer(10)
    while timer.getTime() > 0:
        
        ## Update text.
        Counter.setText('%0.0f' %(1 + ceil(timer.getTime()) % 2))
        Counter.draw()
        W.flip()
        
        ## Check keys.
        CheckForEscape()
        
    ## Log onset of radial checkerboard.
    logging.log(level=logging.EXP, msg='Checkerboard')     
        
    ## Breathhold + radial checkerboard.
    timer = clock.CountdownTimer(10)
    while timer.getTime() > 0:
        
        ## Update radial checkerboard.
        RCB.setRadialPhase(0.025, rp)
        RCB.setAngularPhase(0.025, ap)
        RCB.draw()
        
        ## Update text.
        Counter.setText('%0.0f' %(1 + ceil(timer.getTime()) % 2))
        Counter.draw()
        W.flip()
        
        ## Check keys.
        CheckForEscape()
        
    ## Log offset of breath-hold.
    logging.log(level=logging.EXP, msg='Hyperventilate end')     

    ## Radial checkerboard only.
    timer = clock.CountdownTimer(10)
    while timer.getTime() > 0:

        ## Update radial checkerboard.
        RCB.setRadialPhase(0.025, rp)
        RCB.setAngularPhase(0.025, ap)
        RCB.draw()
        fix.draw()
        W.flip()
        
        ## Check keys.
        CheckForEscape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## Define block structure.
blocks = [FixationBlock, InstructionsBlock, VisualHyperventilateBlock] * 6 + [FixationBlock]
timing = [7, 3, 30] + [27, 3, 30] * 5 + [30]
radial_phase  = ['', '', '+', '', '', '+', '', '', '-', '', '', '-', '', '', '+', '', '', '-', '']
angular_phase = ['', '', '+', '', '', '-', '', '', '-', '', '', '+', '', '', '-', '', '', '-', '']
task = 'Hyperventilate'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Open log file.
msg = 'Initializing VISUAL-HYPERVENTILATE task.\n\nPlease enter subject ID.\n'
f = raw_input(msg)

## Open window.
W = visual.Window(fullscr=True, units='norm', color=[-1,-1,-1], autoLog=False)
W.mouseVisible = False

## Prepare fixation cross.
fix = visual.GratingStim(W, mask='cross', units='norm', pos=(0,0), sf=0, size=(0.1,0.1), 
                         color=(139,0,0), colorSpace='rgb255')

## Prepare rotating checkerboard (RCB).
RCB = visual.RadialStim(W, units='norm', pos=(0,0), size=(1.5,1.5),
                        radialCycles=8, angularCycles=12, autoLog=False)

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
logging.LogFile('%s-VISUAL-HYPERVENTILATE.log' %f, level=logging.EXP, filemode='w')
    
## Run task.
for block, sec, rp, ap in zip(blocks, timing, radial_phase, angular_phase):
    
    if rp and ap: block(rp=rp, ap=ap)
    else: block(sec)
    
## Quit.
logging.log(level=logging.EXP, msg='Done')    
QuitTask()
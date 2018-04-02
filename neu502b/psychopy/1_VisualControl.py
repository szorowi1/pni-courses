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
        
def CheckerBoardBlock(sec, rp='+', ap='+'):
    '''Block of rotating checkerboard for XX seconds.'''
    
    ## Log onset of checkerboard.
    logging.log(level=logging.EXP, msg='Checkerboard')
    
    ## Run visual checkerboard.
    timer = clock.CountdownTimer(sec)
    while timer.getTime() > 0:
        
        ## Update radial checkerboard.
        RCB.setRadialPhase(0.025, rp)
        RCB.setAngularPhase(0.025, ap)
        RCB.draw()
        W.flip()

        ## Check keys.
        CheckForEscape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define experiment.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## Define block structure.
blocks = [FixationBlock, CheckerBoardBlock, FixationBlock, CheckerBoardBlock,
          FixationBlock, CheckerBoardBlock, FixationBlock, CheckerBoardBlock,
          FixationBlock, CheckerBoardBlock, FixationBlock, CheckerBoardBlock,
          FixationBlock]
timing = [10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
radial_phase  = ['', '+', '', '+', '', '-', '', '-', '', '+', '', '-', '']
angular_phase = ['', '+', '', '-', '', '-', '', '+', '', '-', '', '-', '']
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Preprations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Open log file.
msg = 'Initializing VISUAL-CONTROL task.\n\nPlease enter subject ID.\n'
f = raw_input(msg)

## Open window.
W = visual.Window(fullscr=False, units='norm', color=[-1,-1,-1], autoLog=False)

## Prepare fixation cross.
fix = visual.GratingStim(W, mask='cross', units='norm', pos=(0,0), 
                         sf=0, size=(0.1,0.1), color=[1,1,1])

## Prepare rotating checkerboard (RCB).
RCB = visual.RadialStim(W, units='norm', pos=(0,0), size=(1.5,1.5),
                        radialCycles=8, angularCycles=12, autoLog=False)

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
logging.LogFile('%s-VISUAL-CONTROL.log' %f, level=logging.EXP, filemode='w')
    
## Run task.
for block, sec, rp, ap in zip(blocks, timing, radial_phase, angular_phase):
    
    if rp and ap: block(sec, rp=rp, ap=ap)
    else: block(sec)
    
## Quit.
logging.log(level=logging.EXP, msg='Done')
QuitTask()
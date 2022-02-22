# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:20:27 2021

@author: MARC SABIO
"""
      
from psychopy import visual, core, event, data, prefs #import some libraries from PsychoPy
from pandas import DataFrame

import numpy as np

import conditions as cond # creating conditions
import stimuli as st # monitor and constant stimulus features
import instructions as instr # Instructions for each phase
import responses as rsp # Functions for gathering participant info, responses and RTs

# setting PTB as preferred sound lib
prefs.hardware['audioLib']=['pyo'] 
from psychopy.sound import Sound

subject_info = rsp.subject_info()
#============================= SETTING MONITOR ================================
# choosing monitor
monitor = st.monitor_def()[0]
mon = st.define_monitor(monitor) # select the correct monitor 

# Creating the window
win = visual.Window(size = mon.getSizePix(), monitor = mon , units="deg", screen=0, fullscr=False)
win.mouseVisible = False
ifi = 1000/monitor['Hz']

#=========================== Some general presets =============================

event.globalKeys.clear() # implementing a global event to quit the program at any time by pressing ctrl+q
event.globalKeys.add(key='q', modifiers=['ctrl'], func= win.close)

timer = core.Clock() # Multi-purpose clock
RT = None # Without this, if first trial is catch and participant doesn't respond in time,
          # the experiment will crash when trying to save variable RT
          
#============================== DESIGN PRESETS ================================
#Blocks
learning_n = 1 #per modality, so it's x2
test_n = 1 # x2 
mod_map = [0,1]
np.random.shuffle(mod_map) # Random starting modality
blocks_learning = np.concatenate([mod_map] * learning_n)  # 0 = VISUAL / 1 AUDITORY // Alternate them
blocks_test = np.concatenate([mod_map] * test_n)

#Transition matrix type
# 0 = with neutral items
# 1 = no neutral items. Half of them leading, the other half trailing (no repetitions)
# 2 = no neutral items. Items appear in both leading and trailing positions.
# 3 = Reduced. cardinals predict obliques (or viceversa)
# 4 = Frequent vs infrequent. Each leading item has 1 frequent trailing and 1 infrequent trailing. #Not implemented yet
tmt = 3

# Item type counts
n_items = 4 # number of different items
n_leading = 2 # Number of leading items
n_trailing = 2 # Number of trailing items
n_neutral = 1 # Number of neutral items (subset of leading). Only used if tmt == 0

# Pair type frequencies
nEXP = 6 # n of presentations of expected pairs
nVP = 2 # violations
nN = 3 # neutral pairs. Only used if tmt == 0. Must be different from nVP

# Loading constant stimuli information
stim = st.stim_config(ifi, n_items)
basic_stim = st.draw_basic(win, stim) 

# Generating pairs
if tmt == 0:
    vpairs = cond.stimlist_neutral(stim["oris"], "v", nEXP, nVP, nN, n_leading, n_trailing, n_neutral) # visual modality
    apairs = cond.stimlist_neutral(stim["freqs"], "a", nEXP, nVP, nN, n_leading, n_trailing, n_neutral) # auditory modality
elif tmt == 1:
    vpairs = cond.stimlist_noneutral(stim["oris"], "v", nEXP, nVP, n_leading, n_trailing) # visual modality
    apairs = cond.stimlist_noneutral(stim["freqs"], "a", nEXP, nVP, n_leading, n_trailing) # auditory modality
elif tmt == 2:
    vpairs = cond.stimlist_nn_repeat(stim["oris"], "v", nEXP, nVP, n_leading) # visual modality
    apairs = cond.stimlist_nn_repeat(stim["freqs"], "a", nEXP, nVP, n_leading) # auditory modality
elif tmt == 3:
    vpairs = cond.stimlist_reduced("v", nEXP, nVP, n_leading) # visual modality
    apairs = cond.stimlist_reduced("a", nEXP, nVP, n_leading) # auditory modality

    

# # Randomizing order of conditions and merging pairs info into single dict
# these_trials = cond.rand_conditions(vpairs, apairs) 

# Response mapping
maps = [0,1] # if 0 z = familiar & m = unfamiliar

# Catch trials in test phase? 0, no 1 yes
catch_test = 0

#========================== EXPERIMENT STARTS =================================

instr.main_instructions(win, basic_stim['grating_instr'], basic_stim['fixation_instr'], basic_stim['eye'], basic_stim['speaker_cross'])   

header = ['id', 'age', 'gender', 'hand', 'phase', 'block', 'modality', 'ntrial', 'v_pred', 'v_leading', 'v_trailing', 'a_pred', 'a_leading', 'a_trailing', 'catch', 'resp', 'RT']   # saving conditions here
#vars_stored = [['id', 'age', 'gender', 'hand', 'phase', 'block', 'modality', 'ntrial', 'v_pred', 'v_leading', 'v_trailing', 'a_pred', 'a_leading', 'a_trailing', 'catch', 'resp', 'RT']]   # saving conditions here
vars_stored = [] #for pandas
basic_stim['eye'].setPos([0,-12])
basic_stim['speaker'].setPos([0,-12]) # Different placement than during instructions

for phase in [0,1]:
    np.random.shuffle(maps) # random first mapping
    resp_map = np.concatenate([maps] * learning_n) # alternate mapping
    
    # Initializing corresponding phase instructions
    if phase == 0: 
        instr.learning_starts(win, basic_stim['grating'], basic_stim['fixation_point'], basic_stim['fixation_red'])
        instr.training_learn(win, basic_stim, stim) # 2 training trials 
        blocks = blocks_learning        

    else: #(fase == 1)
        instr.test_starts(win)
        instr.training_test(win, basic_stim, stim, monitor) # 2 training trials
        blocks = blocks_test
        

    block_n = 0 # counter to keep track of blocks within phase
    basic_stim["fixation_point"].color = [1,1,1] # Just to clean feedback color from a previous test phase
    for thisBlock in blocks:  #thisBlock == 0 VISUAL / thisBlock == 1 AUDITORY
        # Tracking block's modality
        thisMod = "visual" if thisBlock == 0 else 'auditory'
        reminder = basic_stim["eye"] if thisMod == "visual" else basic_stim["speaker"]   # Reminder: symbol of an eye or a speaker to appear on screen during trials,            
                                                                                        # So that participant can't forget which is the attended modality
        # Randomizing trials 
        #np.random.shuffle(these_trials)  
        # Randomizing order of conditions and merging pairs info into single dict
        these_trials = cond.rand_conditions(vpairs, apairs) 
        trials = data.TrialHandler(these_trials, 1, method='random') # Random method here doesn't randomize our trials, 
                                                                     # as each entry counts as a separate condition which appears just once   
        # Defining response mapping
        this_respmap = resp_map[block_n]
        
        # Instructions for this block            
        if phase == 0:
            instr.learning_visual(win) if thisMod == "visual" else instr.learning_auditory(win)
        else:
            instr.test_visual(win) if thisMod == "visual" else instr.test_auditory(win)
            # Here I also create a text stim to remind participants of response mapping in test phase
            test_keys = visual.TextStim(win, pos = [0,-8])
            test_keys.wrapWidth = 40
            test_keys.height = 1
            if this_respmap == 0: test_keys.text = "z = distorsionado            m = normal"
            else: test_keys.text = "z = normal            m = distorsionado"

#============================== TRIAL STARTS ==================================
       
        for thisTrial in trials:        
            thisResp = None
            leading_sound = Sound(thisTrial['a_leading'], sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
            trailing_sound = Sound(thisTrial['a_trailing'], sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
            basic_stim['grating'].setOpacity(0.5)
            for frame in range(stim['fixation_pre']):
                basic_stim["fixation_point"].draw()
                basic_stim['stim_contour'].draw() 
                reminder.draw()
                if phase == 1: test_keys.draw()
                win.flip()
            
            basic_stim["fixation_point"].color = [1,1,1] # From here until catch or negative fb fixation must be white
            basic_stim['grating'].ori = thisTrial['v_leading']  #updating leading grating ori
            leading_sound.play()
            for frame in range(stim['leading_frames']):       
                basic_stim["fixation_point"].draw()
                basic_stim['stim_contour'].draw()
                basic_stim['grating'].draw()
                reminder.draw()
                if phase == 1: test_keys.draw()
                win.flip()
                
            for frame in range(stim['isi_frames']): 
                basic_stim["fixation_point"].draw()
                basic_stim['stim_contour'].draw()
                reminder.draw()
                if phase == 1: test_keys.draw()
                win.flip()

#=============================== LEARNING ===================================== 
            if phase == 0:          
                basic_stim['grating'].ori = thisTrial['v_trailing']  #updating trailing grating ori
                if thisTrial['catch'] == 1: basic_stim["fixation_point"].color = [1,-1,-1]
                trailing_sound.play() 
                event.clearEvents() # Key presses are to be registered from here      
                for frame in range(stim['trailing_frames']):
                    basic_stim['stim_contour'].draw()
                    basic_stim['grating'].draw()
                    basic_stim["fixation_point"].draw()
                    reminder.draw()
                    win.flip() 

                timer.reset(0) # Reset timer when response screen is presented
                while thisResp == None:
                    thisResp = rsp.learning_Response(win, thisTrial, this_respmap) 
                RT = timer.getTime() # And get RT when a response is given
                basic_stim["fixation_point"].color = [1,1,1] # Make sure it goes back to white after catch
                     
 #=============================== TESTING =====================================             
            else:
                basic_stim['grating'].ori = thisTrial['v_trailing']  #updating trailing grating ori
                if thisTrial['target'] == 1 and thisMod == 'visual': #Checking if we need to set new opacity for grating
                    basic_stim['grating'].setOpacity(0.2)
                    
                if thisMod == 'visual' or thisTrial['target'] == 0: # Normal trailing sound played on visual blocks and in non-target trials
                    trailing_sound.play()               
                else: 
                    wn_freqs = st.white_noise(thisTrial['a_trailing'], stim['trailing_frames']) # Function that generates noise around the tone               
                
                if (thisTrial['catch'] == 1 and catch_test == 1): basic_stim["fixation_point"].color = [1,-1,-1] 
                
                event.clearEvents() # Key presses are to be registered from here                
                for frame in range(stim['trailing_frames']):
                    if frame == 0: timer.reset(0) # Reset timer with first frame for both catch and no catch
                    if thisTrial['target'] == 1 and thisMod == 'auditory':
                        trailing_sound = Sound(wn_freqs[frame], sampleRate=44100, secs=1/monitor['Hz'], stereo=True ,loops=0, volume=0.2)
                        trailing_sound.play()
                     
                    basic_stim['stim_contour'].draw()
                    basic_stim['grating'].draw()
                    basic_stim["fixation_point"].draw() 
                    test_keys.draw()
                    reminder.draw()
                    win.flip()  
                                                        
                    if (thisTrial['catch'] == 1 and catch_test == 1): # in catch trials move to next trial (only) when spacebar is pressed
                        keys = event.getKeys(['space'])                     
                        if len(keys) > 0:
                            thisResp = keys[0]
                            trailing_sound.stop()
                            basic_stim["fixation_point"].color = [1,1,1] # Reset color to white if they respond in time
                            RT = timer.getTime()
                            break
                    
              
                    else: # In no catch trials advance when response is given
                        keys = event.getKeys(['z', 'm'])                     
                        if len(keys) > 0:
                            thisKey = keys[0]
                            trailing_sound.stop() # If end presentation on response
                            thisResp, fix_color = rsp.test_feedback(win, thisTrial, thisKey, this_respmap, basic_stim["fixation_point"])
                            basic_stim["fixation_point"].color = fix_color
                            RT = timer.getTime()
                            break # If end presentation on response
###############################################################################
                
            # After each trial append variables to this list
            vars_stored.append([subject_info["Nombre"], subject_info["Edad"], subject_info["Género"], subject_info["Mano dominante"], phase, block_n, thisMod, trials.thisN,
                                thisTrial['v_expect'],thisTrial['v_leading'],thisTrial['v_trailing'],thisTrial['a_expect'],thisTrial['a_leading'],thisTrial['a_trailing'], thisTrial['catch'], thisResp, RT])# saving conditions here
                               
        block_n += 1 # Updating block count at the end of each block
        if phase == 0: # At the end of learning blocks, calculate accucaracy to show on screen
            block_results = vars_stored[-len(these_trials):] # Slicing trials pertaining to this block
            block_df = DataFrame(block_results, columns = header) # df them
            this_accuracy = rsp.block_accuracy(block_df, thisMod)
            instr.show_accuracy(win, this_accuracy)

#============================= EXPERIMENT ENDS ================================            
            
results = DataFrame(vars_stored, columns = header)

results.to_csv("behav_analyses/data/" + subject_info["Nombre"] + ".csv", index = False)
        
win.close()
core.quit()
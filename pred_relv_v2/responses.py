# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 09:43:42 2021

@author: MARC SABIO
"""

from psychopy import visual, event, gui


def subject_info(): # loading staircase subject data
    
    info = {'Nombre':'', 
            'Edad': '', 
            'Mano dominante': ['izquierda', 'derecha'],
            'Género': ['Mujer', 'Hombre', 'Otro']}
    
    dictDlg = gui.DlgFromDict(dictionary=info,
            title='TestExperiment', fixed=['ExpVersion'])
    if dictDlg.OK:
        print(info)
    else:
        print('User Cancelled')
    
    return info
    
    
def learning_Response(win, thisTrial, this_respmap):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 40
    inst.height = 1
    if this_respmap == 0: inst.text = "z = frecuente          espacio = catch          m = raro"
    else: inst.text = "z = raro         espacio = catch        m = frecuente"
    inst.draw()
    win.flip()          
    allKeys=event.waitKeys(keyList = ["z", "m", "space"])
    if this_respmap == 0: 
        for thisKey in allKeys:
            if thisKey=='z': thisResp = "familiar"
            elif thisKey == 'space': thisResp = "catch"
            else: thisResp = "unfamiliar"
    else:
        for thisKey in allKeys:
            if thisKey=='z': thisResp = "unfamiliar"
            elif thisKey == 'space': thisResp = "catch"
            else: thisResp = "familiar"
    return thisResp


def test_feedback(win, thisTrial, thisKey, this_respmap, fixation):
    if this_respmap == 0: 

        if thisKey=='z': 
            thisResp = "distorsionado"
            fix_color = [-1,1,-1] if thisTrial['target'] == 1 else [1,-1,-1]
            fix_color = [1,-1,-1] if thisTrial['target'] == 0 else [-1,1,-1]

        else: 
            thisResp = "normal"
            fix_color = [1,-1,-1] if thisTrial['target'] == 1 else [-1,1,-1]
            fix_color = [-1,1,-1] if thisTrial['target'] == 0 else [1,-1,-1]
            
    else:

        if thisKey=='z': 
            thisResp = "normal"
            fix_color = [1,-1,-1] if thisTrial['target'] == 1 else [-1,1,-1]
            fix_color = [-1,1,-1] if thisTrial['target'] == 0 else [1,-1,-1]
        else: 
            thisResp = "distorsionado"
            fix_color = [-1,1,-1] if thisTrial['target'] == 1 else [1,-1,-1]
            fix_color = [1,-1,-1] if thisTrial['target'] == 0 else [-1,1,-1]
 
    return thisResp, fix_color

def block_accuracy(df, modality):
    if modality == "visual":
        hits = len(df[(df.iloc[:,8] == "EXP") & (df.iloc[:,15] == "familiar")]) + \
               len(df[(df.iloc[:,8] == "VP") & (df.iloc[:,15] == "unfamiliar")]) + \
               len(df[(df.iloc[:,8] == "N") & (df.iloc[:,15] == "unfamiliar")]) + \
               len(df[(df.iloc[:,14] == 1) & (df.iloc[:,15] == "catch")])
    else:
        hits = len(df[(df.iloc[:,11] == "EXP") & (df.iloc[:,15] == "familiar")]) + \
               len(df[(df.iloc[:,11] == "VP") & (df.iloc[:,15] == "unfamiliar")]) + \
               len(df[(df.iloc[:,11] == "N") & (df.iloc[:,15] == "unfamiliar")]) + \
               len(df[(df.iloc[:,14] == 1) & (df.iloc[:,15] == "catch")])
                  
    accuracy = str(round(((hits / len(df)) * 100), 2))    
    
    return accuracy
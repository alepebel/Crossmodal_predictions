# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:46:26 2021

@author: MARC SABIO
"""

import numpy as np


def stimlist_neutral(stim_feats, modality, nEXP, nVP, nN, n_leading, n_trailing, n_neutral):
# This functions creates a list of dictionaries containing pairs and type of trial.
# Inputs: stim_feats (pregenerated list of stimulus features that define pairs, e.g.: orientations in the visual pairs)
#         nEXP, nVP, nN (frequencies of presentation of each type of pair. Expected, violations and neutral, respectively)
# (CAUTION: it wouldn't make sense, but if nVP and nN are equal the function won't work properly)**

    leading = stim_feats[0:n_leading] # Leading include neutral
    trailing = stim_feats[n_leading:]
    
    pairs = np.ones([n_trailing, n_trailing]) * nVP # This is a square matrix which size alway equals n_trailing
    np.fill_diagonal(pairs, nEXP) # Filling diagonal with frequency of expected pairs
    trans_mat = np.vstack([pairs, np.ones([n_neutral, n_trailing])*nN]) # Adding neutral rows
    trans_mat = trans_mat.astype(int)
    
    stimList = []
    for i in range(trans_mat.shape[0]): # Iter rows
        for j in range(trans_mat.shape[1]): # Iter cols
            if modality == "v": # Different key names for each modality
                for x in range(trans_mat[i,j]): # Append a number of elements defined by values in trans_mat
    
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "EXP"})
                    elif trans_mat[i,j] == nVP:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "VP"})
                    else: 
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "N"}) 
                        # (CAUTION: it wouldn't make sense, but if nVP and nN are equal the function won't work properly)**
            else:
                for x in range(trans_mat[i,j]):     
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "EXP"})
                    elif trans_mat[i,j] == nVP:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "VP"})
                    else: 
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "N"})
                    
    return stimList


# NO NEUTRAL!
def stimlist_noneutral(stim_feats, modality, nEXP, nVP, n_leading, n_trailing):
# This functions creates a list of dictionaries containing pairs and type of trial.
# Inputs: stim_feats (pregenerated list of stimulus features that define pairs, e.g.: orientations in the visual pairs)
#         nEXP, nVP, nN (frequencies of presentation of each type of pair. Expected, violations and neutral, respectively)
# (CAUTION: it wouldn't make sense, but if nVP and nN are equal the function won't work properly)**

    leading = stim_feats[0:n_leading] 
    trailing = stim_feats[n_leading:]
    
    pairs = np.ones([n_leading, n_trailing]) * nVP # This is a square matrix which size alway equals n_trailing
    np.fill_diagonal(pairs, nEXP) # Filling diagonal with frequency of expected pairs
    trans_mat = pairs.astype(int)
    
    stimList = []
    for i in range(trans_mat.shape[0]): # Iter rows
        for j in range(trans_mat.shape[1]): # Iter cols
            if modality == "v": # Different key names for each modality
                for x in range(trans_mat[i,j]): # Append a number of elements defined by values in trans_mat
    
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "EXP"})
                    else:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "VP"})
            else:
                for x in range(trans_mat[i,j]):     
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "EXP"})
                    else:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "VP"})
                                        
    return stimList

def stimlist_nn_repeat(stim_feats, modality, nEXP, nVP, n_leading):
# This functions creates a list of dictionaries containing pairs and type of trial.
# Inputs: stim_feats (pregenerated list of stimulus features that define pairs, e.g.: orientations in the visual pairs)
#         nEXP, nVP, nN (frequencies of presentation of each type of pair. Expected, violations and neutral, respectively)
# (CAUTION: it wouldn't make sense, but if nVP and nN are equal the function won't work properly)**

    leading = stim_feats # Leading include neutral
    trailing = np.roll(stim_feats, 1)
    
    pairs = np.ones([n_leading, n_leading]) * nVP # This is a square matrix which size alway equals n_trailing
    np.fill_diagonal(pairs, nEXP) # Filling diagonal with frequency of expected pairs
    trans_mat = pairs.astype(int)
    
    stimList = []
    for i in range(trans_mat.shape[0]): # Iter rows
        for j in range(trans_mat.shape[1]): # Iter cols
            if modality == "v": # Different key names for each modality
                for x in range(trans_mat[i,j]): # Append a number of elements defined by values in trans_mat
    
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "EXP"})
                    else:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "VP"})
            else:
                for x in range(trans_mat[i,j]):     
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "EXP"})
                    else:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "VP"})
                                        
    return stimList

def stimlist_reduced(modality, nEXP, nVP, n_leading):
    if modality == 'v':
        card_obl = [0,1]
        np.random.shuffle(card_obl)
        leading = [[0,90],[45,135]][card_obl[0]]
        trailing = [[0,90],[45,135]][card_obl[1]]
        np.random.shuffle(leading)
        
    if modality == 'a':
        freqs = [200, 600, 1000, 1400]
        firstpair = np.random.choice(freqs,2, replace = False)
        leading = [firstpair[0]]
        trailing = [firstpair[1]]
        if leading[0] > trailing[0]: # first pair is descending
            leading.append(min([f for f in freqs if f not in (leading + trailing)]))
            trailing.append(freqs[freqs != (leading + trailing)])
        else: # first pair is ascending
            leading.append(max([f for f in freqs if f not in (leading + trailing)]))
            trailing.append(freqs[freqs != (leading + trailing)])

            
    pairs = np.ones([n_leading, n_leading]) * nVP # This is a square matrix which size alway equals n_trailing
    np.fill_diagonal(pairs, nEXP) # Filling diagonal with frequency of expected pairs
    trans_mat = pairs.astype(int)

    stimList = []
    for i in range(trans_mat.shape[0]): # Iter rows
        for j in range(trans_mat.shape[1]): # Iter cols
            if modality == "v": # Different key names for each modality
                for x in range(trans_mat[i,j]): # Append a number of elements defined by values in trans_mat
    
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "EXP"})
                    else:
                        stimList.append({"v_leading":leading[i], "v_trailing":trailing[j], "v_expect": "VP"})
            else:
                for x in range(trans_mat[i,j]):     
                    if trans_mat[i,j] == nEXP:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "EXP"})
                    else:
                        stimList.append({"a_leading":leading[i], "a_trailing":trailing[j], "a_expect": "VP"})
                                        
    return stimList   
        


def rand_conditions(vstimlist, astimlist):
# This function psuedorandomizes the order of the pre-generated stimuli pairs of both modalities.
# It makes sure that violations from both modalities never occur at the same trials
    # generating catch trials and target trials
    catch_ids = np.hstack([np.ones(round(len(vstimlist)*0.1)), np.zeros(round(len(vstimlist)*0.9))]) # 1 = catch/ 10% catch
    target_ids = np.hstack([np.ones(round(len(vstimlist)*0.5)), np.zeros(round(len(vstimlist)*0.5))]) # 1 = target/ 50% target
    catch_trials = []
    target_trials = []
    for i in range(len(vstimlist)):
        catch_trials.append({"catch":catch_ids[i]})
        target_trials.append({"target": target_ids[i]})
    np.random.shuffle(catch_trials)
    np.random.shuffle(target_trials)
    
    # input randomly shuffled visual condition trials, to avoid geeting violations of both modalities together
    # getting trial indices where a visual violation is assigned
    np.random.shuffle(vstimlist) # Shuffle conditions order
    np.random.shuffle(astimlist)
    
    #Finding trials where there are no visual expectation violation
    nonVP_inds = [item[0] for item in list(enumerate(vstimlist)) if item[1]["v_expect"] != "VP"] 
    np.random.shuffle(nonVP_inds) #Shuffling list of non violation indicies
    
    # Prealocating output vector of auditory pairs
    A_rand = list(np.zeros(len(astimlist)))
    
    # Now let's list auditory violation pairs...
    astim_VP = [item for item in astimlist if item["a_expect"] == "VP"]
    # And locate them in the non visual violation indices of the output auditory pair vector
    for i in range(len(astim_VP)):
        A_rand[nonVP_inds[i]] = astim_VP[i] 
        
    # Now we need to fill the empty indices with the non-violation auditory pairs
    # For that we first find the empty indices of the output vector...
    rest_inds = [item[0] for item in list(enumerate(A_rand)) if item[1] == 0]
    # list the remaining auditory non-violation pairs...
    astim_nonVP = [item for item in astimlist if item["a_expect"] != "VP"]
    # And locate them in the empty indices
    for i in range(len(astim_nonVP)):
        A_rand[rest_inds[i]] = astim_nonVP[i]
    
    # And finally merge the dictionaries together, so that each entry contains all the info necessary for a trial
    out = []
    for d in range(len(A_rand)):
        out.append({**vstimlist[d], **A_rand[d], **catch_trials[d], **target_trials[d]})
    
    return out

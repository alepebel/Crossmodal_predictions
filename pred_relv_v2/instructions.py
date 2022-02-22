# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:58:34 2021

@author: MARC SABIO
"""

from psychopy import visual, event, core
from psychopy.sound import Sound
import numpy as np

# Experiment instructions


def main_instructions(win, grating, fixation, eye, speaker):
# Instrucciones generales del experimento       
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.text = "¡Bienvenid@ a este experimento! Durante la sesión te vamos a presentar pares de estímulos sobre los cuáles te preguntaremos algo.\
    Después de cada respuesta, se te presentará otro par de estímulos distinto. Usaremos dos tipos de de estímulo: visuales y auditivos." 
    

    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.wrapWidth = 25
    nextt.height = 0.9
    nextt.color = 'black'
    nextt.text = "Pulsa spacio para continuar"
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])
    
    inst.text = "En cada bloque te pediremos que atiendas a unos u otros.\
    Dicho de otro modo, si te pedimos que atiendas a los estímulos visuales, tendrás que ignorar a los auditivos." 
    inst.draw()
    nextt.draw()
    eye.draw()
    speaker.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])
    
    inst.text = "Los estímulos visuales consisten en enrejados con distintas orientaciones, como el que ves arriba. Primero se te presentará uno, y luego otro.\
    A la vez que se presente el primer enrejado, escucharás un suave tono a través de los auriculares. El segundo tono se reproducirá junto al segundo enrejado.\
    Cuando pulses espacio escucharás un tono como los del experimento."
    inst.setPos([0,-2])
    nextt.setPos([0,-8])
    grating.draw()
    fixation.draw()
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])
    sample_sound = Sound(415, sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
    sample_sound.play()
    core.wait(1)
    
    
    return

# PHASE START MESSAGES
# Learning instructions
def learning_starts(win, grating, fixation, red):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Durante esta primera fase tendrás que intentar aprender cuáles son las parejas correctas. Algunas van a aparecer con mayor frecuencia que las demás.\
                Tras la presentación del segundo estímulo, tu tarea consistirá en indicar si los dos estímulos que has percibido son una pareja frecuente o infrecuente."                 
    nextt.text = "Pulsa espacio para continuar"

    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])
    
    inst.text = "Lógicamente, al principio te costará distinguir qué parejas son nuevas y cuáles no. Pero a la larga ciertas parejas te resultarán familiares y acertarás con mayor frecuencia.\
                Recuerda que en cada bloque te vamos a indicar en qué parejas te tienes que fijar (visuales o auditivas). Las que en un momento dado no tengas que atender no te proporcionarán ningua información útil."
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])
    
    inst.text = "Por último, te pedimos que en todo momento fijes la mirada en el punto central de color blanco, incluso cuando estés atendiendo a las parejas auditivas.\
                Esto es importante ya que en ciertos momentos del experimento, cuando se presente el segundo estímulo, el punto de fijación se pondrá de color rojo.\
                Cuando esto ocurra deberás indicarlo en la pantalla de respuesta, sin tener que responder a la pregunta de si la pareja era frecuente o rara."
    nextt.text = "Pulsa espacio para realizar un par de ejemplos"
    inst.wrapWidth = 35
    inst.setPos([0,12])
    nextt.setPos([0,-10])
    
    
    for i in range(1000):
        keys = event.getKeys(['space'])
        if len(keys) > 0: break
        for frame in range(60):
            inst.draw()
            nextt.draw()
            grating.draw()
            fixation.draw()
            win.flip()
            if len(keys) > 0: break
        for frame in range(30):
            inst.draw()
            nextt.draw()
            grating.draw()
            red.draw()
            win.flip()
            if len(keys) > 0: break
        
# Learning phase training        
def training_learn(win, basic_stim, stim):
    for thisTrial in range(2):        
        thisResp = None
        leading_ori = np.random.choice([0,  30,  60])
        trailing_ori = np.random.choice([90,  120,  150])
        leading_sound = Sound(np.random.choice([200,  440,  680]), sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
        trailing_sound = Sound(np.random.choice([920, 1160, 1400]), sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
        basic_stim['grating'].setOpacity(0.5)
        for frame in range(stim['fixation_pre']):
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw() 
            win.flip()
        
        basic_stim['grating'].ori = leading_ori  #updating leading grating ori
        leading_sound.play()
        for frame in range(stim['leading_frames']):       
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw()
            basic_stim['grating'].draw()
            win.flip()
                
        for frame in range(stim['isi_frames']): 
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw()
            win.flip()

        basic_stim['grating'].ori = trailing_ori  #updating trailing grating ori
        trailing_sound.play() 
        event.clearEvents() # Key presses are to be registered from here      
        for frame in range(stim['trailing_frames']):
            basic_stim['stim_contour'].draw()
            basic_stim['grating'].draw()
            basic_stim["fixation_point"].draw()
            win.flip() 

        inst = visual.TextStim(win, pos = [0,0])
        inst.wrapWidth = 40
        inst.height = 1
        inst.text = "z = frecuente          espacio = catch          m = raro"
        inst.draw()
        win.flip()          
        allKeys=event.waitKeys(keyList = ["z", "m", "space"])        



# Test phase training
def training_test(win, basic_stim, stim, monitor):

    test_keys = visual.TextStim(win, pos = [0,-8])
    test_keys.wrapWidth = 40
    test_keys.height = 1
    test_keys.text = "z = distorsionado            m = normal"
    for thisTrial in range(2):        
        thisResp = None
        leading_ori = np.random.choice([0,  30,  60])
        trailing_ori = np.random.choice([90,  120,  150])
        leading_sound = Sound(np.random.choice([200,  440,  680]), sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
        trailing_freq = np.random.choice([920, 1160, 1400])
        trailing_sound = Sound(trailing_freq, sampleRate=44100, secs=0.5, stereo=True ,loops=0, volume=0.2)
        basic_stim['grating'].setOpacity(0.5)
        for frame in range(stim['fixation_pre']):
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw() 
            win.flip()
        
        basic_stim["fixation_point"].color = [1,1,1]
        basic_stim['grating'].ori = leading_ori  #updating leading grating ori
        leading_sound.play()
        for frame in range(stim['leading_frames']):       
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw()
            basic_stim['grating'].draw()
            win.flip()
            
        for frame in range(stim['isi_frames']): 
            basic_stim["fixation_point"].draw()
            basic_stim['stim_contour'].draw()
            win.flip()
                
        basic_stim['grating'].ori = trailing_ori  #updating trailing grating ori
        if thisTrial == 0: #First we will show a visual target
            basic_stim['grating'].setOpacity(0.2)     
            trailing_sound.play()
        else: # and then an auditory target
            basic_stim['grating'].setOpacity(0.7)
            wn_freqs = np.random.normal(trailing_freq, 30, stim['trailing_frames'])
                
        event.clearEvents() # Key presses are to be registered from here                
        for frame in range(stim['trailing_frames']):
            if thisTrial == 1:
                trailing_sound = Sound(wn_freqs[frame], sampleRate=44100, secs=1/monitor['Hz'], stereo=True ,loops=0, volume=0.2)
                trailing_sound.play()
                     
            basic_stim['stim_contour'].draw()
            basic_stim['grating'].draw()
            basic_stim["fixation_point"].draw() 
            test_keys.draw()                
            win.flip()  
            keys = event.getKeys(['z', 'm'])                     
            if len(keys) > 0:
                thisKey = keys[0]
                trailing_sound.stop() # If end presentation on response
                if thisKey == "z": fix_color = [-1,1,-1]
                if thisKey == "m": fix_color = [1,-1,-1]
                basic_stim["fixation_point"].color = fix_color
                break    
    
    
    
def test_starts(win):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Durante esta fase final van a ir apareciendo los mismos pares de estímulos que ya conoces. Pero ahora ya no te tienes que preocupar de si la pareja es correcta o no.\
                Tu tarea ahora será indicar si el segundo estímulo está distorsionado con respecto a lo habitual. Igual que antes, deberás atender a los visuales o a los auditivos.\
                Sólo los estímulos a los que estés atendiendo en ese momento podrán aparecer distorsionados."
    nextt.text = "Pulsa espacio para continuar"
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])
    
    inst.text = "Aquí valoraremos tu capacidad de reacción. Tendrás poco tiempo para decidir si el estímulo presenta o no la distorsión. En todo momento tendrás una indicación\
                en pantalla sobre qué botón corresponde a cada opción (distorsionado o normal). Cuando respondas verás que el color del punto central cambia.\
                Si se pone verde es que has elegido la opción correcta, y rojo la incorrecta. Si permanece de color blanco significa que no has respondido a tiempo."
                
    nextt.text = "Pulsa espacio para realizar un par de ejemplos"
    
    
# BLOCK START MESSAGES

def learning_visual(win):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Aprende los pares visuales. En la pantalla de respuesta se te indicará con qué teclas responder. ¡Recuerda: fija la mirada en el punto central! "
    nextt.text = "Cuando estes listo/a, pulsa espacio para comenzar "
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])


def learning_auditory(win):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Aprende los pares auditivos. En la pantalla de respuesta se te indicará con qué teclas responder. ¡Recuerda: fija la mirada en el punto central! "
    nextt.text = "Cuando estes listo/a, pulsa espacio para comenzar "
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])

def test_visual(win):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Responde a los estímulos visuales. Coloca los dedos sobre botones de respuesta"
    nextt.text = "Cuando estes listo/a, pulsa espacio para comenzar "
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])

def test_auditory(win):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 0.9
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "Responde a los estímulos auditivos. Coloca los dedos sobre botones de respuesta"
    nextt.text = "Cuando estes listo/a, pulsa espacio para comenzar "
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])

def show_accuracy(win, acc):
    inst = visual.TextStim(win, pos = [0,0])
    inst.wrapWidth = 25
    inst.height = 1
    nextt = visual.TextStim(win, pos = [0,-6])
    nextt.height = 0.7
    nextt.color = "black"
    inst.text = "En este bloque has acertado un " + acc + "% de las parejas"
    nextt.text = "Pulsa espacio para empezar el siguiente bloque "
    inst.draw()
    nextt.draw()
    win.flip()
    event.waitKeys( keyList=['space'])

                

 
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 08:47:42 2025

@author: H0sseini
"""
import json
from video_processing import VideoProcessor
from audio_processing import AudioProcessor
from frame_alignment import FrameTextAligner
from narrative_generator import NarrativeGenerator
from utils import load_defaults

 
    
def modify_inputs(inputs):
    
    ''''The inputs are in this order:
        Audio_inputs
        Video_inputs
        frame_inputs
        Narrative_inputs
        '''
    
    default_inputs = load_defaults()
    
    for dictionary in inputs:
        for element in dictionary:
            if dictionary[element] is not None:
                default_inputs[element] = dictionary[element]
    
    


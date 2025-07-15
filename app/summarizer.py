# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 08:47:42 2025

@author: H0sseini
"""
import json, os
from video_processing import VideoProcessor
from audio_processing import AudioProcessor
from frame_alignment import FrameTextAligner
from narrative_generator import NarrativeGenerator
from text_summarizer import SummarizationTool
from utils import load_defaults, write_inputs

 
    
def modify_inputs(myInputs, path='./settings/'):
    
    ''''The inputs are in this order:
        Audio_inputs
        Video_inputs
        frame_inputs
        Narrative_inputs
        '''
    
    inputs = load_defaults()
    
    for dictionary in myInputs:
        for element in dictionary:
            if dictionary[element] is not None:
                inputs[element] = dictionary[element]
                
    write_inputs(inputs[0], inputs[1], inputs[2], inputs[3], path)
    
def restore_defaults(restore_path="./settings/defaults/", path="./settings/"):
     try:
        inputs = load_defaults(restore_path)
        write_inputs(inputs[0], inputs[1], inputs[2], inputs[3], path)
     except Exception as e:
        print(f"{e} error: cannot restore defaults.")

def summarize_video(mode="medium",summary_type="abstractive", path='./settings/'):
    [audio_settings, video_settings, frame_settings, narrative_settings] = load_defaults(path)
    myAudio = AudioProcessor(**audio_settings)
    myVideo = VideoProcessor(**video_settings)
    myFrame = FrameTextAligner(**frame_settings)
    
    
    text, timining = myAudio.transcribe_audio()
    myVideo.extract_frames()
    myFrame.align_frames_with_text()
    myText = SummarizationTool(model_path="./models/bart-large-cnn")
    myNarrative = NarrativeGenerator(**narrative_settings)
    text = myNarrative.load_narrative_text()
    results = myText.summarize(text, mode, summary_type)
    print("Deleting temporary files ...")
    for files in os.listdir(video_settings["video_path"]):
        os.remove(os.path.join(video_settings["video_path"], files))
    for files in os.listdir(audio_settings["audio_path"]):
            os.remove(os.path.join(audio_settings["audio_path"], files))
    for files in os.listdir(audio_settings["text_path"]):
            os.remove(os.path.join(audio_settings["text_path"], files))
    for files in os.listdir(frame_settings["frame_folder"]):
            os.remove(os.path.join(frame_settings["frame_folder"], files))
    return results
    
    
    
    


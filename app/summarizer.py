# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 08:47:42 2025

@author: H0sseini
"""
import json, os, re
from app.video_processing import VideoProcessor
from app.audio_processing import AudioProcessor
from app.frame_alignment import FrameTextAligner
from app.narrative_generator import NarrativeGenerator
from app.text_summarizer import SummarizationTool
from app.utils import load_defaults, write_inputs_from_combined

 
    
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
                
    write_inputs_from_combined(inputs[0], inputs[1], inputs[2], inputs[3], path)
    
def restore_defaults(restore_path="./settings/defaults/", path="./settings/"):
     try:
        inputs = load_defaults(restore_path)
        write_inputs_from_combined(inputs[0], inputs[1], inputs[2], inputs[3], path)
     except Exception as e:
        print(f"{e} error: cannot restore defaults.")

def summarize_video(mode="detailed",summary_type="abstractive", path='./app/settings/'):
    [audio_settings, video_settings, frame_settings, narrative_settings] = load_defaults(path)
    myAudio = AudioProcessor(**audio_settings)
    myVideo = VideoProcessor(**video_settings)
    myFrame = FrameTextAligner(**frame_settings)
    
    
    text, timining = myAudio.transcribe_audio()
    myVideo.extract_frames()
    myFrame.align_frames_with_text()
    myText = SummarizationTool(model_path="./app/models/bart-large-cnn")
    myNarrative = NarrativeGenerator(**narrative_settings)
    text = myNarrative.load_narrative_text()
    summary_mode = myNarrative.summary_mode if myNarrative.summary_mode is not None else mode
    print(f"📓 summary mode selected for the text: {summary_mode}. Summarizing ...")
    
   
    # creating full_text
    matches = re.findall(r'\(\s*(.*?)\s*\)', text)

    # Remove consecutive duplicates
    unique_lines = []
    prev = None
    for line in matches:
        if line != prev:
            unique_lines.append(line)
            prev = line

    # Join all texts
    full_text = " ".join(unique_lines)
    summary = myText.summarize(full_text, summary_mode, summary_type)
    print("👉🏻🗑️ Deleting temporary files ...")
    for files in os.listdir("./app/temp/video"):
        os.remove(os.path.join("./app/temp/video", files))
    for files in os.listdir("./app/temp/audio"):
            os.remove(os.path.join("./app/temp/audio", files))
    for files in os.listdir("./app/temp/frames"):
            os.remove(os.path.join("./app/temp/frames", files))
    for files in os.listdir("./app/temp/transcripts"):
            os.remove(os.path.join("./app/temp/transcripts", files))
    return full_text, summary

def reading_inputs(path="./app/settings/"):
    [audio_settings, video_settings, frame_settings, narrative_settings] = load_defaults(path)
    
    
    return
    
    


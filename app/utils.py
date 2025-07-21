import os
import json

def ensure_model(path, hf_id, cls, **kwargs):
    if not os.path.exists(path):
        print(f"Downloading {hf_id} to {path}")
        obj = cls.from_pretrained(hf_id, **kwargs)
        obj.save_pretrained(path)
    else:
        print(f"Using cached model at {path} for {hf_id}")
        obj = cls.from_pretrained(path, **kwargs)
    return obj

def load_defaults(path='./settings/defaults/'):
    
    with open(os.path.join(path,'AudioInputs.json')) as file:
        AudioInputs = json.load(file)
    with open(os.path.join(path,'VideoInputs.json')) as file:
        VideoInputs = json.load(file)
    with open(os.path.join(path,'FrameAlignInputs.json')) as file:
        FrameAlignInputs = json.load(file)
    with open(os.path.join(path,'NarrativeInputs.json')) as file:
        NarrativeInputs = json.load(file)
    
    '''   
    AudioInputs = {
        "model_dir": "./models/whisper_models",
        "model_size": "base",
        "video_path": "./temp/video",
        "video_name": "input_video.mp4",
        "audio_path": "./temp/audio",
        "audio_name": "extracted_audio.wav",
        "text_path": "./temp/transcripts",
        "text_name": "full_text.txt",
        "timing_name": "timed_transcript.txt"
    }
    
    
    VideoInputs = {
        "frame_folder":"./temp/frames",
        "video_path": "./temp/video", 
        "video_name": "input_video.mp4",
        "interval_sec": 5, 
        "scene_stability_sec": 15,
        "diff_threshold": 30.0
    }
    
    FrameAlignInputs = {
        "clip_model_id": "openai/clip-vit-base-patch32",
        "clip_model_path": "./models/clip-vit-base-patch32",
        "clip_proc_path": "./models/clip-vit-base-patch32-processor",
        "blip_model_id": "Salesforce/blip2-flan-t5-xl",
        "blip_model_path": "./models/blip2-flan-t5-xl-model",
        "blip_proc_path": "./models/blip2-flan-t5-xl-processor",
        "transcript_path": "./temp/transcripts/timed_transcript.txt",
        "frame_folder": "./temp/frames",
        "output_path": "./temp/transcripts/frame_text_alignment.txt"
    }
    
    NarrativeInputs = {
        "confidence": 0.26,
        "frames_dir": "./temp/frames",
        "alignment_file": "./temp/transcripts/frame_text_alignment.txt",
        "output_file": "./temp/transcripts/narrative.txt",
        "blip_model_path": "./models/blip2-flan-t5-xl-model",
        "blip_processor_path": "./models/blip2-flan-t5-xl-processor",
        "model_id": "Salesforce/blip2-flan-t5-xl",
        "fps": 1,
        "json_path": "./temp/transcripts/frame_narrative_data.json"    
    }
    '''
    
    
   
    return [AudioInputs, VideoInputs, FrameAlignInputs, NarrativeInputs]

def write_inputs(audio, video, frame, narrative, path='./app/settings/'):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(f'{e} error: cannot create the folder: {path}')
    
       
    with open(os.path.join(path,'AudioInputs.json'), 'w') as file:
        json.dump(audio, file)
    with open(os.path.join(path,'VideoInputs.json'), 'w') as file:
        json.dump(video, file)
    with open(os.path.join(path,'FrameAlignInputs.json'), 'w') as file:
        json.dump(frame, file)
    with open(os.path.join(path,'NarrativeInputs.json'), 'w') as file:
        json.dump(narrative, file)
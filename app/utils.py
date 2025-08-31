import os
import json
from fastapi import Request
from fastapi.responses import JSONResponse
import shutil

def ensure_model(path, hf_id, cls, **kwargs):
    if not os.path.exists(path):
        print(f"Downloading {hf_id} to {path}")
        obj = cls.from_pretrained(hf_id, **kwargs)
        obj.save_pretrained(path)
    else:
        print(f"Using cached model at {path} for {hf_id}")
        obj = cls.from_pretrained(path, **kwargs)
    return obj

def load_defaults(path='./app/settings/defaults/'):
    
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
        "model_dir": "whisper_models",
        "model_size": "base"
    }
    
    
    VideoInputs = {
        
        "interval_sec": 5, 
        "scene_stability_sec": 15,
        "diff_threshold": 30.0
    }
    
    FrameAlignInputs = {
        "clip_model_id": "openai/clip-vit-base-patch32",
        "blip_model_id": "Salesforce/blip2-flan-t5-xl"
    }
    
    NarrativeInputs = {
        "confidence": 0.26,
        "model_id": "Salesforce/blip2-flan-t5-xl",
        "fps": 1,
        "summary_mode": "medium"
    }
    '''
    
    
   
    return [AudioInputs, VideoInputs, FrameAlignInputs, NarrativeInputs]

def restore_defaults(path: str = './app/settings/', defaults_path: str = './app/settings/defaults/'):
    try:
        # Ensure settings folder exists
        if not os.path.exists(path):
            os.makedirs(path)

        # Copy each default JSON into the settings folder
        for filename in os.listdir(defaults_path):
            src_file = os.path.join(defaults_path, filename)
            dst_file = os.path.join(path, filename)

            if os.path.isfile(src_file):
                shutil.copyfile(src_file, dst_file)

        return JSONResponse(content={"status": "success", "message": "Defaults restored successfully"}, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

def write_inputs_from_combined(settings: dict, 
                               path: str = './app/settings/', 
                               defaults_path: str = './app/settings/defaults/'):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": f"Cannot create folder {path}: {e}"},
            status_code=500
        )

    def load_defaults(filename):
        try:
            with open(os.path.join(defaults_path, filename), 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def merge_with_defaults(user_data: dict, default_data: dict):
        merged = default_data.copy()
        for key, value in (user_data or {}).items():
            if value is not None and value != "":
                merged[key] = value
        return merged

    try:
        # Load defaults
        default_audio = load_defaults('AudioInputs.json')
        default_video = load_defaults('VideoInputs.json')
        default_frame = load_defaults('FrameAlignInputs.json')
        default_narrative = load_defaults('NarrativeInputs.json')

        # Merge with user settings
        audio = merge_with_defaults(settings.get("audio"), default_audio)
        video = merge_with_defaults(settings.get("video"), default_video)
        frame = merge_with_defaults(settings.get("frame"), default_frame)
        narrative = merge_with_defaults(settings.get("narrative"), default_narrative)

        # Save merged settings
        with open(os.path.join(path, 'AudioInputs.json'), 'w') as file:
            json.dump(audio, file, indent=4)
        with open(os.path.join(path, 'VideoInputs.json'), 'w') as file:
            json.dump(video, file, indent=4)
        with open(os.path.join(path, 'FrameAlignInputs.json'), 'w') as file:
            json.dump(frame, file, indent=4)
        with open(os.path.join(path, 'NarrativeInputs.json'), 'w') as file:
            json.dump(narrative, file, indent=4)

        return JSONResponse(content={"status": "success"}, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
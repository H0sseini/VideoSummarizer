import os
import json
from fastapi import Request
from fastapi.responses import JSONResponse

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

def write_inputs(settings: dict, path: str = './app/settings/'):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(f'{e} error: cannot create the folder: {path}')
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

    try:
        audio = settings.get("audio", {})
        video = settings.get("video", {})
        frame = settings.get("frame", {})
        narrative = settings.get("narrative", {})

        with open(os.path.join(path, 'AudioInputs.json'), 'w') as file:
            json.dump(audio, file)
        with open(os.path.join(path, 'VideoInputs.json'), 'w') as file:
            json.dump(video, file)
        with open(os.path.join(path, 'FrameAlignInputs.json'), 'w') as file:
            json.dump(frame, file)
        with open(os.path.join(path, 'NarrativeInputs.json'), 'w') as file:
            json.dump(narrative, file)

        return JSONResponse(content={"status": "success"}, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

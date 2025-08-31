# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 09:06:15 2025

@author: Mehdi
"""

from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import  JSONResponse, HTMLResponse 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.summarizer import summarize_video
import os, shutil, json, traceback
from app.utils import load_defaults, write_inputs_from_combined, restore_defaults



app = FastAPI()

templates = Jinja2Templates(directory="frontend/template")
app.mount("/static", StaticFiles(directory="./frontend/template/static"), name="static")

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "full_text": None, "error": None})

@app.post("/summarize", response_class=JSONResponse)
async def summarize(
    request: Request,
    file: UploadFile = File(...),
):
    try:
        video_path = "./app/temp/video/input_video.mp4"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        full_text, summary = summarize_video()

        return JSONResponse({
            "status": "success",
            "summary_text": summary,
            "fullNarrative": full_text
        })
    except Exception as e:
        
        error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return JSONResponse({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
            }, status_code=500)
    
@app.get("/read_settings")
async def read_current_settings():
    try:
        audio, video, frame, narrative = load_defaults("./app/settings/")
        settings={
            "audio": audio,
            "video": video,
            "frame": frame,
            "narrative": narrative
            }
        return settings
    
    except Exception as e:
       error_message = f"❌ Failed to read settings: {str(e)}"
       print(error_message)
       print(traceback.format_exc())  # Show full traceback
       return JSONResponse(
            content={"error": f"Failed to read settings: {str(e)}"},
            status_code=500
        ) 

@app.post("/write_inputs")
async def write_inputs_endpoint(request: Request):
    try:
        settings = await request.json()
        return write_inputs_from_combined(settings)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
    
@app.post("/restore_defaults")
async def restore_defaults_route():
    return restore_defaults()

@app.get("/read_settings")
async def read_settings_route():
    print("kir")
    settings_path = "./app/settings/"
    files = {
        "audio": "AudioInputs.json",
        "video": "VideoInputs.json",
        "frame": "FrameAlignInputs.json",
        "narrative": "NarrativeInputs.json"
    }

    settings_data = {}
    try:
        for key, filename in files.items():
            file_path = os.path.join(settings_path, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    settings_data[key] = json.load(f)
                    print(settings_data)
            else:
                settings_data[key] = {}  # empty if not found
        return {"status": "success", "settings": settings_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading settings: {str(e)}")
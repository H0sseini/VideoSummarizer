# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 09:06:15 2025

@author: Mehdi
"""

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import  JSONResponse, HTMLResponse 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.summarizer import summarize_video
import os
import shutil
from app.utils import load_defaults
import traceback

app = FastAPI()

templates = Jinja2Templates(directory="frontend/template")
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

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

        full_text, summary = summarize_video(path='./app/settings/')

        return JSONResponse({
            "status": "success",
            "summary": summary,
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

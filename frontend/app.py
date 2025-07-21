# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 09:06:15 2025

@author: Mehdi
"""

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.summarizer import summarize_video
import os
import shutil

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

@app.post("/", response_class=HTMLResponse)
async def summarize(
    request: Request,
    mode: str = Form("medium"),
    summary_type: str = Form("abstractive"),
    text_input: str = Form(None),
    file: UploadFile = File(...)
):
    try:
        video_path = "./app/temp/video/input_video.mp4"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        full_text, result = summarize_video(mode=mode, summary_type=summary_type, path='./app/settings/')

        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "full_text": full_text,
            "error": None
        })
    except Exception as e:
        import traceback
        error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": None,
            "full_text": None,
            "error": str(e)
        })

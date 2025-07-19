# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 09:06:15 2025

@author: Mehdi
"""

from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.summarizer import summarize_video, modify_inputs, restore_defaults
import os

app = FastAPI()


templates = Jinja2Templates(directory="./frontend/templates")
app.mount("/static", StaticFiles(directory="./frontend/templates/static"), name="static")

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
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "error": None})
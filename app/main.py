# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:16:34 2025

@author: H0sseini
"""
import os
import tempfile
from moviepy import VideoFileClip
import whisper
import torch

WHISPER_MODEL_DIR = "./models/whisper-base"
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

model = whisper.load_model("base")
save_path = "./models/whisper-base"
os.makedirs(save_path, exist_ok=True)
torch.save({
    "args": model.args,
    "model_state_dict": model.state_dict()
}, os.path.join(save_path, "model.pt"))

class AudioProcessor:
    def __init__(self, model_dir="./models/whisper-base"):
        model_file = os.path.join(model_dir, "model.pt")
        
        # Safe model load
        checkpoint = torch.load(model_file, map_location="cpu", weights_only=False)

        # Instantiate and load Whisper model
        self.model = whisper.Whisper(**checkpoint["args"])
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()  # ensure evaluation mode

    def load_model(self):
        if os.path.exists(self.model_path):
            print(f"🔁 Loading Whisper model from {self.model_path}")
            return torch.load(self.model_path)
        else:
            print(f"🌐 Downloading Whisper model: {self.model_size}")
            model = whisper.load_model(self.model_size)
            os.makedirs(self.model_dir, exist_ok=True)
            torch.save(model, self.model_path)
            return model

    def extract_audio(self, video_path):
        """Extract audio from video and save to a temporary WAV file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(temp_audio.name, codec="pcm_s16le")
            return temp_audio.name

    def transcribe_audio(self, audio_path):
        """Use Whisper model to transcribe audio."""
        result = self.model.transcribe(audio_path)
        return result.get("text", "")

    def transcribe_video(self, video_path):
        """Full pipeline: extract audio, transcribe it, return text."""
        audio_path = self.extract_audio(video_path)
        try:
            transcript = self.transcribe_audio(audio_path)
        finally:
            os.remove(audio_path)  # Clean up temp file
        return transcript


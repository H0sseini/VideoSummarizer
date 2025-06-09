import os
from moviepy import VideoFileClip
import whisper



class AudioProcessor:
    def __init__(self, model_dir="./whisper_models",
                 model_size = "base", path="./input_video.mp4",
                 audio_path = "./extracted_audio.wav", name="input_video.mp4"):
        
            
        self.model_dir = model_dir
        self.model_size = model_size # choose between 'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo'
        self.path = path
        self.audio_path = audio_path
        self.name = name
        
        if os.path.isfile(self.path):
            print("video file exists.")
        else:
            raise Exception(f"video file does not exists in {os.path.abspath("./")}\\{self.name}")
        
        
        
    def extract_audio(self):
        try:
            video = VideoFileClip(self.path)
            audio = video.audio
            audio.write_audiofile(self.audio_path)
        except Exception as e:
            print(f"Error extracting audio: {e}")
            raise Exception("Error in extacting. Aborting.")

    def get_whisper_model(self):
        os.makedirs(self.model_dir, exist_ok=True)
        model_path = os.path.join(self.model_dir, f'{self.model_size}.pt')
        if not os.path.exists(model_path):
            print(f"Model {self.model_size} not found in {self.model_dir}. Downloading...")
        else:
            print(f"Model {self.model_size} found in {self.model_dir}.")
        model = whisper.load_model(self.model_size, download_root=self.model_dir)
        return model

    def transcribe_audio(self):
        model = self.get_whisper_model()
        self.extract_audio()
        result = model.transcribe(self.audio_path)
        self.full_text = result['text']
        self.timing_text = []
        for seg in result['segments']:
            self.timing_text.append(f"[{seg['start']:.2f}s -> {seg['end']:.2f}s] {seg['text']}")
            
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(self.full_text)
        with open("timed_transcript.txt", "w", encoding="utf-8") as f:
            for item in self.timing_text:
                f.write(f"{item}\n")

        return self.full_text, "\n".join(self.timing_text)
    
        
        


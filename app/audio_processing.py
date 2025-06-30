import os
from moviepy import VideoFileClip
import whisper



class AudioProcessor:
    def __init__(self, model_dir="./models/whisper_models",
                 model_size = "base", video_path="./temp/video",video_name="input_video.mp4",
                 audio_path = "./temp/audio", audio_name="extracted_audio.wav", 
                 text_path = "./temp/transcripts",
                 text_name="full_text.txt", timing_name="timed_transcript.txt"):
        
            
        self.model_dir = model_dir
        self.model_size = model_size # choose between 'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo'
        self.video_path = video_path
        self.video_name = video_name
        self.audio_path = audio_path
        self.audio_name = audio_name
        self.text_path = text_path
        self.text_name = text_name
        self.timing_name = timing_name
        
        
        
        if os.path.isfile(os.path.join(self.video_path, self.video_name)):
            print("video file exists.")
            try:
                os.mkdir(self.text_path)
            except FileExistsError:
                print(f"No need to create transcripts folder in {self.text_path}. Already exists")
            except Exception as e:
                print(f"Error {e} creating audio folder in {self.text_path}.")
            
            try:
                os.mkdir(self.audio_path)
            except FileExistsError:
                print(f"No need to create transcripts folder in {self.audio_path}. Already exists")
            except Exception as e:
                print(f"Error {e} creating audio folder in {self.audio_path}.")
        else:
            raise Exception(f"video file does not exists in {os.path.join(self.video_path, self.video_name)}")
        
        
        
    def extract_audio(self):
        try:
            video = VideoFileClip(os.path.join(self.video_path, self.video_name))
            audio = video.audio
            audio.write_audiofile(os.path.join(self.audio_path, self.audio_name))
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
        result = model.transcribe(os.path.join(self.audio_path, self.audio_name))
        self.full_text = result['text']
        self.timing_text = []
        for seg in result['segments']:
            self.timing_text.append(f"[{seg['start']:.2f}s -> {seg['end']:.2f}s] {seg['text']}")
        #removing old files
        os.remove(os.path.join(self.text_path, self.text_name))
        os.remove(os.path.join(self.text_path, self.timing_name))
        
        with open(os.path.join(self.text_path, self.text_name), "w", encoding="utf-8") as f:
            f.write(self.full_text)
        with open(os.path.join(self.text_path, self.timing_name), "w", encoding="utf-8") as f:
            for item in self.timing_text:
                f.write(f"{item}\n")

        return self.full_text, "\n".join(self.timing_text)
    
        
        


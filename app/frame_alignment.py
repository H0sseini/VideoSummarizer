
import os
from PIL import Image
from tqdm import tqdm
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel, Blip2Processor, Blip2ForConditionalGeneration
from app.utils import ensure_model

class FrameTextAligner:
    def __init__(
        self,
        clip_model_id="openai/clip-vit-base-patch32",
        clip_model_path="./app/models/clip-vit-base-patch32",
        clip_proc_path="./app/models/clip-vit-base-patch32-processor",
        blip_model_id="Salesforce/blip2-flan-t5-xl",
        blip_model_path="./app/models/blip2-flan-t5-xl-model",
        blip_proc_path="./app/models/blip2-flan-t5-xl-processor",
        transcript_path="./app/temp/transcripts/timed_transcript.txt",
        frame_folder="./app/temp/frames",
        output_path="./app/temp/transcripts/frame_text_alignment.txt"
    ):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.clip_model = ensure_model(clip_model_path, clip_model_id, CLIPModel).to(self.device)
        self.clip_processor = ensure_model(clip_proc_path, clip_model_id, CLIPProcessor)

        self.blip_model = ensure_model(blip_model_path, blip_model_id, Blip2ForConditionalGeneration, torch_dtype=self.torch_dtype)
        self.blip_processor = ensure_model(blip_proc_path, blip_model_id, Blip2Processor)

        self.transcript_path = transcript_path
        self.frame_folder = frame_folder
        self.output_path = output_path

    def load_transcript(self):
        with open(self.transcript_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def align_frames_with_text(self):
        print("🔍 Embedding transcript...")
        text_lines = self.load_transcript()
        text_inputs = self.clip_processor(text=text_lines, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(**text_inputs)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        print("🖼️  Processing frames...")
        frame_files = sorted([f for f in os.listdir(self.frame_folder) if f.endswith(".jpg")])
        results = []
        confidence_scores = []
        
        for frame_file in tqdm(frame_files):
            img = Image.open(os.path.join(self.frame_folder, frame_file)).convert("RGB")
            image_input = self.clip_processor(images=img, return_tensors="pt").to(self.device)
        
            with torch.no_grad():
                image_feature = self.clip_model.get_image_features(**image_input)
                image_feature /= image_feature.norm(dim=-1, keepdim=True)
        
            # Similarity & best match
            similarities = cosine_similarity(image_feature.cpu().numpy(), text_features.cpu().numpy())
            best_idx = similarities.argmax()
            best_score = similarities[0][best_idx]
            best_text = text_lines[best_idx]
        
            results.append((frame_file, best_text, best_score))  # include score

        print(f"💾 Saving alignment to {self.output_path}")
        with open(self.output_path, "w", encoding="utf-8") as f:
            for frame, line, score in results:
                f.write(f"{frame} => {line} => {score}\n")

        print("✅ Frame ↔ Transcript alignment completed!")

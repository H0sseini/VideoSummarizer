import os
from PIL import Image
from tqdm import tqdm
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from app.utils import ensure_model
import json


class NarrativeGenerator:
    def __init__(
        self,
        confidence = 0.26,
        model_id="Salesforce/blip2-flan-t5-xl",
        fps = 1,
        summary_mode = "medium"
    ):
        self.confidence = confidence
        self.frames_dir = "./app/temp/frames"
        self.alignment_file = "./app/temp/transcripts/frame_text_alignment.txt"
        self.output_file = "./app/temp/transcripts/narrative.txt"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.fps = fps #frame rate of the video
        self.json_path = "./app/temp/transcripts/frame_narrative_data.json"

        # Load BLIP2 model and processor
        blip_model_loc = model_id.replace(model_id[:model_id.find("/")],
                                                "./app/models")
        blip_model_path = blip_model_loc + "-model"
        blip_processor_path = blip_model_loc + "-processor"
        
        self.processor = ensure_model(blip_processor_path, model_id, Blip2Processor)
        self.model = ensure_model(blip_model_path, model_id, Blip2ForConditionalGeneration, torch_dtype=self.dtype)
        self.model.to(self.device)

        # Load frame ↔ transcript alignment data
        self.frame_text_map = self._load_alignment_file()
        
        self.summary_mode = summary_mode

    def _load_alignment_file(self):
        mapping = {}
        with open(self.alignment_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.count("=>") == 2:
                    frame, text, score = map(str.strip, line.strip().split("=>"))
                    mapping[frame] = {
                        "text": text,
                        "score": float(score)
                    }
        return mapping

    def generate_caption(self, image: Image.Image):
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return caption.strip()

    def generate_narrative(self):
        results = []
        json_data = []
        frame_files = sorted([f for f in os.listdir(self.frames_dir) if f.endswith(".jpg")])
        
        caption_counter = 0
        for frame_file in tqdm(frame_files, desc="🌱 Generating narrative"):
            img_path = os.path.join(self.frames_dir, frame_file)
            image = Image.open(img_path).convert("RGB")

            frame_info = self.frame_text_map.get(frame_file, {})
            aligned_text = frame_info.get("text", "")
            score = frame_info.get("score", 0.0)
            caption_counter += 1
            if (caption_counter % 5 == 0):
                caption = self.generate_caption(image.resize((224, 224)))
            else:
                caption = ""

            narrative_line = f"{frame_file} | {caption}"
            if aligned_text:
                narrative_line += f" ({aligned_text})"

            results.append(narrative_line)
            
            start_time, end_time = self.extract_time_from_frame_name(frame_file)
            json_data.append({
                "frame": frame_file,
                "start_time": start_time,
                "end_time": end_time,
                "frame_caption": caption,
                "aligned_text": aligned_text.split("]")[-1],
                "confidence_score": round(float(score), 4)
            })

        with open(self.output_file, "w", encoding="utf-8") as f:
            for line in results:
                f.write(line + "\n")

        print(f"\n✅ Narrative saved to {self.output_file}")
        # Save to file
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        
        print(f"\n✅ Saved frame/text alignment to {self.json_path}.")        
        
        
        
    
    def extract_time_from_frame_name(self, name):
        
        frame_num = int(name.replace("frame_", "").replace(".jpg", ""))
        start = frame_num / self.fps
        end = (frame_num + 1) / self.fps
        return round(start, 2), round(end, 2)
    
    def load_narrative_text(self, min_confidence=0.26):
        self.generate_narrative()
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        narrative_lines = []
        confidence = self.confidence if self.confidence is not None else min_confidence
        for entry in data:
            score = float(entry.get("confidence_score", 1.0))
            if score < confidence:
                continue  # skip low confidence matches
    
            time_str = f"[{entry['start_time']}s → {entry['end_time']}s]"
            frame_caption = entry.get("frame_caption", "")
            aligned_text = entry.get("aligned_text", "")
    
            combined = f"{time_str} {frame_caption}"
            if aligned_text:
                combined += f" ({aligned_text})"
    
            narrative_lines.append(combined)
    
        return "\n".join(narrative_lines)
    
    
    
    
    
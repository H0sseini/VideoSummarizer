import cv2
import os
import shutil
import numpy as np


class VideoProcessor:
    def __init__(self, frame_folder="./app/temp/frames", video_path = "./app/temp/video", 
                 video_name="input_video.mp4", interval_sec=5, 
                 scene_stability_sec=15, diff_threshold=30.0):
        self.frame_folder = frame_folder
        self.interval_sec = interval_sec
        self.scene_stability_sec = scene_stability_sec
        self.diff_threshold = diff_threshold
        self.video_full_path = os.path.join(video_path, video_name)

        self._prepare_frame_folder()

    def _prepare_frame_folder(self):
        if os.path.exists(self.frame_folder):
            shutil.rmtree(self.frame_folder)
        os.makedirs(self.frame_folder)

    def _frame_difference(self, frame1, frame2):
        # Resize for faster comparison
        frame1_small = cv2.resize(frame1, (160, 90))
        frame2_small = cv2.resize(frame2, (160, 90))
        diff = cv2.absdiff(frame1_small, frame2_small)
        return np.mean(diff)

    def extract_frames(self):
        print("🖼️ extracting frames ...")
        cap = cv2.VideoCapture(self.video_full_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / self.fps

        interval_frames = int(self.interval_sec * self.fps)
        stable_frames = int(self.scene_stability_sec * self.fps)

        last_saved_frame = None
        last_saved_index = -stable_frames  # ensure the first frame is considered
        current_index = 0
        
        #cleaning all previous files
        for filename in os.listdir(self.frame_folder):
            file_path = os.path.join(self.frame_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if current_index % interval_frames == 0:
                save_path = os.path.join(self.frame_folder, f"frame_{current_index}.jpg")
                cv2.imwrite(save_path, frame)
                last_saved_frame = frame
                last_saved_index = current_index

            elif (current_index - last_saved_index) >= stable_frames:
                if last_saved_frame is not None:
                    diff = self._frame_difference(last_saved_frame, frame)
                    if diff < self.diff_threshold:
                        save_path = os.path.join(self.frame_folder, f"frame_{current_index}_stable.jpg")
                        cv2.imwrite(save_path, frame)
                        last_saved_frame = frame
                        last_saved_index = current_index

            current_index += 1

        cap.release()
        print(f"Frames saved in: {self.frame_folder}")

# VideoSummarizer

VideoSummarizer is a tool that generates concise text summaries from videos by combining video and audio processing techniques. It uses advanced algorithms to extract key content, allowing users to quickly grasp the essence of a video without watching it in full. The tool features a user-friendly GUI powered by FastAPI and Uvicorn for easy interaction.

## Features

- **Video and Audio Processing**: Extracts meaningful information from both visual and audio components of a video.
- **Text Summarization**: Produces summaries in three lengths (`short`, `medium`, `detailed`) using abstractive or extractive methods.
- **Web-Based GUI**: Access the summarization tool through an intuitive interface served by Uvicorn.
- **Customizable Output**: Select summary length and type via the GUI or command line.
- **Open Source**: Licensed under the GNU General Public License v3.0, allowing free use, modification, and distribution.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/H0sseini/VideoSummarizer.git
   cd VideoSummarizer
   ```

2. **Install Dependencies**:
   Ensure Python 3.8+ is installed. Install required packages using:
   ```bash
   pip install -r requirements.txt
   ```
   *Note*: Requirements include `fastapi`, `uvicorn`, `torch`, `transformers`, `pymupdf`, `python-docx`, and others. Check `requirements.txt` for the full list.

3. **Download Pre-trained Model (Automatic)**:
   The tool uses the `facebook/bart-large-cnn` model for summarization. Run the following to download it:
   ```bash
   python text_summarizer.py
   ```
   This downloads the model to `./app/models/bart-large-cnn`.
   The tool also uses `whisper-models` for transcribing audio, `clip` model for the alignment of frames with texts, and `blip` model for generation of narratives. 
   There is no need to download these models manually, the app will download necessary models during the first summariztion and stores them in the `./app/models/` folder.
   Warning: You may need to download around 12.5 GB of data during the first usage.

4. **Install NLTK Data**:
   The tool requires NLTK’s `punkt` tokenizer. Install it with:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```
   Again, the app downloads and installs the necessary files and there is no need to use the manual method.

## Usage

### Via GUI (Recommended)
1. **Launch the GUI**:
   Start the FastAPI server with Uvicorn to access the web-based interface:
   ```bash
   uvicorn frontend.app:app --host 0.0.0.0 --port 8000
   ```
   Or, use Python if you didnn't install uvicorn:
   ```bash
   python -m uvicorn frontend.app:app --host 0.0.0.0 --port 8000
   ```
   - The server will run on `http://localhost:8000`.

2. **Access the GUI**:
   Open your browser and navigate to `http://localhost:8000`. The interface allows you to:
   - Upload a video file (e.g., MP4, AVI).
   - View or copy the generated narrative and summary.
   - Change settings of the app.

3. **Interact with the GUI**:
   Follow the on-screen instructions to upload a video, configure settings, and generate summaries.



## Requirements

- Python 3.8 or higher
- Libraries: `fastapi`, `uvicorn`, `torch`, `transformers`, `pymupdf`, `python-docx`, `sumy`, `nltk`, and others (see `requirements.txt`)


## License

This project is licensed under the [GNU General Public License v3.0](LICENSE). You are free to use, modify, and distribute this software, provided you comply with the license terms.



## Troubleshooting

- **GUI Not Loading**: Ensure Uvicorn is running and the correct port (`8000`) is accessible. Check for firewall issues.
- **Summarization Fails**: Verify the video format is supported and the `bart-large-cnn` model is downloaded.
- **Warnings About Input Length**: If you see warnings like `"Your max_length is set to 300, but your input_length is only 3"`, ensure your video contains sufficient audio/text content. Short inputs may produce empty summaries.

## Contact

For issues or suggestions, please open an issue on the [GitHub repository](https://github.com/H0sseini/VideoSummarizer).
# Simple Whisper GUI

A simple graphical user interface for OpenAI's Whisper speech recognition model, with support for English and Italian languages.

## Features

- Easy-to-use interface for audio transcription
- Automatic model recommendation based on system RAM
- Support for multiple audio and video formats
- Multi-language interface (English and Italian)
- Background processing to keep the UI responsive

## Requirements

- Python 3.8 or higher
- FFmpeg installed on your system
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/whisper-gui.git
   cd whisper-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg (if not already installed):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or equivalent for your distribution

## Usage

1. Run the application:
   ```
   python whisper_gui.py
   ```

2. Select your preferred language (English or Italian)
3. Choose a Whisper model (or use the recommended one)
4. Click "Load/Reload Model" to load the selected model
5. Select an audio or video file to transcribe
6. Click "Transcribe" to start the transcription process
7. View the transcription results in the text area

## Models

The application automatically recommends a model based on your system's available RAM:

- **tiny**: Requires ~2GB RAM
- **base**: Requires ~2.5GB RAM
- **small**: Requires ~4GB RAM
- **medium**: Requires ~8GB RAM
- **large**: Requires ~12GB RAM

You can manually select a different model if you prefer.

## License

MIT License - See LICENSE file for details.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) - The underlying speech recognition model
- [Python Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

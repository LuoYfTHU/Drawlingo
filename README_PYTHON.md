# Drawlingo - Python Version

A Python-based desktop application that helps children learn foreign languages through drawing. Draw a sketch, and the app will generate a simple story in both English and German using the Qwen2-VL-2B model, then read it aloud.

## Features

- **Drawing Canvas**: Draw freely using mouse, touch screen, or pen/stylus
- **AI-Powered Analysis**: Uses Qwen2-VL-2B model locally to understand sketches
- **Bilingual Stories**: Generates kindergarten-level stories in English and German
- **Text-to-Speech**: Reads stories aloud in both languages
- **Simple UI**: Clean, child-friendly interface

## Requirements

- **Python 3.8+**
- **PyQt6** (GUI framework)
- **PyTorch** (for Qwen2-VL model)
- **Transformers** (Hugging Face library)
- **~4-6 GB RAM** (model loads in 4-bit quantization)
- **~3-4 GB disk space** (for model download)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The first time you run the app, it will download the Qwen2-VL-2B model (~2GB). This happens automatically.

### 2. Run the Application

```bash
python main.py
```

## Usage

1. **Launch the application**
2. **Draw on the canvas** using your mouse, touch screen, or stylus
3. **Click the arrow button** (→) to analyze your drawing
4. **Wait for the story** to be generated (first run may take longer as the model downloads and loads)
5. **Listen** as the app reads the story in English, then German

## Project Structure

```
Drawlingo/
├── main.py                 # Application entry point
├── MainWindow.py           # Main window UI and logic
├── DrawingCanvas.py        # Drawing canvas widget
├── SketchAnalyzer.py       # Qwen2-VL model integration
├── requirements.txt        # Python dependencies
├── src_backup/            # Backup of original C++ files
└── README_PYTHON.md       # This file
```

## Model Information

The app uses **Qwen2-VL-2B-Instruct**, a 2-billion parameter vision-language model:
- Loads in **4-bit quantization** to reduce RAM usage (~2.5 GB)
- Runs entirely **locally** on your machine
- No internet required after initial model download
- First inference may take 30-60 seconds (model loading)

## Troubleshooting

### Model download fails

- Check your internet connection
- The model is downloaded from Hugging Face - ensure you can access huggingface.co
- You may need to accept the model license on Hugging Face first

### Out of memory errors

- The model uses 4-bit quantization to minimize RAM usage
- Close other applications to free up memory
- Ensure you have at least 4 GB of free RAM

### Text-to-speech not working

- **Windows**: Should work out of the box with SAPI5 voices
- **Linux**: Install speech synthesis:
  ```bash
  sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
  ```
- **macOS**: Should work out of the box with system voices

### Drawing not working

- Ensure your touch screen/stylus drivers are installed
- Try using the mouse as an alternative input method
- Check that the canvas widget is receiving events

## Performance Tips

- **First run**: Model download and loading takes time (2-5 minutes)
- **Subsequent runs**: Model loads faster if kept in memory (~30-60 seconds)
- **GPU support**: If you have a CUDA-compatible GPU, the model will automatically use it for faster inference

## Differences from C++ Version

- **Local processing**: All analysis happens on your machine (no API key needed)
- **Better ML integration**: Native Python support for transformers
- **Easier to extend**: Python ecosystem makes it easier to add features
- **Cross-platform**: Works on Windows, Linux, and macOS

## License

This project is provided as-is for educational and demonstration purposes.

## Notes

- The model requires significant RAM (4-6 GB recommended)
- First model download is ~2GB and happens automatically
- Text-to-speech quality depends on your system's installed voices
- The app runs entirely offline after the initial model download


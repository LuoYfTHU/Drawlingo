# Drawlingo - Sketch-Based Language Learning App

A Qt-based desktop application that helps children learn foreign languages through drawing. Draw a sketch, and the app will generate a simple story in both English and German, then read it aloud.

## Features

- **Drawing Canvas**: Draw freely using mouse, touch screen, or pen/stylus
- **AI-Powered Analysis**: Uses Qwen2-VL 2B model to understand sketches
- **Bilingual Stories**: Generates kindergarten-level stories in English and German
- **Text-to-Speech**: Reads stories aloud in both languages
- **Simple UI**: Clean, child-friendly interface

## Requirements

- **Qt 6.x** (Core, Widgets, Network, TextToSpeech modules)
- **CMake 3.16+**
- **C++17 compatible compiler**
- **Hugging Face API Key** (for Qwen2-VL model access)

## Building the Application

### Windows

1. Install Qt 6.x from [qt.io](https://www.qt.io/download)
2. Install CMake from [cmake.org](https://cmake.org/download/)
3. Set up your environment:
   ```powershell
   # Set Qt6_DIR (adjust path to your Qt installation)
   $env:Qt6_DIR = "D:\Apps\Qt\6.10.1\mingw_64\lib\cmake\Qt6"
   ```

4. Build the project:
   ```powershell
   mkdir build
   cd build
   cmake ..
   cmake --build . --config Release
   ```

### Linux

1. Install Qt6 and development tools:
   ```bash
   sudo apt-get update
   sudo apt-get install qt6-base-dev qt6-base-dev-tools cmake build-essential
   ```

2. Build the project:
   ```bash
   mkdir build
   cd build
   cmake ..
   make
   ```

### macOS

1. Install Qt6 using Homebrew:
   ```bash
   brew install qt@6 cmake
   ```

2. Build the project:
   ```bash
   mkdir build
   cd build
   cmake -DCMAKE_PREFIX_PATH=$(brew --prefix qt@6) ..
   make
   ```

## Configuration

### Setting up the API Key

The app uses Hugging Face Inference API to access the Qwen2-VL-2B-Instruct model. You have three options:

#### Option 1: Using config.h (Recommended)

1. Copy the example config file:
   ```bash
   cp src/config.h.example src/config.h
   ```

2. Edit `src/config.h` and replace `hf_YOUR_API_KEY_HERE` with your actual API key

3. Rebuild the project

**Note:** `config.h` is in `.gitignore` and will NOT be committed to Git.

#### Option 2: Set directly in code

Edit `src/MainWindow.cpp` and replace `hf_YOUR_API_KEY_HERE` with your API key.

**⚠️ Warning:** This method is NOT recommended if you plan to commit to Git, as your API key will be exposed!

#### Option 3: Environment variable

Set the API key as an environment variable:

   **Windows (PowerShell):**
   ```powershell
   $env:HUGGINGFACE_API_KEY = "your-api-key-here"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set HUGGINGFACE_API_KEY=your-api-key-here
   ```

   **Linux/macOS:**
   ```bash
   export HUGGINGFACE_API_KEY="your-api-key-here"
   ```

### Getting a Hugging Face API Key

1. Create a Hugging Face account at [huggingface.co](https://huggingface.co)
2. Go to Settings → Access Tokens: https://huggingface.co/settings/tokens
3. Create a new token with "Read" permissions
4. Copy the token (it starts with `hf_`)

### Using a Different API Endpoint

If you're using a different API provider or self-hosted model, you can change the API URL:

```cpp
m_analyzer->setApiUrl("https://your-api-endpoint.com/v1/chat/completions");
```

## Usage

1. **Launch the application**
2. **Draw on the canvas** using your mouse, touch screen, or stylus
3. **Click the arrow button** (→) to analyze your drawing
4. **Wait for the story** to be generated and displayed
5. **Listen** as the app reads the story in English, then German

## Project Structure

```
Drawlingo/
├── CMakeLists.txt          # Build configuration
├── README.md               # This file
└── src/
    ├── main.cpp            # Application entry point
    ├── MainWindow.h/cpp    # Main window UI and logic
    ├── DrawingCanvas.h/cpp # Drawing canvas widget
    ├── SketchAnalyzer.h/cpp # API integration for sketch analysis
    └── config.h.example    # Example config file (copy to config.h)
```

## Troubleshooting

### Text-to-Speech not working

- **Windows**: Ensure you have SAPI5 voices installed
- **Linux**: Install speech synthesis:
  ```bash
  sudo apt-get install speech-dispatcher
  ```
- **macOS**: Should work out of the box with system voices

### API errors

- Verify your Hugging Face API key is set correctly
- Check your internet connection
- Ensure the Qwen2-VL-2B-Instruct model is accessible via the API
- The model may take a moment to load on first use (cold start) - wait 30-60 seconds and try again

### Drawing not working

- Ensure your touch screen/stylus drivers are installed
- Try using the mouse as an alternative input method
- Check that the canvas widget is receiving events

## Security Note

**⚠️ IMPORTANT:** Never commit API keys to Git! 

- API keys are like passwords - if exposed, others can use your account
- Use `config.h` (which is in `.gitignore`) or environment variables
- If you accidentally commit an API key, revoke it immediately and create a new one

## License

This project is provided as-is for educational and demonstration purposes.

## Notes

- The app requires an internet connection to use the AI model
- First API call may take longer as the model loads (20-60 seconds)
- Text-to-speech quality depends on your system's installed voices
- For production use, consider implementing local model inference for better performance and privacy

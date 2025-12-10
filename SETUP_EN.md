# Drawlingo Environment Setup Guide

## ✅ Environment Setup Complete!

The Conda environment `Drawlingo` has been successfully created with all dependencies installed.

## 📋 Environment Information

- **Environment Name**: Drawlingo
- **Python Version**: 3.10.19
- **Key Installed Packages**:
  - PyQt6 6.10.0 (GUI framework)
  - torch 2.9.1 (Deep learning framework)
  - transformers 4.57.3 (Hugging Face model library)
  - qwen-vl-utils 0.0.14 (Qwen2-VL utilities)
  - bitsandbytes 0.48.2 (4-bit quantization support)
  - pyttsx3 2.99 (Text-to-speech)

## 🚀 Usage Instructions

### 1. Activate Environment

**Option A: Standard Method (if conda is initialized):**
```bash
conda activate Drawlingo
```

**Option B: Use Helper Script (Recommended if conda activate doesn't work):**
```bash
# Windows Batch File
activate_env.bat

# Or PowerShell Script
.\activate_env.ps1
```

**Option C: Direct Path Method (if conda init fails):**
```bash
# Windows
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo

# Linux/macOS
source ~/miniconda3/bin/activate Drawlingo
```

**Note:** If you get "Run conda init before conda activate" error, see `TROUBLESHOOTING.md` for solutions.

### 2. Run the Application

After activating the environment, run:
```bash
python main.py
```

Or use the quick start scripts:
- Windows: `run.bat`
- Linux/macOS: `run.sh`

### 3. Deactivate Environment

```bash
conda deactivate
```

## 📝 Important Notes

1. **First Run**: The first time you run the app, it will automatically download the Qwen2-VL-2B model (~2GB), which may take some time
2. **Memory Requirements**: Recommended at least 4-6 GB of available RAM
3. **Model Caching**: The model will be cached in `~/.cache/huggingface/` directory, making subsequent runs faster

## 🔧 Environment Management

### List All Environments
```bash
conda env list
```

### Remove Environment (if needed)
```bash
conda env remove -n Drawlingo
```

### Export Environment Configuration
```bash
conda env export > environment.yml
```

### Create Environment from Configuration File
```bash
conda env create -f environment.yml
```

## 📦 Update Dependencies

To update a specific package:
```bash
conda activate Drawlingo
pip install --upgrade <package_name>
```

## ❓ Frequently Asked Questions

**Q: How do I confirm the environment is activated?**
A: The command prompt will show `(Drawlingo)` at the beginning

**Q: What if model download fails?**
A: Check your internet connection, or manually download the model from Hugging Face to the cache directory

**Q: What if I run out of memory?**
A: The model is already configured for 4-bit quantization. If you still encounter issues, try closing other applications

**Q: Can I use GPU acceleration?**
A: Yes! If you have a CUDA-compatible GPU, PyTorch will automatically detect and use it. The model will run faster on GPU.

**Q: How do I reinstall if something goes wrong?**
A: You can remove and recreate the environment:
```bash
conda env remove -n Drawlingo
conda create -n Drawlingo python=3.10 -y
conda activate Drawlingo
pip install -r requirements.txt
```

## 🔍 Verify Installation

To verify all packages are installed correctly:
```bash
conda activate Drawlingo
python --version
pip list | grep -E "PyQt6|torch|transformers|qwen"
```

## 📚 Additional Resources

- **Main README**: See `README_PYTHON.md` for detailed application documentation
- **Python Integration**: See `PYTHON_INTEGRATION.md` for integration details
- **Original C++ Code**: Backed up in `src_backup/` directory


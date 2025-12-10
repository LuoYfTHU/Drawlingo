# Troubleshooting Guide - Conda Activation Issues

## Problem: "Run conda init before conda activate"

If you see this error, here are several solutions:

## Solution 1: Restart PowerShell (Recommended)

After running `conda init powershell`, you need to **restart your PowerShell window**:

1. Close the current PowerShell window
2. Open a new PowerShell window
3. Try `conda activate Drawlingo` again

## Solution 2: Use the Activation Scripts

We've created helper scripts that work without conda init:

### Windows Batch File (CMD/PowerShell):
```bash
activate_env.bat
```

### PowerShell Script:
```powershell
.\activate_env.ps1
```

Or right-click and "Run with PowerShell"

## Solution 3: Manual Activation (Direct Path)

If conda activate doesn't work, use the direct path method:

```bash
# Replace with your actual conda installation path
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo
```

Then run:
```bash
python main.py
```

## Solution 4: Initialize Conda Manually

If `conda init` doesn't work, try:

### For PowerShell:
```powershell
conda init powershell
# Then restart PowerShell
```

### For CMD:
```cmd
conda init cmd.exe
# Then restart CMD
```

### Check if initialization worked:
After restarting, you should see `(base)` in your prompt if conda is initialized.

## Solution 5: Use Anaconda Prompt

If you have Anaconda/Miniconda installed:

1. Open "Anaconda Prompt" or "Anaconda PowerShell Prompt" from Start Menu
2. Run: `conda activate Drawlingo`
3. Navigate to project: `cd D:\Workspace\Drawlingo`
4. Run: `python main.py`

## Solution 6: Verify Environment Exists

Check if the environment was created:

```bash
conda env list
```

You should see `Drawlingo` in the list. If not, recreate it:

```bash
conda create -n Drawlingo python=3.10 -y
conda activate Drawlingo
pip install -r requirements.txt
```

## Solution 7: Use Full Python Path

If activation still fails, you can use the full Python path:

```bash
# Find the Python executable
D:\Apps\MiniConda\envs\Drawlingo\python.exe main.py
```

## Quick Test

To test if everything works, try:

```bash
# Method 1: Direct activation
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo
python --version  # Should show Python 3.10.19

# Method 2: Use the script
.\activate_env.bat
```

## Still Having Issues?

1. **Check conda installation path**: The scripts assume conda is at `D:\Apps\MiniConda`. If yours is different, edit the scripts.

2. **Check environment location**: 
   ```bash
   conda info --envs
   ```

3. **Recreate environment**:
   ```bash
   conda env remove -n Drawlingo
   conda create -n Drawlingo python=3.10 -y
   conda activate Drawlingo
   pip install -r requirements.txt
   ```

4. **Use virtual environment instead** (alternative):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```





# Quick Start Guide - 快速开始指南

## 🚀 最简单的方法（推荐）

### Windows 用户：

**方法 1: 双击运行批处理文件**
```
activate_env.bat
```

**方法 2: PowerShell 中运行**
```powershell
.\activate_env.ps1
```

这两个脚本会自动：
- ✅ 激活 Drawlingo 环境
- ✅ 启动应用程序

---

## 📝 手动激活（如果脚本不工作）

### 在 PowerShell 中：

```powershell
# 1. 初始化 conda（每次新开 PowerShell 需要运行一次）
D:\Apps\MiniConda\Scripts\conda.exe shell.powershell hook | Out-String | Invoke-Expression

# 2. 激活环境
conda activate Drawlingo

# 3. 运行应用
python main.py
```

### 在 CMD 中：

```cmd
# 1. 激活环境
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo

# 2. 运行应用
python main.py
```

---

## 🔧 让 conda 自动初始化（可选）

如果你想每次打开 PowerShell 时自动初始化 conda：

### 方法 1: 运行初始化脚本
```powershell
. .\init_conda.ps1
```

### 方法 2: 手动添加到 PowerShell 配置文件

1. 检查配置文件是否存在：
```powershell
Test-Path $PROFILE
```

2. 如果返回 False，创建配置文件：
```powershell
New-Item -Path $PROFILE -Type File -Force
```

3. 添加 conda 初始化代码：
```powershell
notepad $PROFILE
```

在打开的记事本中添加：
```powershell
# Initialize conda
& "D:\Apps\MiniConda\Scripts\conda.exe" shell.powershell hook | Out-String | Invoke-Expression
```

4. 保存并关闭，重启 PowerShell

---

## ❓ 常见问题

**Q: 为什么 conda init 显示 "no change"？**
A: 这表示 conda 已经初始化过了，但 PowerShell 配置文件可能没有正确加载。使用上面的手动初始化方法即可。

**Q: 每次都要手动初始化吗？**
A: 如果不想每次手动初始化，可以：
- 使用 `activate_env.bat` 或 `activate_env.ps1` 脚本（推荐）
- 或者按照上面的方法添加到 PowerShell 配置文件

**Q: 最简单的方法是什么？**
A: 直接双击 `activate_env.bat` 文件！这是最简单的方法。

---

## ✅ 验证安装

运行以下命令验证环境是否正确：

```powershell
# 激活环境
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo

# 检查 Python 版本
python --version
# 应该显示: Python 3.10.19

# 检查已安装的包
pip list | Select-String -Pattern "PyQt6|torch|transformers"
```





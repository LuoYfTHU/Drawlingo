# Drawlingo 环境设置指南

## ✅ 环境已创建完成！

Conda 环境 `Drawlingo` 已成功创建，所有依赖已安装。

## 📋 环境信息

- **环境名称**: Drawlingo
- **Python 版本**: 3.10.19
- **已安装的主要包**:
  - PyQt6 6.10.0 (GUI框架)
  - torch 2.9.1 (深度学习框架)
  - transformers 4.57.3 (Hugging Face模型库)
  - qwen-vl-utils 0.0.14 (Qwen2-VL工具)
  - bitsandbytes 0.48.2 (4-bit量化支持)
  - pyttsx3 2.99 (文本转语音)

## 🚀 使用方法

### 0. 初始化 Conda（如果尚未初始化）

如果遇到 "Run conda init before conda activate" 错误，需要先初始化 conda：

**方法1: 使用批处理文件（推荐，无执行策略限制）：**
```cmd
init_conda.bat
```

**方法2: 直接在 PowerShell 中运行（如果知道 conda 路径）：**
```powershell
# 如果 conda 在 D:\Apps\MiniConda
D:\Apps\MiniConda\Scripts\conda.exe init powershell

# 如果 conda 在其他位置，替换为实际路径
# 例如：C:\Users\<用户名>\anaconda3\Scripts\conda.exe init powershell
```

**方法3: 绕过 PowerShell 执行策略运行脚本：**
```powershell
# 临时允许运行脚本（仅当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\init_conda.ps1
```

**重要提示：**
- 运行 `conda init` 后，**必须关闭并重新打开 PowerShell** 才能生效
- 重新打开后，提示符前应显示 `(base)`，表示 conda 已初始化
- 如果 PowerShell 脚本被阻止，使用 `init_conda.bat` 批处理文件

### 1. 激活环境

**方法A: 标准方法（如果conda已初始化）：**
```bash
conda activate Drawlingo
```

**方法B: 使用辅助脚本（推荐，如果conda activate不工作）：**
```bash
# Windows批处理文件
activate_env.bat

# 或PowerShell脚本
.\activate_env.ps1
```

**方法C: 直接路径方法（如果conda init失败）：**
```bash
# Windows
D:\Apps\MiniConda\Scripts\activate.bat Drawlingo

# Linux/macOS
source ~/miniconda3/bin/activate Drawlingo
```

**注意：** 如果遇到"Run conda init before conda activate"错误，请查看 `TROUBLESHOOTING.md` 获取解决方案。

### 2. 运行应用

激活环境后，运行：
```bash
python main.py
```

或者使用快捷脚本：
- Windows: `run.bat`
- Linux/macOS: `run.sh`

### 3. 退出环境

```bash
conda deactivate
```

## 📝 注意事项

1. **首次运行**: 第一次运行时会自动下载 Qwen2-VL-2B 模型（约2GB），需要一些时间
2. **内存要求**: 建议至少 4-6 GB 可用内存
3. **模型缓存**: 模型会缓存在 `~/.cache/huggingface/` 目录，后续运行会更快

## 🔧 环境管理

### 查看环境列表
```bash
conda env list
```

### 删除环境（如果需要）
```bash
conda env remove -n Drawlingo
```

### 导出环境配置
```bash
conda env export > environment.yml
```

### 从配置文件创建环境
```bash
conda env create -f environment.yml
```

## 📦 更新依赖

如果需要更新某个包：
```bash
conda activate Drawlingo
pip install --upgrade <package_name>
```

## ❓ 常见问题

**Q: 如何确认环境已激活？**
A: 命令行提示符前会显示 `(Drawlingo)`

**Q: 模型下载失败怎么办？**
A: 检查网络连接，或手动从 Hugging Face 下载模型到缓存目录

**Q: 内存不足怎么办？**
A: 模型已配置为4-bit量化，如果仍不足，可以关闭其他应用程序


# 视频分析助手 Skill (Video Analyzer Skill)

[English](README.md) | [中文](README.zh.md)

本 Skill 允许 AI 编辑器（如 **Claude Code**, **GitHub Copilot**, **Antigravity**, **OpenCode**，**Cursor**等）通过调用 [video-helper](https://github.com/LDJ-creat/video-helper) 后端服务来实现深度的视频分析功能。

## 🚀 前置要求

本 Skill 是 AI 编辑器与 **视频分析助手** 之间的桥梁。你 **必须** 先下载并配置完整项目：

1.  **后端服务**: 下载并设置 [video-helper](https://github.com/LDJ-creat/video-helper)。
2.  **配置**: 确保后端服务正常运行（默认地址通常为 `http://localhost:8000`）。

## 📥 安装方式

你可以通过将本仓库的文件放置在对应 AI 编辑器的 Skill 目录下进行安装。

### 方式 1：自动脚本安装 (推荐)

克隆本仓库后，运行对应的安装脚本：

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Linux / macOS (Shell):**
```bash
chmod +x install.sh
./install.sh
```

### 方式 2：手动安装

将本仓库的文件（不包含安装脚本和 git 文件）复制到以下对应 AI 编辑器的路径下：

- **Claude Code**: `~/.claude/skills/video-analyzer-skill/`
- **OpenCode**: `~/.config/opencode/skills/video-analyzer-skill/`
- **GitHub Copilot**: `~/.copilot/skills/video-analyzer-skill/`

## 💡 使用示例

安装完成后，你只需直接向 AI 编辑器发送视频分析指令即可：

> “帮我分析一下这个视频：https://www.youtube.com/watch?v=VIDEO_ID”

AI 将调用本 Skill 触发分析流水线。你可以在 **视频分析助手** 的 Web 端或桌面端查看生成的结构化结果（思维导图、重点摘要、时间戳等）：

🔗 **查看结果**: [https://github.com/LDJ-creat/video-helper](https://github.com/LDJ-creat/video-helper)

## 🔗 相关项目

- [video-helper](https://github.com/LDJ-creat/video-helper): 视频分析助手的核心后端与前端项目。
- [video-helper-skill](https://github.com/LDJ-creat/video-helper-skill): 本 Skill 仓库。

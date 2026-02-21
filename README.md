# Video Analyzer Skill

[English](README.md) | [中文](README.zh.md)

This skill enables AI editors (such as **Claude Code**, **GitHub Copilot**, **Antigravity**, **OpenCode**, **Cursor**, etc.) to perform deep video analysis by leveraging the [video-helper](https://github.com/LDJ-creat/video-helper) backend service.

## 🚀 Prerequisites

This skill is a bridge between your AI editor and the **Video Analysis Assistant**. You **must** have the main project installed and configured:

1.  **Backend Service**: Download and set up [video-helper](https://github.com/LDJ-creat/video-helper).
2.  **Configuration**: Ensure the backend is running (typically at `http://localhost:8000`).

## 📥 Installation

You can install this skill by placing the files in the appropriate directory for your AI editor.

### Option 1: Automatic Installation (Recommended)

Clone the repository and run the installation script:

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Linux / macOS (Shell):**
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

Copy the contents of this repository (excluding scripts and git files) to one of the following paths depending on your AI editor:

- **Claude Code**: `~/.claude/skills/video-analyzer-skill/`
- **OpenCode**: `~/.config/opencode/skills/video-analyzer-skill/`
- **GitHub Copilot**: `~/.copilot/skills/video-analyzer-skill/`

## 💡 Usage Example

Once installed, you can simply ask your AI editor to analyze a video:

> "Help me analyze this video: https://www.youtube.com/watch?v=VIDEO_ID"

The AI will use the skill to trigger the analysis pipeline. You can view the structured results (mind maps, highlights, timestamps) in the **Video Analysis Assistant** web or desktop interface:

🔗 **View Results**: [https://github.com/LDJ-creat/video-helper](https://github.com/LDJ-creat/video-helper)

## 🔗 Related Projects

- [video-helper](https://github.com/LDJ-creat/video-helper): The core backend and frontend for video analysis.
- [video-helper-skill](https://github.com/LDJ-creat/video-helper-skill): This repository.

#!/bin/bash

# install.sh
SKILL_NAME="video-analyzer-skill"
DEST_PATHS=(
    "$HOME/.claude/skills/$SKILL_NAME"
    "$HOME/.config/opencode/skills/$SKILL_NAME"
    "$HOME/.copilot/skills/$SKILL_NAME"
    "$HOME/.gemini/skills/$SKILL_NAME"
    "$HOME/.gemini/antigravity/skills/$SKILL_NAME"
)

# Exclude list for rsync/grep
EXCLUDE_PATTERN="install.ps1|install.sh|.git|README|task.md|implementation_plan.md|walkthrough.md|__pycache__"

echo "Starting installation of $SKILL_NAME..."

for DEST_PATH in "${DEST_PATHS[@]}"; do
    PARENT_DIR=$(dirname "$DEST_PATH")
    
    # Check if parent directory is writable/exists
    if [ ! -d "$PARENT_DIR" ]; then
        mkdir -p "$PARENT_DIR" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "Skipping $DEST_PATH (could not create parent directory)"
            continue
        fi
    fi

    if [ -d "$DEST_PATH" ]; then
        echo "Updating existing skill at: $DEST_PATH"
        rm -rf "$DEST_PATH"
    else
        echo "Installing skill to: $DEST_PATH"
    fi
    
    mkdir -p "$DEST_PATH"
    
    # Use rsync if available for easier exclusion, otherwise use cp
    if command -v rsync >/dev/null 2>&1; then
        rsync -av --exclude="install.ps1" --exclude="install.sh" --exclude=".git*" --exclude="README*" --exclude="task.md" --exclude="implementation_plan.md" --exclude="walkthrough.md" --exclude="__pycache__" ./ "$DEST_PATH/"
    else
        # Fallback to cp and manual cleanup
        cp -R . "$DEST_PATH"
        find "$DEST_PATH" -maxdepth 1 -name "install.ps1" -delete
        find "$DEST_PATH" -maxdepth 1 -name "install.sh" -delete
        find "$DEST_PATH" -maxdepth 1 -name ".git*" -exec rm -rf {} +
        find "$DEST_PATH" -maxdepth 1 -name "README*" -delete
        find "$DEST_PATH" -maxdepth 1 -name "task.md" -delete
        find "$DEST_PATH" -maxdepth 1 -name "implementation_plan.md" -delete
        find "$DEST_PATH" -maxdepth 1 -name "walkthrough.md" -delete
    fi
done

echo "Installation complete!"

# install.ps1
$SkillName = "video-analyzer-skill"
$DestPaths = @(
    "$HOME\.claude\skills\$SkillName",
    "$HOME\.config\opencode\skills\$SkillName",
    "$HOME\.copilot\skills\$SkillName",
    "$HOME\.gemini\skills\$SkillName",
    "$HOME\.gemini\antigravity\skills\$SkillName"
)

$ExcludeFiles = @("install.ps1", "install.sh", ".git*", ".gitignore", "README*", "task.md", "implementation_plan.md", "walkthrough.md")

Write-Host "Starting installation of $SkillName..." -ForegroundColor Cyan

foreach ($DestPath in $DestPaths) {
    $ParentDir = Split-Path -Path $DestPath -Parent
    
    # Try to create parent directory if it doesn't exist
    if (!(Test-Path -Path $ParentDir)) {
        try {
            New-Item -ItemType Directory -Force -Path $ParentDir -ErrorAction SilentlyContinue | Out-Null
            Write-Host "Created directory: $ParentDir"
        } catch {
            Write-Host "Skipping $DestPath (could not create parent directory)" -ForegroundColor Yellow
            continue
        }
    }

    if (Test-Path -Path $DestPath) {
        Write-Host "Updating existing skill at: $DestPath"
        Remove-Item -Path $DestPath -Recurse -Force
    } else {
        Write-Host "Installing skill to: $DestPath"
    }

    New-Item -ItemType Directory -Force -Path $DestPath | Out-Null
    Copy-Item -Path ".\*" -Destination $DestPath -Recurse -Exclude $ExcludeFiles -Force
}

Write-Host "Installation complete!" -ForegroundColor Green

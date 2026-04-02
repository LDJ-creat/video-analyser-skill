#!/usr/bin/env python3
"""
Video Analyzer - Submit Plan
Usage: python submit_plan.py <jobId> [plan.json]
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

DEFAULT_API_BASE = os.environ.get("VIDEO_HELPER_API_URL", "http://localhost:8000/api/v1")


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_env_file(path: Path) -> None:
    try:
        if not path.exists():
            return
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception:
        pass


def _resolve_default_plan_path(job_id: str) -> Path | None:
    run_base = _skill_root() / "data" / "runs"
    candidates = list(run_base.glob(f"*/{job_id}/plan.json"))
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        return None

    cwd_default = Path("plan.json")
    if cwd_default.is_file():
        return cwd_default
    return None

def main():
    _load_env_file(_skill_root() / ".env")
    api_base = os.environ.get("VIDEO_HELPER_API_URL", DEFAULT_API_BASE).rstrip("/")

    parser = argparse.ArgumentParser(description="Submit completed analysis plan JSON.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("plan_file", nargs="?", default=None, help="Path to your generated plan JSON file (optional).")
    args = parser.parse_args()

    url = f"{api_base}/jobs/{args.job_id}/plan"

    plan_path = Path(args.plan_file) if args.plan_file else (_resolve_default_plan_path(args.job_id) or Path(""))
    
    # Pre-flight check: ensure the file exists and is valid JSON
    if not plan_path.is_file():
        print("FAILED: plan file not found.", file=sys.stderr)
        print("Provide an explicit path, e.g.:", file=sys.stderr)
        print(f"  python scripts/submit_plan.py {args.job_id} data/runs/<projectId>/{args.job_id}/plan.json", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            data_content = f.read()
            json.loads(data_content) # simple structural check
    except Exception as e:
        print(f"FAILED: File {plan_path} is not valid JSON - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Submitting {plan_path} to {url}...")
    try:
        req = urllib.request.Request(
            url, 
            data=data_content.encode('utf-8'),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            ret_data = response.read().decode('utf-8')
            print(f"SUCCESS: Submitted plan! Server Response: {ret_data}")
            print(f"Next Step: Use `python scripts/poll_job.py {args.job_id}` to wait for completion.")
    except Exception as e:
        print(f"FAILED to submit plan: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

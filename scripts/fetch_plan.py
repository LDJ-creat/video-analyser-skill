#!/usr/bin/env python3
"""
Video Analyzer - Fetch Plan Request
Usage: python fetch_plan.py <jobId> [--out PATH]
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


def _default_plan_request_out_path(*, project_id: str, job_id: str) -> Path:
    return _skill_root() / "data" / "runs" / project_id / job_id / "plan_request.json"

def main():
    _load_env_file(_skill_root() / ".env")
    api_base = os.environ.get("VIDEO_HELPER_API_URL", DEFAULT_API_BASE).rstrip("/")

    parser = argparse.ArgumentParser(description="Fetch the plan request data containing transcript.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("--out", default=None, help="Output file path. Default: data/runs/<projectId>/<jobId>/plan_request.json")
    args = parser.parse_args()

    url = f"{api_base}/jobs/{args.job_id}/plan-request"
    
    print(f"Fetching plan request from {url}...")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))

        project_id = str(payload.get("projectId") or "unknown-project").strip() or "unknown-project"
        out_path = Path(args.out) if args.out else _default_plan_request_out_path(project_id=project_id, job_id=args.job_id)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"SUCCESS: Saved plan request data to {out_path}")
        print("Next Step: Use your LLM context to read this file and generate a corresponding plan.json.")
        print(f"Recommended plan output path: {out_path.with_name('plan.json')}")
    except Exception as e:
        print(f"FAILED to fetch plan request: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

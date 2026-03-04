#!/usr/bin/env python3
"""
Video Analyzer - Submit Plan
Usage: python submit_plan.py <jobId> plan.json
"""

import argparse
import json
import os
import sys
import urllib.request

DEFAULT_API_BASE = os.environ.get("VIDEO_HELPER_API_URL", "http://localhost:8000/api/v1")

def main():
    parser = argparse.ArgumentParser(description="Submit completed analysis plan JSON.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("plan_file", help="Path to your generated plan JSON file.")
    args = parser.parse_args()

    url = f"{DEFAULT_API_BASE}/jobs/{args.job_id}/plan"
    
    # Pre-flight check: ensure the file exists and is valid JSON
    if not os.path.exists(args.plan_file):
        print(f"FAILED: File {args.plan_file} not found.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(args.plan_file, "r", encoding="utf-8") as f:
            data_content = f.read()
            json.loads(data_content) # simple structural check
    except Exception as e:
        print(f"FAILED: File {args.plan_file} is not valid JSON - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Submitting {args.plan_file} to {url}...")
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

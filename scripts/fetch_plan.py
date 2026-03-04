#!/usr/bin/env python3
"""
Video Analyzer - Fetch Plan Request
Usage: python fetch_plan.py <jobId> [--out plan_request.json]
"""

import argparse
import json
import os
import sys
import urllib.request

DEFAULT_API_BASE = os.environ.get("VIDEO_HELPER_API_URL", "http://localhost:8000/api/v1")

def main():
    parser = argparse.ArgumentParser(description="Fetch the plan request data containing transcript.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("--out", default="plan_request.json", help="Output file path.")
    args = parser.parse_args()

    url = f"{DEFAULT_API_BASE}/jobs/{args.job_id}/plan-request"
    
    print(f"Fetching plan request from {url}...")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            with open(args.out, "wb") as f:
                f.write(data)
        print(f"SUCCESS: Saved plan request data to {args.out}")
        print("Next Step: Use your LLM context to read this file and generate a corresponding plan.json.")
    except Exception as e:
        print(f"FAILED to fetch plan request: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

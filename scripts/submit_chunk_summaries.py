#!/usr/bin/env python3
"""
Video Analyzer - Submit external chunk summaries.

Usage:
    python scripts/submit_chunk_summaries.py <jobId> [summaries.json]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
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


def _http_post_json(url: str, payload: dict, timeout: float = 30.0) -> tuple[int, dict]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return int(resp.status), json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return int(e.code), json.loads(body)
        except Exception:
            return int(e.code), {"error": body}


def _resolve_default_summaries_path(job_id: str) -> Path | None:
    # Prefer normalized run directory: data/runs/<projectId>/<jobId>/summaries.json
    run_base = _skill_root() / "data" / "runs"
    candidates = list(run_base.glob(f"*/{job_id}/summaries.json"))
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        return None

    # Backward compatibility: current working directory summaries.json
    cwd_default = Path("summaries.json")
    if cwd_default.is_file():
        return cwd_default
    return None


def main() -> None:
    _load_env_file(_skill_root() / ".env")
    api_base = os.environ.get("VIDEO_HELPER_API_URL", DEFAULT_API_BASE).rstrip("/")

    parser = argparse.ArgumentParser(description="Submit externally generated chunk summaries for a blocked job.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("summaries_file", nargs="?", default=None, help="Path to summaries.json (optional)")
    args = parser.parse_args()

    path = Path(args.summaries_file) if args.summaries_file else (_resolve_default_summaries_path(args.job_id) or Path(""))
    if not path.is_file():
        print("FAILED: summaries file not found.", file=sys.stderr)
        print("Provide an explicit path, e.g.:", file=sys.stderr)
        print(f"  python scripts/submit_chunk_summaries.py {args.job_id} data/runs/<projectId>/{args.job_id}/summaries.json", file=sys.stderr)
        sys.exit(1)

    try:
        raw_obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: invalid JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    if isinstance(raw_obj, list):
        payload = {"summaries": raw_obj}
    elif isinstance(raw_obj, dict):
        payload = raw_obj
    else:
        print("FAILED: summaries file must be a JSON object or array.", file=sys.stderr)
        sys.exit(1)

    summaries = payload.get("summaries") if isinstance(payload, dict) else None
    if not isinstance(summaries, list) or not summaries:
        print("FAILED: payload must contain non-empty summaries array.", file=sys.stderr)
        sys.exit(1)

    url = f"{api_base}/jobs/{args.job_id}/chunk-summaries"
    print(f"Submitting {len(summaries)} chunk summaries to {url} ...")

    try:
        status, result = _http_post_json(url, payload)
    except Exception as e:
        print(f"FAILED to submit chunk summaries: {e}", file=sys.stderr)
        sys.exit(1)

    if status != 200:
        print(f"FAILED to submit chunk summaries (HTTP {status})", file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    print("SUCCESS: chunk summaries submitted.")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("")
    print("Next steps:")
    print(f"  1. python scripts/fetch_plan.py {args.job_id}")
    print("  2. Generate or revise plan.json using the returned plan request")
    print(f"  3. python scripts/submit_plan.py {args.job_id} plan.json")
    print(f"  4. python scripts/poll_job.py {args.job_id}")


if __name__ == "__main__":
    main()

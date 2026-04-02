#!/usr/bin/env python3
"""
Video Analyzer - Fetch transcript chunks for long-video external LLM flow.

Usage:
    python scripts/fetch_chunks.py <jobId> [--out PATH]
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


def _http_get_json(url: str, timeout: float = 30.0) -> tuple[int, dict]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
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


def _batch_ranges(total: int, batch_size: int = 3) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    i = 0
    while i < total:
        j = min(i + batch_size - 1, total - 1)
        out.append((i, j))
        i += batch_size
    return out


def _default_chunks_out_path(*, project_id: str, job_id: str) -> Path:
    return _skill_root() / "data" / "runs" / project_id / job_id / "chunks.json"


def main() -> None:
    _load_env_file(_skill_root() / ".env")
    api_base = os.environ.get("VIDEO_HELPER_API_URL", DEFAULT_API_BASE).rstrip("/")

    parser = argparse.ArgumentParser(description="Fetch transcript chunks for long-video external LLM summarization.")
    parser.add_argument("job_id", help="The UUID of the job.")
    parser.add_argument("--out", default=None, help="Output file path. Default: data/runs/<projectId>/<jobId>/chunks.json")
    args = parser.parse_args()

    url = f"{api_base}/jobs/{args.job_id}/chunks"
    print(f"Fetching chunks from {url} ...")

    try:
        status, payload = _http_get_json(url)
    except Exception as e:
        print(f"FAILED to fetch chunks: {e}", file=sys.stderr)
        sys.exit(1)

    if status != 200:
        print(f"FAILED to fetch chunks (HTTP {status})", file=sys.stderr)
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    project_id = str(payload.get("projectId") or "unknown-project").strip() or "unknown-project"
    out_path = Path(args.out) if args.out else _default_chunks_out_path(project_id=project_id, job_id=args.job_id)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    is_long = bool(payload.get("isLongVideo"))
    if not is_long:
        print(f"Saved response to {out_path}")
        print("This job is not classified as long-video. Continue with:")
        print(f"  python scripts/fetch_plan.py {args.job_id}")
        return

    chunks = payload.get("chunks") if isinstance(payload.get("chunks"), list) else []
    chunk_count = int(payload.get("chunkCount") or len(chunks))
    window_ms = payload.get("windowMs")
    total_batches = int(payload.get("totalBatches") or ((chunk_count + 2) // 3))

    print(f"Fetched {chunk_count} chunks (windowMs={window_ms}) -> {out_path}")
    print("")
    print(f"Long-video: process in batches of 3 ({total_batches} total rounds):")

    ranges = _batch_ranges(chunk_count, 3)
    for idx, (start, end) in enumerate(ranges, start=1):
        ids = []
        for k in range(start, end + 1):
            chunk = chunks[k] if k < len(chunks) and isinstance(chunks[k], dict) else {}
            ids.append(str(chunk.get("chunkId") or f"chunk-{k}"))
        chunk_ids = ", ".join(ids)
        print(f"  Batch {idx}/{len(ranges)}: chunks[{start}..{end}] ({chunk_ids})")

    print("")
    print("For EACH batch, generate summaries with fields:")
    print("  chunkId, startMs, endMs, summary, points[], terms[], keyMoments[]")
    print("")
    summaries_path = out_path.with_name("summaries.json")
    print("When all summaries are ready, save to:")
    print(f"  {summaries_path}")
    print("Then submit with:")
    print(f"  python scripts/submit_chunk_summaries.py {args.job_id} {summaries_path}")


if __name__ == "__main__":
    main()

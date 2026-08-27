import argparse
import concurrent.futures
import hashlib
import json
import time
from pathlib import Path

import requests


def analyze(index, score, api_url, output):
    started = time.perf_counter()
    with score.open("rb") as stream:
        response = requests.post(api_url, files={"files": (score.name, stream, "application/vnd.recordare.musicxml")}, timeout=600)
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    rows = payload.get("rows", [])
    item = {
        "index": index,
        "file": score.name,
        "source_sha256": hashlib.sha256(score.read_bytes()).hexdigest(),
        "row_count": len(rows),
        "labeled_count": sum(bool(row.get("romanNumeral")) for row in rows),
        "abstention_count": sum(not bool(row.get("romanNumeral")) for row in rows),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "rows": rows,
    }
    (output / f"{index:03d}.json").write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--output", type=Path, default=Path("rerun"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    scores = sorted(args.corpus.resolve().glob("*.mxl"))
    if len(scores) != 335:
        raise SystemExit(f"Expected 335 .mxl files; found {len(scores)}")
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(analyze, index, score, args.api_url, args.output) for index, score in enumerate(scores, 1)]
        for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(f"[{completed}/335] {result['file']}: {result['row_count']} rows", flush=True)
    results.sort(key=lambda item: item["index"])
    summary = {
        "files_requested": 335,
        "files_completed": len(results),
        "rows": sum(item["row_count"] for item in results),
        "labeled": sum(item["labeled_count"] for item in results),
        "abstentions": sum(item["abstention_count"] for item in results),
        "per_work": [{key: value for key, value in item.items() if key != "rows"} for item in results],
    }
    (args.output / "batch_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()


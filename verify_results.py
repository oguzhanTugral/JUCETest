import argparse
import csv
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results/batch_summary.json"))
    parser.add_argument("--realtime", type=Path, default=Path("results/realtime_validation_report.json"))
    parser.add_argument("--manifest", type=Path, default=Path("corpus_manifest.csv"))
    args = parser.parse_args()
    manifest = list(csv.DictReader(args.manifest.open(encoding="utf-8-sig", newline="")))
    batch = json.loads(args.results.read_text(encoding="utf-8"))
    realtime = json.loads(args.realtime.read_text(encoding="utf-8"))
    assert len(manifest) == 335
    assert len({row["filename"] for row in manifest}) == 335
    assert all(len(row["sha256"]) == 64 for row in manifest)
    assert batch["files_requested"] == batch["files_completed"] == 335
    assert len(batch["per_work"]) == 335
    assert batch["rows"] == batch["labeled"] + batch["abstentions"]
    assert realtime["filesRequested"] == realtime["filesParsed"] == 335
    assert realtime["coreChecks"] == realtime["coreMatches"]
    checks = realtime["checks"]
    for name in (
        "expectedMidiCount", "allMidiParsed", "singleCanonicalEngineSource",
        "realtimeAdapterSharedCoreParity", "everyTokenHasConcurrentMultimodalRecord",
        "oneToOneTokenLinkIds", "eegSnapshotWithin50Ms", "cardioSnapshotWithin1000Ms",
        "behaviorSnapshotWithin250Ms", "subSecondLatencyAllTokens",
    ):
        assert checks[name] is True, name
    assert realtime["matrixValidation"]["ok"] is False
    sums = Path("results/SHA256SUMS").read_text(encoding="utf-8").splitlines()
    for line in sums:
        expected, relative = line.split("  ", 1)
        actual = hashlib.sha256(Path(relative).read_bytes()).hexdigest()
        assert actual == expected, relative
    print("PASS: manifest, summaries, targeted realtime checks, and published artifact hashes verified")
    print("DISCLOSED: the separate harmony-matrix self-test did not pass; see the public report")


if __name__ == "__main__":
    main()

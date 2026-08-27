# musWM × When-in-Rome 335 validation

This repository contains the public, engine-independent verification package for the 335-score technical validation reported in the accompanying manuscript. The score source is [When-in-Rome](https://github.com/MarkGotham/When-in-Rome). The tested selection is fixed by `corpus_manifest.csv`, including one SHA-256 digest per input score.

The proprietary musWM engine is **not** included. Re-running the analysis requires an authorized musWM HTTP service implementing `POST /api/analyze/muswm`, or a compatible black-box adapter. Published outputs, counts, schema conformance, file coverage, and hashes can be verified without the engine.

## Verify the published run

```bash
python verify_results.py
```

## Re-run with an authorized local service

```bash
python run_analysis.py --corpus /path/to/musicxml_all --api-url http://127.0.0.1:8765/api/analyze/muswm
python verify_results.py --results rerun/batch_summary.json --manifest corpus_manifest.csv
```

The runner uploads only score files from the user-specified directory and stores returned analysis rows locally. It contains no harmonic-analysis implementation.

## Reproducibility boundary

- Publicly reproducible: corpus identity, output integrity, row counts, label/abstention counts, per-work coverage, and published summary consistency.
- Reproducible with an authorized musWM runner: full batch inference on all 335 scores.
- The accelerated real-time parity test uses the same private engine through its batch and causal real-time adapters. Its aggregate report and hashes are published; the engine source is not.

See `METHODS.md` for the protocol and `LICENSE` for the code license. Corpus files remain governed by the upstream project and are not redistributed here.

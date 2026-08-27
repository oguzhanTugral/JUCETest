# Validation protocol

1. Enumerate exactly 335 `.mxl` scores in lexical filename order.
2. Record SHA-256 for every source file in `corpus_manifest.csv`.
3. Submit each score independently to the musWM batch endpoint and retain the returned rows.
4. Convert the same scores to MIDI with MuseScore Studio and replay them deterministically through the causal real-time adapter.
5. For every emitted token, compare Roman numeral, root pitch class, chord code, and analyzed pitch-class set with the shared batch core.
6. Summarize parsing coverage, emitted tokens, parity checks, multimodal record completeness, and processing latency.
7. Hash all published result artifacts and verify them in continuous integration.

The replay uses deterministic test streams to exercise record linkage and software timing. It is distinct from the separately reported recordings acquired with an eight-channel EEG system, a chest-strap cardiovascular sensor, facial-expression measures, and behavioral measures.

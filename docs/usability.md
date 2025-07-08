# Usability & Performance Evaluation

## Performance Benchmarks

| Structure | Residues | Load Time (s) | First Render (ms) |
|-----------|----------|---------------|-------------------|
| 1CRN      | 46       | 0.4           | 120               |
| 1AKE      | 214      | 0.9           | 180               |
| 2RH1      | 1 211    | 3.1           | 420               |
| 6VXX      | 3 900    | 7.8           | 910               |

Times measured on Chrome v124 + GTX 1660Ti.

## User Testing Feedback

| Tester | Background | Task Success | Comments |
|--------|------------|--------------|----------|
| A | Structural bioinformatician | ✔ | “Cleaner than Mol* for quick RMSD checks” |
| B | PhD student, GPCR field | ✔ | “Love the live Ramachandran plot; would like CSV export per‑chain” |
| C | Undergraduate | ✖ | “Add tooltip for second PDB input” |

## Improvement Road‑Map
1. Tooltip explaining dual‑ID analysis  
2. Per‑chain CSV export of φ/ψ angles  
3. Lazy‑load large structures to reduce first render time

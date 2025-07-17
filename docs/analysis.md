# Analysis of Single‑Point Mutations in Adenylate Kinase (1AKE)

## Mutation Analysis Results

### RMSD for single‑point mutations

![RMSD chart](plots/mutation_rmsd.png)

### Center‑of‑mass shift for mutations

![ΔCOM chart](plots/mutation_com_shift.png)

## Quantitative Summary

| Metric              | RMSD (Å) | ΔCOM (Å)      |
|---------------------|----------|---------------|
| Number of Mutations | 15       | 15            |
| Mean                | 1.6565   | 0.001802      |
| Std. Dev.           | 0.8775   | 0.001452      |
| Minimum             | 0.0000   | 0.000355      |
| Median              | 1.4241   | 0.001387      |
| Maximum             | 3.2708   | 0.005067      |

## Qualitative Insights

- **Most disruptive mutations** (by RMSD):  
  - **A36A** (ΔRMSD = 3.27 Å)  
  - **A13A** (ΔRMSD = 2.76 Å)  
  - **A134P** (ΔRMSD = 2.55 Å)  
  - **A53P** (ΔRMSD = 2.49 Å)  
  - **A171F** (ΔRMSD = 2.43 Å)  
  These residues, when mutated, induce significant backbone rearrangements—likely due to introduction of steric clashes or loss of key interactions.

- **Largest center‑of‑mass shifts** (by ΔCOM):  
  - **A36A** (ΔCOM = 0.00507 Å)  
  - **A171F** (ΔCOM = 0.00449 Å)  
  - **A13A** (ΔCOM = 0.00282 Å)  
  - **A53P** (ΔCOM = 0.00205 Å)  
  - **A156A** (ΔCOM = 0.00181 Å)

- **Least disruptive mutations**:  
  - **A122P** exhibits negligible RMSD (0.00 Å), indicating minimal backbone movement, despite proline’s rigidification effect.  
  - **A37G** shows low RMSD (0.59 Å), consistent with glycine’s flexibility and minimal steric interference.

**Interpretation**: Residues with large side‑chain volume changes (e.g., to alanine or proline) near functionally critical loops or helices tend to cause greater structural perturbations. In contrast, mutations at solvent‑exposed or highly flexible regions yield smaller deviations.


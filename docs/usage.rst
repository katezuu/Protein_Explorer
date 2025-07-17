Usage Guide
===========

Running the Web App
-------------------

1. Activate your virtual environment (if not already active):

   .. code-block:: bash

      source .venv/bin/activate

2. Start the Flask server:

   .. code-block:: bash

      python app.py

3. Open your browser to:

   .. code-block:: none

      http://localhost:5000

4. Enter a 4‑character PDB ID and click **Analyze**.

Analyzing Single‐Point Mutations
-------------------------------

1. On the results page, select a chain and residue number.
2. Enter the original and mutated one‐letter amino acids.
3. Click **Analyse Mutation**.
4. View RMSD, center‐of‐mass shift, and see the mutated residue highlighted.

Comparing Two Proteins
----------------------

On the home page, provide two PDB IDs. The app will compute and display the RMSD between them.


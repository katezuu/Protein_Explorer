Usage
=====

Home Page
---------

.. image:: _static/home.png
   :alt: Home page
   :width: 600px
   :align: center

1. Enter one or two **PDB IDs** (e.g. ``1CRN`` or ``1CRN, 4HHB``).
2. Click **Analyse** – the server fetches the PDB files,
   parses secondary-structure information and displays the first model.

Interactive Viewer
------------------

.. image:: _static/viewer.png
   :alt: 3-D viewer
   :width: 600px
   :align: center

* **Left mouse** – rotate, **wheel** – zoom, **right mouse** – pan
* Toggle representation in the sidebar: *Cartoon*, *Surface*, *Ball & Stick*
* Hover any residue to see its chain ID and residue number.

Mutation Analysis
-----------------

.. image:: _static/mutation.png
   :alt: Mutation highlighted
   :width: 600px
   :align: center

1. Pick a residue from the drop-down list.
2. Select the replacement amino acid.
3. Press **Analyse Mutation** – mutated residue is highlighted, and metrics
   (RMSD, centre-of-mass shift) appear in the side panel.

Exporting Results
-----------------

* **PNG** – save a high-resolution screenshot of the current viewport
* **CSV** – download residue-level hydrogen-bond counts and dihedral angles
* **JSON** – full atomic coordinates of the parsed model


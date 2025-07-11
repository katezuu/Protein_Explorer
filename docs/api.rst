API Reference
=============

``/api/metrics/<pdb_id>``
-------------------------

Returns atom coordinates, secondary-structure assignment and basic metrics.

 :Method: ``GET``
 :URL param: ``pdb_id`` – 4-letter PDB identifier

**Example request**

.. code-block:: bash

   curl -L https://katezuu.github.io/Protein_Explorer/api/metrics/1CRN

**Example response (truncated)**

.. code-block:: json

   {
     "model": 0,
     "chains": ["A"],
     "atoms": [
       {
         "serial": 1,
         "name": "N",
         "resSeq": 1,
         "resName": "THR",
         "x": 22.517,
         "y": 30.460,
         "z": 27.347
       }
     ],
     "phi_psi": [
       {
         "resSeq": 2,
         "phi": -60.1,
         "psi": -45.7
       }
     ]
   }

``/api/mutation_metrics`` (POST)
--------------------------------

Analyse a single-point mutation.

**Request body**

.. code-block:: json

   {
     "rmsd": 1.37,
     "com_shift": 0.82,
     "highlight": [
       [2.5, 8.4, -1.3]
     ]
   }

**Response**

.. code-block:: json

   {
     "rmsd": 1.37,
     "com_shift": 0.82,
     "highlight": [[2.5, 8.4, -1.3], [ ... ]]
   }

All coordinates are in ångströms (Å).

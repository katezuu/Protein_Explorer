API Reference
=============

.. http:get:: /api/metrics/<pdb_id>

   Retrieve atomic coordinates and basic metrics for a given PDB entry.

.. http:post:: /api/mutation_metrics

   :json body: ``{ pdbId, chain, residueNumber, originalAA, mutatedAA }``
   :>json title: MutationAnalysis

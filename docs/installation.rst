Installation
============

Prerequisites
-------------

- Python 3.8 or higher
- Git
- (Optional) virtualenv

Local Installation
------------------

#. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/katezuu/Protein_Explorer.git
      cd Protein_Explorer

#. Create and activate a virtual environment:

   .. code-block:: bash

      python3 -m venv .venv
      source .venv/bin/activate      # On Windows: .venv\Scripts\activate

#. Install Python dependencies:

   .. code-block:: bash

      pip install --upgrade pip
      pip install -r requirements.txt


Docker (Recommended)
------------------
Pull and run the Docker image:

   .. code-block:: bash

      docker pull katezu/protein-explorer:latest
      docker run -d -p 5000:5000 katezu/protein-explorer:latest

Then open your browser at: http://localhost:5000
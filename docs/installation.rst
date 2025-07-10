Installation
============

The project can be installed **from source** for local development,
or **via Docker** for a reproducible production setup.

From source
-----------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/katezuu/Protein_Explorer.git
      cd Protein_Explorer

2. Create a virtual environment and install dependencies:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate           # Windows: .venv\\Scripts\\activate
      pip install -r requirements.txt

3. Launch the Flask server:

   .. code-block:: bash

      flask --app app run    # default at http://127.0.0.1:5000

Docker
------

Build and run in one command:

.. code-block:: bash

   docker compose up --build

* `app` listens on **http://localhost:8000**
* hot reload is enabled in development mode

To rebuild only the backend image after code changes:

.. code-block:: bash

   docker compose build backend

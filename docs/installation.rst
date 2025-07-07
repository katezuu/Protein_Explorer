Installation
============

The project can be installed **from source** or **via Docker**.

From source
-----------

.. code-block:: bash

   git clone https://github.com/your-org/Protein_Explorer.git
   cd Protein_Explorer
   pip install -r requirements.txt
   flask run

Docker
------

.. code-block:: bash

   docker build -t protein-explorer .
   docker run -p 80:5000 protein-explorer

The application will be available at http://localhost (port 80).

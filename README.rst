discotech
=========

python library to help dealing with everything regarding social media
providers

homepage: https://www.discoapi.com/products/discotech.html

you can find full docs here: https://www.discoapi.com/discotech/docs

installation
============

.. code:: bash

    pip install discotech

requirements:
=============

-  python > 2.6
-  requests
-  requests-oauth

installation from source:
=========================

.. code:: bash

    python setup.py install

unit tests:
===========

first add your credentials to tests/testCredentials.json

.. code:: bash

    python setup.py test

creating docs:
==============

.. code:: bash

    epydoc -v discotech -o docs

note that you have to have epydoc installed (pip install epydoc)

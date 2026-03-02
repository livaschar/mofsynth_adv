Help to install mofid module
============================

Run the following commands in a Debian system:

.. code-block:: shell

    apt-get -y install default-jre rapidjson-dev openbabel wx3.2-headers libxml2-dev libcairo2-dev libwxgtk3.2-dev

Cloning the Repository
----------------------

Follow these steps to clone the repository:

.. code-block:: shell
    
    mkdir mofid_module
    cd mofid_module
    git clone https://github.com/snurr-group/mofid.git
    cd mofid
    

Editing the Source Code (Not always needed, depends on the system)
-----------------------

Make the following modification to the source code:

.. code-block:: shell

    vim openbabel/include/openbabel/obutil.h

Write **#include <ctime>** in line 47. Make sure to save the file before exit.

Finalizing the Installation
---------------------------

Complete the installation with these commands:

.. code-block:: shell

    make init
    python3 set_paths.py
    pip install .

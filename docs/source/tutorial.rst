.. highlight:: python

|:rocket:| Tutorial
===================

MOFSynth-ADV via Python
----------

If you want to run MOFSynth-ADV via Python, check the `examples folder <https://github.com/livaschar/mofsynth_adv/tree/main/examples>`_.

MOFSynth-ADV via CLI
----------

As stated in :ref:`advantages`, all you need is a ``.cif`` file!

If you don't have one |:point_right:| :download:`example.cif<down/example.cif>`
or try MOFSynth-ADV in a mini database |:point_right:| :download:`example_database.zip<down/example_database.zip>`

First, create a directory for the tutorial:

    .. code-block:: console

        $ mkdir mofsynth_tutorial
        $ cd mofsynth_tutorial

Next, create a directory to store the CIF files:

    .. code-block:: console

        $ mkdir cifs_folder

The final structure should look like this

.. code-block:: text
   
   cifs_folder/
   └── example.cif

Before running the workflow, make sure your Slurm settings are configured correctly.
MOFSynth-ADV uses a global SLURM template file located at ``~/.mofsynth/slurm_template.sh``.
If you have never run the tool before, this file will be automatically created with default settings the first time you execute a job. You can edit this file to adjust the number of tasks, cpus, time limits, or partition to match your cluster's requirements.

You are ready to run the tool using the following command. The default calculator is ``xtb`` and the default optimizer is ``lbfgs``. You can also specify the fragmentation time limit using the ``--time`` flag:

    .. code-block:: console

        $ mofsynth_adv exec cifs_folder --time 20

You can view available options (such as changing the calculator or optimizer) by running ``mofsynth_adv --help``.

After the jobs are submitted to the queue, you can check the progress using the ``verify`` function:

    .. code-block:: console

        $ mofsynth_adv verify cifs_folder

Once all linker optimizations have completed, compile the final results:

    .. code-block:: console

        $ mofsynth_adv report cifs_folder

Hurray! An **.xlsx file** containing the final synthesizability evaluation results will be created in your working directory.



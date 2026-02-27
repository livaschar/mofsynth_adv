|:keyboard:| CLI Arguments
==========================

MOFSynth-ADV uses a Command Line Interface (CLI) to orchestrate its synthesizability evaluation. You can display all available options at any time by running:

.. code-block:: console

    $ mofsynth_adv --help

Function
--------

The first positional argument is the ``function`` you wish the tool to perform:

- ``exec``: Executes the initial evaluation, extracts linkers, and submits geometry optimizations.
- ``verify``: Checks which geometry optimization runs (from ``exec``) have successfully converged.
- ``report``: Compiles and exports the compiled syntheziability results into an Excel file.

Configuration Options
---------------------

``--calc``
~~~~~~~~~~
Computational engine used for energy evaluations.

* **Choices**: ``xtb`` (GFN2-xTB), ``mace_off``, ``mace_mp``.
* **Default**: ``xtb``

``--opt``
~~~~~~~~~
Geometry optimization algorithm controlling the structural relaxation of the isolated linkers.

* **Choices**: ``sella``, ``fire``, ``bfgs``, ``lbfgs``.
* **Default**: ``lbfgs``

Limits & Constraints
--------------------

``--time``
~~~~~~~~~~
**The fragmentation time limit in seconds.** 

When MOFSynth-ADV parses the ``.cif`` file and extracts the building blocks of the MOF into isolated clusters (linkers and nodes), the graph exploration procedure can sometimes diverge and run endlessly for topologically complex, heavily intertwined, or severely defective input structures. 
This hard time limit prevents the process from hanging your machine indefinitely on a single problematic MOF structre.

* **Default**: ``20`` (seconds)


``--supercell``
~~~~~~~~~~~~~~~
**The maximum length for each edge of the unit cell in Angstroms (Å).**

This limit determines whether a supercell should be created based on the dimensions of the original unit cell inside the ``.cif`` file. If the dimensions of the original unit cell are deemed too small to properly represent the chemical environment and coordination, a supercell is dynamically generated. 
If not provided, the supercell creation will not be constrained by a specific maximum size. However, providing a sensible limit helps significantly with computational speed and guarantees the geometry convergence doesn't explode due to massive system sizes.

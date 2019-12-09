Installation
------------

The GRANTA plugin depends on external libraries provided by GRANTA:
- MIScriptingToolkit: a low level access to the GRANTA MI database
- granta: a higher level interface to the same database, providing a more user friendly API.

Both these libraries are available from GRANTA.
To install them, and this plugin, you must:

- be in the edm bootstrap environment (generally called edm), using ``edm shell``.
- enable the deployment edm environment (generally called force-py36) using ``edm shell -e force-py36``.
- Go in the MIScriptingToolkit library directory, and run ``python setup.py install``.
- Go in the granta library directory, and run ``pip install .``
- Leave the edm deployment environment (a simple ``exit`` will do), to go back to the bootstrap edm environment.
- Access the plugin directory, and run ``python -m ci install``.



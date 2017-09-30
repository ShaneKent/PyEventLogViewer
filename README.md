# PyEventLogViewer

# Installation Instructions
To install, use `$ pip install --ugrade .` from the repository root. This command must be run in an elevated context in order for scripts to be properly added to the path.

To run, use `$ evt_viewer.py`.

# Development Instructions
Before running anything, you should always run `$ pip install --upgrade .`. This ensures that the python runtime is using the latest version of the library.

**Untested**: To avoid running in an elevated context, you can run `$ pip install --user --upgrade .`. This does not add scripts to the path, but it should upgrade the libraries used by the python runtime. 

**Note**: If you are using a sufficiently advanced editor, you can test without upgrading the installed package version. In PyCharm, for example, you can mark `winlogtimeline` as a sources root and `config` as a resource root, and create a run configuration to automatically add them to the path when running a script in `bin`.
import sys,os
from cx_Freeze import setup, Executable

#To build: Go to directory on the cmd line. and do:  python setup.py build

base = None
if sys.platform == "win32":
    base = "Win32GUI"


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

includefiles = []
includes = []
excludes = ['Tkinter']
packages = ['gui.py']


setup(
    name = 'myapp',
    version = '0.2',
    description = 'A general enhancement utility',
    author = 'lenin',
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('gui.py')]
)


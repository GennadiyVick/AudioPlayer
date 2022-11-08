Spruce. 
AudioPlayer based on libvlc for python and pyqt5 for gui.

Required:
To run the program, you need python itself and the installed PyQt5 and libvlc modules.


Installing python and PyQt5 and libvlc modules.
**********************************************

MS Windows: ============================
You can download the distribution from https://www.python.org/downloads/ 
and double-click the installation

after installation, you need to install the PyQt5 and libvlc modules
to do this in the console enter 

python -m pip install pyqt5
python -m pip install python-vlc

the program will download and install the module.
To run this program, you must enter in the console

python program_path\AudioPlayer.py

You can also create a launch shortcut on the desktop.
To run from a shortcut, use pythonw instead of python

pythonw program_path\AudioPlayer.py

Linux: ========================
For the program to work in Linux, you need to use python version 3 or higher.
Most distributions have python preinstalled and you don't need to download and install it, 
you just need to install the PyQt5 module.
If you do not have python3 installed, you can install it using your package manager, 
for example, in distributions based on Debian, it is installed like this:

sudo apt-get install python3

To install the module in the console, enter
pip3 install pyqt5
pip3 install python3-vlc
modules will be automatically downloaded and installed.
The program starts like this:

python3 program_path/AudioPlayer.py

You can also add permission to run the script and run it by double clicking
*************************************************

Author: Roganov G.V. roganovg@mail.ru



*************************************************



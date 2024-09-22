# Audio player
## Based on the BASS library
https://www.un4seen.com/bass.html

![screenshot](https://gitlab.com/GennadiyVick/audioplayer/raw/master/image.png)
## Required:
To run the program, you need BASS library (see in libs archive for your OS), python itself and the installed PyQt5 module.

### MS Windows:
You can download the distribution from [python.org](https://www.python.org/downloads/) and double-click the installation
after installation, you need to install the `PyQt5` module, to do this in the console enter 
```console
python -m pip install pyqt5
```
the program will download and install the module.
Then copy bass.dll to AudioPlayer.py directory from libs.zip/windows/x64, if you need support m4a and acc, wma formats see such libraryes in libs.zip/windows/aac and wma

To run this program, you must enter in the console
```console
python program_path\AudioPlayer.py
```
You can also create a launch shortcut on the desktop.
To run from a shortcut, use `pythonw` instead of `python`
```console
pythonw program_path\AudioPlayer.py
```

### Linux:
For the program to work in Linux, you need to use python version 3 or higher.
Most distributions have python preinstalled and you don't need to download and install it, 
you just need to install the `PyQt5` module.
If you do not have python3 installed, you can install it using your package manager, 
for example, in distributions based on Debian, it is installed like this:
```console
sudo apt-get install python3
```
To install the module in the console, enter
```console
sudo apt-get install python3-pyqt5
```
module will be automatically downloaded and installed.
Then copy libbass.so to AudioPlayer.py directory from libs.zip/linux/bass/x86_64, if you need support m4a and acc format see library in libs.zip/linux/aac/x86_64/ and copy it also

The program starts like this:
```console
python3 program_path/AudioPlayer.py
```
You can also add permission to run the script and double-click to run it, as well as create a desktop shortcut.


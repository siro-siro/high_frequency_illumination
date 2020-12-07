# ScriptCapture
Captureing script for High-frequency illumination.
This script captures an image for each projection patterns.

There are two options depending on your camera.
* If you use a DSLR camera such as Nikon, Canon, Sony, etc., you can use ```ScriptCaptureDSLR.py```.
* If you use a camera made by Point Gray, you can use ```ScriptCapturePgr.py```.

## Usage
1. Prepare images for projection by yourself, or use ```generate_checker_board.py```. Please note that all images are saved in a directory (e.g. ```./illuminations/```) and it must not include other files.
 ```
 mkdir illuminations && cd illuminations
 python ../generate_checker_board.py
 cd ..
 ```

2. Use this script. All captured images are saved as the same name of the illumination file.
 ```
 mkdir captures
 python ScriptCapture[Camera].py
 ```
  Illumination and output directories are selectable. Please see ```-h``` option. 
  
  Tips: Sometimes, projection time lag problem will occur. In that case, ```--dummy``` option can mitigate this problem.
 
3. Finally, post process captured images yourself, or use ```separate_direct_global.py```.
 ```
 python separate_direct_global.py -d captures
 eog captures/direct.png
 ```

## Dependencies
* FlyCapture2 SDK

    Download installer from Point Gray website and install followed by their README.
    Please note, this SDK also depends on other packages.

* pyflycapture2

  FlyCapture2 SDK python wrapper.
  ```
  git clone https://github.com/jordens/pyflycapture2.git
  cd pyflycapture2
  sudo python setup.py install
  ```
  Note that this package also depends on other packages such as cython.
  ```
  sudo pip install cython
  ```
  See readme for the detail here: https://github.com/jordens/pyflycapture2

* dcraw

  Though dcraw can be installed via apt-get system, we recommend to build from the source.
  Download the source code from its [website](https://www.cybercom.net/~dcoffin/dcraw/), compile, and install as:
  ```
  wget https://www.cybercom.net/~dcoffin/dcraw/dcraw.c
  gcc -o dcraw -O4 dcraw.c -lm -DNODEPS
  sudo cp -p dcraw /usr/local/bin
  ```

* imagemagick, OpenCV, gphoto2, and PyQt4

  In Ubuntu 14.04, these packages can be installed as:
  ```
  sudo apt-get install imagemagick libopencv-dev python-opencv python-qt4 gphoto2
  ```

## Notes
 Copyright (c) 2016, Optical Media Interface Lab., NAIST, Japan,
   coded by Kenichiro Tanaka, 2013-2016.

   If you use our codes for publication, please cite the following paper.
   * K. Tanaka, Y. Mukaigawa, Y. Matsushita, Y. Yagi, "Descattering of Transmissive Observations using Parallel High-frequency Illumination", IEEE International Conference on Computational Photography, 2013.

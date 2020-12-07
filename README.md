# Tools for high frequency illumination
Includes pattern generator and post process scripts.

* ScriptCapture

  Automatic projection and capture scripts. Please refer [ScriptCapture/README.md](./ScriptCapture/README.md) for the detail.

* generate_checker_board.py

  Generates projection patterns.
  Image size, pattern size, shift amount, and color are adjustable. See usage by ```-h``` option.

* separate_direct_global.py

  Separates into direct and global components from captured images.


# Dependencies
These scripts depend on python, numpy, and opencv.
For Ubuntu 14.04, these packages can be installed as:
```
sudo apt-get install libopencv-dev python python-numpy python-opencv
```
If you use ScriptCaptures, other packages are required. See also [ScriptCapture/README.md](./ScriptCapture/README.md).

# Notes
This program implements the paper;

* S. Nayar et al. "Fast Separation of Direct and Global Components of a Scene using High Frequency Illumination", SIGGRAPH 2006.

If you use our codes for publication, please cite the following paper.

* K. Tanaka, Y. Mukaigawa, Y. Matsushita, Y. Yagi, "Descattering of Transmissive Observations using Parallel High-frequency Illumination", IEEE International Conference on Computational Photography, 2013.

You can use our codes under MIT license.

# For Japanese
[こちらのページ](http://www.am.sanken.osaka-u.ac.jp/~tanaka/projects/phfi-jp.html)で簡単な解説がご覧になれます．

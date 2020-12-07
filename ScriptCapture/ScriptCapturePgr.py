#!/usr/bin/env python
'''
 ScriptCapturePgr.py
 
 Feb. 2016.
  coded by Kenichiro Tanaka

 Dependencies
  imagemagick, FlyCapture2 SDK, pyflycapture2, OpenCV, PyQt4
'''

import argparse
from subprocess import Popen, check_call, call
import os
import signal
import commands
import numpy as np
import cv2
import flycapture2 as fc2
import time
import sys
from glob import glob
import shutil

def kill_display():
    pid_display = commands.getoutput('ps -ax | grep SC_display_window').split()[0]
    call(['kill', pid_display])

def __control_c_stop(no, fr):
    kill_display()
    raise KeyboardInterrupt

# Parse program arguments
parser = argparse.ArgumentParser(description='Repeat displaying pattern and captureing its image.')
parser.add_argument('--version', action='version', version="%(prog)s 1.0.0")
parser.add_argument('-s', '--shutter', type=float, default=500., help="Shutter time of the camera (ms).")
parser.add_argument('-g', '--gain', type=float, default=0., help="Gain of the camera.")
parser.add_argument('--dummy', type=int, default=0, help="# of dummy capture. PG cameras sometimes remain buffers of former pattern.")
parser.add_argument('--average', type=int, default=1, help="# of captures for average per each pattern.")
parser.add_argument('--roi', type=int, nargs=4, default=(0, 0, 800, 600), metavar=("X", "Y", "width","height"), help="Region of interest.")
parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing output directory.')
parser.add_argument('illumination', nargs='?', default='illuminations/', help='Directory where projection images are stored.')
parser.add_argument('output', nargs='?', default='captures/', help='Directory where captured images are going to be stored.')
args = parser.parse_args()

# Check directory
if not os.path.exists(args.output):
    os.makedirs(args.output)
else:
    if not args.force:
        print 'Terminated: Output directory already exists. Use -f option to ignore and overwrite.'
        sys.exit(0)
    shutil.rmtree(args.output, ignore_errors=True)
    os.makedirs(args.output)


# Load image filenames
files = [os.path.basename(x) for x in glob(os.path.join(args.illumination, '*'))]

# Start display
pid = os.fork()
if pid == 0:
#    pargs=['python', 'SC_display_window.py', '-f', '-t'] # debug
    pargs=['python', 'SC_display_window.py'] # debug
    p = Popen(pargs)
    sys.exit()    
signal.signal(signal.SIGINT, __control_c_stop) # kill display in case of Ctrl-C termination.
time.sleep(.1)

try:
    # Connect to the camera
    c = fc2.Context()
    if c.get_num_of_cameras == 0:
        print 'There are no cameras detected.'
        kill_display()
        sys.exit()
    c.connect(*c.get_camera_from_index(0))
    buf = fc2.Image()
    
    # Initialize the camera
    #   TODO: set appropriate mode and pixel format depending on connected camera model.
    c.set_format7_configuration(7, args.roi[0], args.roi[1], args.roi[2], args.roi[3], fc2.PIXEL_FORMAT_MONO16)
    #             (type             , present, on_off, auto , abs_c, one_p, val         , val_a, val_b)
    c.set_property(fc2.FRAME_RATE   , True   , False , False, True , False, 1.          , 0    , 0    )
    c.set_property(fc2.AUTO_EXPOSURE, True   , False , False, False, False, 0.          , 0    , 0    )
    c.set_property(fc2.BRIGHTNESS   , True   , True  , False, True , False, 0.          , 0    , 0    )
    c.set_property(fc2.SHARPNESS    , True   , True  , False, False, False, 0.          , 0    , 0    )
    c.set_property(fc2.GAMMA        , True   , True  , False, True , False, 1.          , 0    , 0    )
    c.set_property(fc2.GAIN         , True   , True  , False, True , False, args.gain   , 0    , 0    )
    c.set_property(fc2.SHUTTER      , True   , True  , False, True , False, args.shutter, 0    , 0    )
    #   TODO: set white balance in case of color cameras...
    
    # Move stage and capture
    for f in files:
        # display an image
        print 'Projection:', f
        pattern = os.path.join(args.illumination, f)
        output = os.path.join(args.output, f)
        iargs=['display', '-window', 'SC_display_window.py', pattern]
        check_call(iargs)
        # capture dummy image
        c.start_capture()
        for i in range(args.dummy):
            sys.stdout.write('\r    dummy:' + str(i+1))
            sys.stdout.flush()
            c.retrieve_buffer(buf) 
        # capture images, average, and save.
        img = np.zeros((args.roi[3], args.roi[2]))
        for i in range(args.average):
            sys.stdout.write('\r    capture:' + str(i+1) + '    ')
            sys.stdout.flush()
            c.retrieve_buffer(buf) 
            img += np.array(buf)
        img /= args.average
        c.stop_capture()
        cv2.imwrite(output, np.uint16(img))
        print '--> saved.'
            
        
    #os.kill(pid, signal.SIGTERM)
    kill_display()
    c.disconnect()
except:
    kill_display() # in case of flycapture fault.
    raise
    

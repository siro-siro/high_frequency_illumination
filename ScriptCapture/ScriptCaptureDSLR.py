#!/usr/bin/env python
'''
 ScriptCapturePgr.py
 
 Feb. 2016.
  coded by Kenichiro Tanaka

 Dependencies
  imagemagick, dcraw, gphoto2, PyQt4
'''

import argparse
from subprocess import Popen, check_call
import os
import signal
import commands
import DSLR
import time
import sys
from glob import glob
import threading
import shutil

def kill_display():
    pid_dw = commands.getoutput('ps -ax | grep SC_display_window').split()[0]
    check_call(['kill', pid_dw])

def __control_c_stop(no, fr):
    kill_display()
    raise KeyboardInterrupt

# Parse program arguments
parser = argparse.ArgumentParser(description='Repeat displaying pattern and captureing its image.')
parser.add_argument('--version', action='version', version="%(prog)s 1.0.0")
parser.add_argument('-s', '--shutter', type=int, default=23, help="Shutter time of the camera.")
parser.add_argument('-g', '--gain', type=int, default=0, help="Gain (ISO) of the camera.")
#parser.add_argument('--dummy', type=int, default=0, help="# of dummy capture. PG cameras sometimes remain buffers of former pattern.")
#parser.add_argument('--average', type=int, default=1, help="# of captures for average per each pattern.")
#parser.add_argument('--roi', type=int, nargs=4, default=(0, 0, 800, 600), metavar=("X", "Y", "width","height"), help="Region of interest.")
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
    # Initialize the camera
    #   TODO: convert millisecond or ISO value to gphoto2 parameter index. 
    #         In current implementation, users must specify these parameters by gphoto2 index.
    #         See also, DSLR.print_configurable_properties() and DSLR.print_property()
    DSLR.set_ISO(args.gain)
    DSLR.set_shutter(args.shutter)
    
    # Move stage and capture
    for f in files:
        #
        fn, ext = os.path.splitext(f)
        raw_fn = os.path.join(args.output, fn + '.nef') # TODO: Nikon cameras only. To use other maker's camera, appropriate extention should be specified.
        # display an image
        print 'Projection:', f
        pattern = os.path.join(args.illumination, f)
        output = os.path.join(args.output, f)
        iargs=['display', '-window', 'SC_display_window.py', pattern]
        check_call(iargs)
        # capture dummy image
        DSLR.capture_and_save(raw_fn)
        print '--> raw saved.',
        convert_thread = threading.Thread(target=DSLR.raw2png, args=[raw_fn, output])
        convert_thread.start()
        print '--> conversion queued.'
        
    #os.kill(pid, signal.SIGTERM)
    kill_display()
    print 'Wait for queued process finished.'
except:
    kill_display() # in case of flycapture fault.
    raise
    


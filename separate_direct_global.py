#!/usr/bin/python
'''
 separate_direct_global.py

 Copyright(c) Photometry Group in Prof. Yagi's lab., ISIR, Osaka University.
     Sep. 2013, Kenichiro Tanaka


 Separate into direct and global components.

 
 Notes
 -----
 1. All images in the directory are loaded for separation.
 2. Black bias is automatically enabled if there is 'black.png'.
 3. Normal illumination is automatically ignored if there is 'white.png'.
'''

import argparse
import glob
import sys
import numpy as np
import cv2

# Parse program arguments
parser = argparse.ArgumentParser(description='Separate into direct and global components.')
parser.add_argument('-v', dest='max_min_output', default=False, action='store_true' , help="Outputs max and min images.")
parser.add_argument('-e', '--extension', default=".png", help="File extension of all images. default is .png")
parser.add_argument('-d', '--dir', default="./", help="Source images' directory. default is the current directory.");
parser.add_argument('-w', '--whiteout', default=False, action='store_true', help = "Processing mode of saturated pixel. If this flag is specified, direct component becomes white, otherwise becomes black.")
args = parser.parse_args()

# Variables
black_bias = False

# Get input filenames.
dir_name = args.dir
extension = args.extension
if not dir_name.endswith('/'):
	dir_name = dir_name + '/'
if not extension.startswith('.'):
	extension = '.' + extension
search_sequence = dir_name + "*" + extension
black_file = dir_name + "black" + extension
files = glob.glob(search_sequence)
if black_file in files:
	black_bias = True
	files.remove(black_file)
for excp in ['white', 'direct', 'global', 'max', 'min']:
    filename = dir_name + excp + extension
    if filename in files:
        files.remove(filename)

# If file does not exist, exit the program.
if len(files) == 0:
	print "No images..."
	sys.exit()

# Load images
img = cv2.imread(files[0], -1)
max_img = img
min_img = img
for filename in files:
	img = cv2.imread(filename, -1)
	max_img = np.maximum(max_img, img)
	min_img = np.minimum(min_img, img)

img_is_16bit = (max_img.itemsize != 1)

# If all images are satulated, direct image should be white?
if args.whiteout:
    if img_is_16bit:
        min_img[min_img==65535] = 0
    else:
        min_img[min_img==255]=0

# Separate into direct and global components
if black_bias:
    # subtract black bias with underflow prevention
    black_img = cv2.imread(black_file, -1)
    max_img = np.maximum(max_img - black_img, 0)
    min_img = np.maximum(min_img - black_img, 0)
direct_img = max_img - min_img

# Prevent overflow
intensity_max = 65535.0 if img_is_16bit else 255.
global_img = np.minimum(2.0 * min_img, intensity_max)
if img_is_16bit:
    global_img = np.uint16(global_img)
else:
    gloabl_img = np.uint8(global_img)

# Save images
cv2.imwrite(dir_name + "direct" + extension, direct_img)
cv2.imwrite(dir_name + "global" + extension, global_img)
if args.max_min_output:
	cv2.imwrite(dir_name + 'max' + extension, max_img)
	cv2.imwrite(dir_name + 'min' + extension, min_img)


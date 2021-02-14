import pathlib
import argparse
import glob
import sys
import numpy as np
import cv2

import matplotlib.pyplot as plt


def separate_direct_global(*, max_min_output, extension, image_dir, whiteout, beta, mcolor):
    # Variables
    black_bias = False
    if not image_dir.endswith('/'):
        image_dir = image_dir + '/'
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Mean each pattern images
    dirs = [str(f) for f in pathlib.Path(image_dir).iterdir() if f.is_dir()]
    for d in dirs:
        search_sequence = d + "/*" + extension
        files = glob.glob(search_sequence)
        img = np.zeros_like(cv2.imread(files[0], -1)).astype(float)
        for f in files:
            img = img + cv2.imread(f, -1)
        img = img / len(files)
        filename = d.split("/")[-1]
        cv2.imwrite(image_dir + filename + extension, img)
        
    # Get input filenames.
    search_sequence = image_dir + "*" + extension
    black_file = image_dir + "black" + extension
    files = glob.glob(search_sequence)
    if black_file in files:
        black_bias = True
        files.remove(black_file)
    for excp in ['white', 'direct', 'global', 'max', 'min']:
        filename = image_dir + excp + extension
        if filename in files:
            files.remove(filename)
    
    # If file does not exist, exit the program.
    if len(files) == 0:
        print ("No images...")
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
    if whiteout:
        if img_is_16bit:
            min_img[min_img==65535]=0
        else:
            min_img[min_img==255]=0
    
    # Separate into direct and global components
    if black_bias:
        # subtract black bias with underflow prevention
        black_img = cv2.imread(black_file, -1)
        max_img = np.maximum(max_img - black_img, 0)
        min_img = np.maximum(min_img - black_img, 0)
        
    # Prevent overflow
    direct_img = np.minimum((max_img - min_img) / (1 - beta), mcolor)
    global_img = np.minimum(2.0 * (min_img - beta * max_img) / (1 - beta**2), mcolor)
    
    # Save images
    cv2.imwrite(image_dir + "direct" + extension, direct_img)
    cv2.imwrite(image_dir + "global" + extension, global_img)
    if max_min_output:
        cv2.imwrite(image_dir + 'max' + extension, max_img)
        cv2.imwrite(image_dir + 'min' + extension, min_img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Separate into direct and global components.')
    parser.add_argument('-v', dest='max_min_output', default=False, action='store_true', help="Outputs max and min images.")
    parser.add_argument('-e', '--extension', default=".png", help="File extension of all images. default is .png")
    parser.add_argument('-d', '--dir', default="./", help="Source images' directory. default is the current directory.");
    parser.add_argument('-w', '--whiteout', default=False, action='store_true', help="Processing mode of saturated pixel. If this flag is specified, direct component becomes white, otherwise becomes black.")
    parser.add_argument('-b', '--beta', default=0, help="Leakage to not illuminated fraction")
    parser.add_argument('-m', '--mcolor', nargs=3, default=(255, 255, 255), help="max color")
    args = parser.parse_args()
    separate_direct_global(max_min_output=args.max_min_output,
                           extension=args.extension, image_dir=args.dir,
                           whiteout=args.whiteout, beta=args.beta, mcolor=args.mcolor)

#!/usr/bin/env python
'''
 generate_checker_board.py

 Copyright(c) Photometry group in Yagi lab., ISIR, Osaka University.
     Sep. 2013, Kenichiro Tanaka
     modified: Jan. 2016, Kenichiro Tanaka

 Generate checkerboard for high frequency illumination
'''

import numpy as np
import cv2
#import Image # PIL can be used if you don't want to use Open CV.
import argparse
import sys

def generate_checker(h=720, w=1280, sqsize=9, color1=(0,0,0), color2=(255,255,255), offset_x=0, offset_y=0):
    '''
    Generate checkerboard image.
    
    Parameters
    ----------
    h : int, optional
        Image height.
    w : int, optional
        Image width.
    sqsize : int, optional
        Size of white and black squares.
    color1 : (int, int, int), optional
        Color of the 'black' square.
    color2 : (int, int, int), optional
        Color of the 'white' square.
    offset_x : int, optional
        Pattern offset for horizontal axis.
    offset_y : int, optional
        Pattern offset for vertical axis.
        
    Returns
    -------
    img : int(h, w, 3)
        Checkerboard image.
    '''
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.fromfunction(lambda y,x: (((y+offset_y)//sqsize) + ((x+offset_x)//sqsize)) % 2, (h,w))
    img[c==0]=color1
    img[c==1]=color2
    return img

def generate_stripex(h=720, w=1280, sqsize=9, color1=(0,0,0), color2=(255,255,255), offset_x=0):
    '''
    Generate stripex image.
    
    Parameters
    ----------
    h : int, optional
        Image height.
    w : int, optional
        Image width.
    sqsize : int, optional
        Size of white and black squares.
    color1 : (int, int, int), optional
        Color of the 'black' square.
    color2 : (int, int, int), optional
        Color of the 'white' square.
    offset_x : int, optional
        Pattern offset for horizontal axis.
    offset_y : int, optional
        Pattern offset for vertical axis.
        
    Returns
    -------
    img : int(h, w, 3)
        Stripe image.
    '''
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.fromfunction(lambda y,x: (x+offset_x) // sqsize % 2, (h,w))
    img[c==0]=color1
    img[c==1]=color2
    return img

def generate_stripey(h=720, w=1280, sqsize=9, color1=(0,0,0), color2=(255,255,255), offset_y=0):
    '''
    Generate stripey image.
    
    Parameters
    ----------
    h : int, optional
        Image height.
    w : int, optional
        Image width.
    sqsize : int, optional
        Size of white and black squares.
    color1 : (int, int, int), optional
        Color of the 'black' square.
    color2 : (int, int, int), optional
        Color of the 'white' square.
    offset_x : int, optional
        Pattern offset for horizontal axis.
    offset_y : int, optional
        Pattern offset for vertical axis.
        
    Returns
    -------
    img : int(h, w, 3)
        Stripe image.
    '''
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.fromfunction(lambda y,x: (y+offset_y) // sqsize % 2, (h,w))
    img[c==0]=color1
    img[c==1]=color2
    return img
	
def generate_sinusoid(h=720, w=1280, sqsize=9, color1=(0,0,0), color2=(255,255,255), phi=0):
    '''
    Generate sinusoid image.
    
    Parameters
    ----------
    h : int, optional
        Image height.
    w : int, optional
        Image width.
    sqsize : int, optional
        Size of white and black squares.
    color1 : (int, int, int), optional
        Color of the 'black' square.
    color2 : (int, int, int), optional
        Color of the 'white' square.
    phi : float, optional
        Pattern offset for horizontal axis.
        
    Returns
    -------
    img : int(h, w, 3)
        Sinusoid image.
    '''
    #img = np.zeros((h,w,3), dtype=np.uint8)
    #TODO
    print(color2[0])
    c = np.fromfunction(lambda y,x: 0.5+0.5*np.sin((x//sqsize)+np.sin(y//sqsize)+phi), (h,w))
    print(img[c])
    img[c]=img[c]*color2
    #img[c==0]=color1
    #img[c==1]=color2
    return img
	
if __name__ == '__main__':
    # Parse program arguments
    parser = argparse.ArgumentParser(description='Generate patterns')
    parser.add_argument('-t', '--btype', type=str, default="checker", help="Type of pattern. ('checker', 'stripex', 'stripey', 'sinusoid')")
    parser.add_argument('-s', '--size', type=int, nargs=2, default=(1280, 720), help="Image size.", metavar=("Width", "Height"))
    parser.add_argument('-q', '--sqsize', type=int, default=9, help="Square size of the pattern.")
    parser.add_argument('-f', '--shift', type=int, default=3, help="Shift amount.")
    parser.add_argument('-o', '--once', action='store_true', default=False, help="Generate only single pattern.")
    parser.add_argument('--color1', type=int, nargs=3, default=(0, 0, 0), help = "Background color.", metavar=("R","G","B"))
    parser.add_argument('--color2', type=int, nargs=3, default=(255, 255, 255), help = "Foreground color.", metavar=("R","G","B"))
    args = parser.parse_args()
    btype = args.btype
    (w, h) = args.size
    sqsize = args.sqsize
    step = args.shift
    color1 = args.color1
    color2 = args.color2

    x = 0
    y = 0
    fnum = 0
        
    #
    # white and black
    #
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.zeros((h, w))
    img[c==0]=color1
#    Image.fromarray(img, 'RGB').save('black.png')
    cv2.imwrite('black.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #c = np.ones((h, w)) * 255
    c = np.ones((h, w))
    img[c==1]=color2
#    Image.fromarray(img, 'RGB').save('white.png')
    cv2.imwrite('white.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    #
    # Shifting
    #
    if args.once:
        if btype == "checker":
            img = generate_checker(h, w, sqsize, color1, color2, 0, 0)
        elif btype == "stripex":
            img = generate_stripex(h, w, sqsize, color1, color2, 0)
        elif btype == "stripey":
            img = generate_stripey(h, w, sqsize, color1, color2, 0)
        elif btype == "sinusoid":
            print("Can't separate.")
#        pilImg = Image.fromarray(img, 'RGB')
#        pilImg.save(str(fnum)+'.png')
        cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        sys.exit(0)

    #
    # Shifting
    #
    if btype == "checker":
        while y < sqsize:
            x = 0
            while x < sqsize*2:
                img = generate_checker(h, w, sqsize, color1, color2, x, y)
#                pilImg = Image.fromarray(img, 'RGB')
#                pilImg.save(str(fnum)+'.png')
                cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                fnum += 1
                x += step
            y += step
    elif btype == "stripex":
        while x <= sqsize:
            img = generate_stripex(h, w, sqsize, color1, color2, x)
#            pilImg = Image.fromarray(img, 'RGB')
#            pilImg.save(str(fnum)+'.png')
            cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            fnum += 1
            x += step
    elif btype == "stripey":
        while y <= sqsize:
            img = generate_stripey(h, w, sqsize, color1, color2, y)
#            pilImg = Image.fromarray(img, 'RGB')
#            pilImg.save(str(fnum)+'.png')
            cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            fnum += 1
            y += step
    elif btype == "sinusoid":
        for x in range(4):
            img = generate_sinusoid(h, w, sqsize, color1, color2,  x*(2*np.pi/3))
#            pilImg = Image.fromarray(img, 'RGB')
#            pilImg.save(str(fnum)+'.png')
            cv2.imwrite(str(x)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
         

#!/usr/bin/env python
'''
gphoto2 samples
'''

import subprocess
import cv2
import numpy as np

def print_sammary():
    '''
    Print the sammary of detected cameras.
    '''
    subprocess.check_call(['gphoto2', '--summary'])
    
def print_configurable_properties():
    '''
    Print the configureable properties of detected cameras.
    '''
    subprocess.check_call(['gphoto2', '--list-config'])
    
def print_property(prop="/main/capturesettings/shutterspeed"):
    '''
    Print the property value
    
    Parameters
    ----------
    prop : string
        Property name of gphoto2.
        
    See also
    --------
    print_configurable_properties, set_property
    '''
    subprocess.check_call(['gphoto2', '--get-config='+prop])    
    
def set_property(prop="/main/capturesettings/shutterspeed", value=0):
    '''
    Print the property value
    
    Parameters
    ----------
    prop : string
        Proerty name of gphoto2.
    value : int
        Index of configurable property values.
        
    See also
    --------
    print_configurable_properties, print_property
    '''
    subprocess.check_call(['gphoto2', '--set-config='+prop+'='+str(value)])    
    
    
def print_all_files_in_camera():
    '''
    List all files in camera
    '''
    subprocess.check_call(['gphoto2', '--list-files'])
    
def capture_and_save(filename):
   '''
   Capture an image, download and save to 'filename', and remove it from the camera.
   Parameters
   ----------
   filename : string
       Output filename
   '''
   #check_call(['gphoto2', '--capture-image'])
   #check_call(['gphoto2', '--get-raw-data', '1', '--filename', filename])
   #check_call(['gphoto2', '--delete-file', '1', '-R'])
   subprocess.check_call(['gphoto2', '--capture-image-and-download', '--filename', filename])
   
def capture_and_save_bulb(filename, shutter=10):
   '''
   Capture an image, download and save to 'filename', and remove it from the camera.
   This is only works for 'M' (manual) mode and shutter time is set to 'bulb'.
   Maybe works only with Canon cameras... (I'm not sure)
   Parameters
   ----------
   filename : string
       Output filename
   shutter : float or int
       Shutter time in second
   '''
   subprocess.check_call(['gphoto2', '-B', str(shutter), '--capture-image-and-download', '--filename', filename])
   
def raw2png(raw, png):
    '''
    Convert raw image to png image
    Parameters
    ----------
    raw : string
        Raw filename
    png : string
        Output filename
    '''
    command = 'dcraw -4 -w -c ' + raw + ' | convert - ' + png
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()
    
def raw2png_resize(raw, png):
    '''
    Convert raw image to png image
    Parameters
    ----------
    raw : string
        Raw filename
    png : string
        Output filename
    '''
    command = 'dcraw -4 -w -c ' + raw + ' | convert - -resize 25% ' + png
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    subprocess.check_call(['rm', '-f', raw])
    
def raw2png_crop(raw, png, roi):
    '''
    Convert raw image to png image with cropping
    Parameters
    ----------
    raw : string
        Raw filename
    png : string
        Output filename
    roi : string
        Crop region, imagemagick format.
    '''
    command = 'dcraw -4 -w -c ' + raw + ' | convert - -crop ' + roi + ' +repage ' + png
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    subprocess.check_call(['rm', '-f', raw])
    
def capture_and_show_intensity(roi):
    '''
    Capture and print mean intensity of the region
    Parameters
    ----------
    roi : string
        Crop region, imagemagick format.
    '''
    set_iso400()
    subprocess.check_call(['rm', '-rf', 'temp.nef'])
    capture_and_save('temp.nef')
    raw2png_crop('temp.nef', 'temp.ppm', roi)
    img = cv2.imread('temp.ppm', -1)
    print np.mean(img)
    
camera_conf_names = {
        'shutter': '/main/capturesettings/shutterspeed',
        'ISO': '/main/imgsettings/iso',
        'f-number': '/main/capturesettings/f-number'}
        
#def capture_multiple_gains():
#    base_shutter = 41 # 3
#    base_ISO = 0 # 100
#    base_f_number = 5 # f/10
#    set_property(camera_conf_names['f-number'], base_f_number)
#    for iso in range(0, 24, 3):
#        set_property(camera_conf_names['shutter'], base_shutter)
#        set_property(camera_conf_names['ISO'], base_ISO)
#        base_shutter -= 3
#        base_ISO += 3
#        capture_and_save('ISO'+str(iso)+'.nef')
#        raw2png('ISO'+str(iso)+'.nef', 'ISO'+str(iso)+'.png')
#        
#def print_values():
#    print 'target brightness: 16384'    
#    for iso in range(0, 24, 3):
#        print iso, np.amax(cv2.imread('ISO'+str(iso)+'.png', -1))
        
def set_ISO(value=6):
    '''
    Set ISO value.
    Parameters
    ----------
    value : int
        Index of configurable property values.
        
    See also
    --------
    print_configurable_properties, print_property, set_property
    '''
    set_property(camera_conf_names['ISO'], value)
    
def set_shutter(value=35):
    '''
    Set shutter value.
    Parameters
    ----------
    value : int
        Index of configurable property values.
        
    See also
    --------
    print_configurable_properties, print_property, set_property
    '''
    set_property(camera_conf_names['shutter'], value)
    
def set_f_number(value=5):
    '''
    Set f-number value.
    Parameters
    ----------
    value : int
        Index of configurable property values.
        
    See also
    --------
    print_configurable_properties, print_property, set_property
    '''
    set_property(camera_conf_names['f-number'], value)
    
        
def set_iso400():
    base_shutter = 35 # .7692s, 10/13
    base_ISO = 6 # 400
    base_f_number = 5 # f/10
    set_property(camera_conf_names['f-number'], base_f_number)
    set_property(camera_conf_names['shutter'], base_shutter)
    set_property(camera_conf_names['ISO'], base_ISO)
    

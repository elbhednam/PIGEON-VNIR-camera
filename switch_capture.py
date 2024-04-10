from gpiozero import Button 
from picamera2 import Picamera2, Metadata
from libcamera import controls
from pprint import *
import time
import os
from datetime import datetime
import utils 

    
def main():
    """
    The main function for camera operation.

    """
    # The button is hardcoded to GPIO pin 2 
    button = Button(2, bounce_time=0.2)  
    
    # Define camera objects
    camera0 = Picamera2(0) # NoIR Camera
    camera1 = Picamera2(1) # RGB Camera
    
    # PNG compression level, where 0 gives no compression 
    camera0.options["compress_level"] = 0  
    camera1.options["compress_level"] = 0  

    #-------------------------------------------------------------------------------------------------------
    cameras_info = Picamera2.global_camera_info() # returns a list containing one dictionary for each camera

    num_of_cam = len(cameras_info)

    if num_of_cam == 0:
        print("No cameras attached! Exit")
        exit(1)
    
    print("number of cameras: ", num_of_cam)
    
    new_folder_path, folder_name = utils.make_image_folder('/home/sensors/Pictures/')
    
    # initially set Awb and Aec/Aeg to auto and get baseline camera control settings and metadata
    metadata0 = utils.get_auto_settings(camera0, new_folder_path + '/auto_settings_noir.png')
    metadata1 = utils.get_auto_settings(camera1, new_folder_path + '/auto_settings_rgb.png')
    
    # Tell us that the  auto settings have been taken
    print ("Auto Settings picture has been taken")
    
    # Call configuration function
    config = utils.configure_camera(camera1)
    
    # Configure cameras
    camera0.configure(config)
    camera1.configure(config)
    
    # set camera controls based on metadata from auto settings
    utils.set_camera_controls(camera0, metadata0)
    utils.set_camera_controls(camera1, metadata1)

    # start streams for both cameras
    camera0.start()
    camera1.start()
    
    i = 0 
    while True: 
        if button.is_pressed:
            # Picamera2 uses PIL to save the images, so this supports JPEG, BMP, PNG and GIF files
            img_name0 = 'imx708_noir_%s.png' % str(i) 
            img_name1 = 'imx708_%s.png' % str(i)
            
            # Switch to still capture configuration and take a picture
            camera0.capture_file(os.path.join(new_folder_path, img_name0))  
            camera1.capture_file(os.path.join(new_folder_path, img_name1))
            
            # Get image metadata
            metadata0 = camera0.capture_metadata()
            metadata1 = camera1.capture_metadata()

            # Save metadata per image to file
            utils.save_metadata_to_file(os.path.join(new_folder_path, 'metadata_%s.txt' % folder_name), img_name0, metadata0)
            utils.save_metadata_to_file(os.path.join(new_folder_path, 'metadata_%s.txt' % folder_name), img_name1, metadata1)
            button.wait_for_release()  # This stops the camera from rapid firing if the button is held down
            i += 1 

if __name__ == "__main__":
    main()

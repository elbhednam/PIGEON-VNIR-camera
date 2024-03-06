from gpiozero import Button 
from picamera2 import Picamera2, Metadata
from libcamera import controls
from pprint import *
import time
import os
from datetime import datetime
from utils import *

    
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

    #-------------------------------------------------------------------------------------------------------
    
    preview_mode = camera1.sensor_modes[0] # Lower resolution sensor mode for the preview window
    capture_mode = camera1.sensor_modes[2] # Highest resolution sensor mode for image capture
    
    # configuration suitable for fast preview window based on sensor mode 0
    preview_config = camera1.create_preview_configuration(sensor={'output_size': preview_mode['size'],
                                                                 'bit_depth': preview_mode['bit_depth']})  
                                                                 
    # configuration suitable for capturing a high-resolution still image based on sensor mode 2
    capture_config = camera1.create_still_configuration(sensor={'output_size': capture_mode['size'],
                                                               'bit_depth': capture_mode['bit_depth']})  
    # configure preview window for both cameras                                                            
    camera0.configure(preview_config)
    camera1.configure(preview_config)
    
    # TODO: IMPLEMENT FUNCTION TO INITIALLY SET  AWB AND AEC/AGC TO AUTO AND GET BASELINE CAMERA CONTROL SETTINGS AND METADATA
    # TODO: IMPLEMENT FUNCTION TO SET CAMERA CONTROLS BASED ON METADATA FROM AUTO SETTINGS
    # set camera controls based on auto settings
    camera0.set_controls({
        "AeEnable": False,  # Disable AEC/AGC
        "AwbEnable": False,  # Disable AWB
        "AfMode": controls.AfModeEnum.Manual,  # Set autofocus to manual so lens position can be set
        "LensPosition": 0.0,  # in dioptres (reciprocal of the distance in metres)
        "ExposureTime": 1500,  # in microseconds = 1/ 1million, smaller number is faster
        "AnalogueGain": 1.0,  # min: 1.1228070259094238, max: 16.0
        "ColourGains": (1.0, 2.5)  # red gain, blue gain (between 0.0 and 32.0), setting this overrides AWB even if AwbEnable is set to true
    })

    camera1.set_controls({
        "AeEnable": False,  # Disable AEC/AGC
        "AwbEnable": False,  # Disable AWB
        "AfMode": controls.AfModeEnum.Manual,  # Set autofocus to manual so lens position can be set
        "LensPosition": 0.0,  # in dioptres (reciprocal of the distance in metres)
        "ExposureTime": 1500,  # in microseconds = 1/ 1million, smaller number is faster
        "AnalogueGain": 1.0,  # min: 1.1228070259094238, max: 16.0
        "ColourGains": (1.0, 2.5)  # red gain, blue gain (between 0.0 and 32.0), setting this overrides AWB even if AwbEnable is set to true
    })

    # start streams for both cameras
    camera0.start(show_preview=True)
    camera1.start(show_preview=True)

    # TODO: SEPARATE LOGIC TO MAKE A NEW FOLDER AND PUT IT INTO A FUNCTION IN UTILS SCRIPT
    # new_folder_path, folder_name = make_image_folder('/home/sensors/Pictures/')
    
    # create new image folder for output
    now = datetime.now()  # Get the current date and time
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")  # Format the date and time as desired for the folder name
    new_folder_path = os.path.join('/home/sensors/Pictures/', folder_name)
    os.mkdir(new_folder_path)

    # TODO: SEPARATE CAMERA LOOP INTO 'BUTTON_CAPTURE' FUNCTION
    # TODO: WRITE 'TIMED_CAPTURE' AND 'GPS_CAPTURE FUNCTIONS AS ALTERNATIVES
    i = 0 
    while True: 
        if button.is_pressed:
            # Picamera2 uses PIL to save the images, so this supports JPEG, BMP, PNG and GIF files
            img_name0 = 'imx708_noir_%s.png' % str(i) 
            img_name1 = 'imx708_%s.png' % str(i) 
            # Switch to still capture configuration and take a picture
            camera0.switch_mode_and_capture_file(capture_config, os.path.join(new_folder_path, img_name0))  
            camera1.switch_mode_and_capture_file(capture_config, os.path.join(new_folder_path, img_name1))  
            # Get image metadata
            metadata0 = camera0.capture_metadata()
            metadata1 = camera1.capture_metadata()
            # Save metadata
            pprint(metadata0)
            print()
            pprint(metadata1)
            # TODO: IMPLEMENT FUNCTION TO SAVE METADATA TO A FILE
            #save_metadata_to_file(os.path.join(new_folder_path, 'metadata_%s.txt' % folder_name), img_name0, metadata0)
            #save_metadata_to_file(os.path.join(new_folder_path, 'metadata_%s.txt' % folder_name), img_name1, metadata1)
            button.wait_for_release()  # This stops the camera from rapid firing if the button is held down
            i += 1 

if __name__ == "__main__":
    main()

from gpiozero import Button 
from picamera2 import Picamera2, Metadata # use Metadata object for 'get_auto_settings' function
from libcamera import controls
from pprint import *
import time
import os
from datetime import datetime

def save_metadata_to_file(filename, image_name, metadata):
    """
    Saves image metadata to a file.

    Parameters:
    - filename (str): The path to the file where metadata will be saved.
    - image_name (str): The name of the image.
    - metadata: The metadata object to be saved.

    Returns:
    - None
    """
    with open(filename, 'a') as file:
        file.write("Image Name: {}\n".format(image_name))
        file.write("Image Metadata:\n")
        file.write(str(metadata))
        file.write("\n")
        file.write("------------------------------------------------------------------\n")
    pass

def make_image_folder(base_dir):
    """
    Creates a new folder with a timestamped name.

    Parameters:
    - base_dir (str): The base directory where the new folder will be created.

    Returns:
    - new_folder_path (str): The path to the newly created folder.
    - folder_name (str): The name of the newly created folder.
    """
    now = datetime.now()  # Get the current date and time
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")  # Format the date and time as desired for the folder name
    new_folder_path = os.path.join(base_dir, folder_name)
    os.mkdir(new_folder_path)
    
    return new_folder_path, folder_name

def delete_empty_folder(folder_path):
    """
    Deletes the folder if it is empty.

    Parameters:
    - folder_path (str): The path to the folder.

    Returns:
    - None
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
    
    pass
   
def configure_camera(camera):
    # highest resolution capture mode for the IMX708
    mode = camera.sensor_modes[2]
    
    # configuration suitable for capturing a high-resolution still image based on sensor mode 2
    conf = camera.create_still_configuration(sensor={'output_size': mode['size'],
                                                     'bit_depth': mode['bit_depth'],
                                                     'format': mode['unpacked']}) # Explicitly requests 'SRGGB10' unpacked format
    return conf
    
def get_auto_settings(camera, file_path):
    """
    Retrieves automatic camera settings.

    Parameters:
    - camera: The camera object.

    Returns:
    - metadata: The metadata object containing automatic camera settings.
    """
    #capture_mode = camera.sensor_modes[2] # Highest resolution sensor mode for image capture
    
    # configuration suitable for capturing a high-resolution still image based on sensor mode 2
    config = configure_camera(camera)
    camera.configure(config)
    # Set AeEnable and AwbEnable to True
    camera.set_controls({
    "AeEnable": True,
    "AwbEnable": True,
    "AfMode": controls.AfModeEnum.Manual,
    "LensPosition": 0.0,
    })

    # Start the camera
    camera.start()

    # Wait for AEC/AGC to settle (1-2 seconds)
    time.sleep(1)

    # Capture metadata
    metadata = Metadata(camera.capture_metadata())
    # create new image folder for output
    camera.capture_file(file_path) 
    # Stop the camera
    camera.stop()

    return metadata
    
def set_camera_controls(camera, metadata):
    """
    Sets camera controls.

    Parameters:
    - camera: The camera object.
    - metadata: The metadata object containing camera settings.

    Returns:
    - None
    """

     # Set AeEnable and AwbEnable to False
    camera.set_controls({
    "AeEnable": False,
    "AwbEnable": False,
    "AfMode": controls.AfModeEnum.Manual,
    "LensPosition": 0.0,
    
    "ExposureTime": metadata.ExposureTime,
    "AnalogueGain": metadata.AnalogueGain,
    "ColourGains": metadata.ColourGains,

    })

    return

def system_shutdown():

    Button(21).wait_for_press()
    os.system("sudo poweroff")
    pass


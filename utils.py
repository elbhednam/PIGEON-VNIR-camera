from gpiozero import Button 
from picamera2 import Picamera2, Metadata # use Metadata object for 'get_auto_settings' function
from libcamera import controls
from pprint import *
import time
import os
from datetime import datetime

# TODO: write a function that saves writes the image file name and corresponding metadata to a file for each image capture. Put separators and line breaks where appropriate.
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
    pass

# TODO: Put the logic to a create a new folder here. Return the folder path and folder name.
def create_new_folder(base_dir):
    """
    Creates a new folder with a timestamped name.

    Parameters:
    - base_dir (str): The base directory where the new folder will be created.

    Returns:
    - new_folder_path (str): The path to the newly created folder.
    - folder_name (str): The name of the newly created folder.
    """

    pass

# TODO: Write a function that deletes empty folders from when we run the code but don't capture an image
def delete_empty_folder(folder_path):
    """
    Deletes the folder if it is empty.

    Parameters:
    - folder_path (str): The path to the folder.

    Returns:
    - None
    """
    pass
   
# TODO: Write a function that sets the AWB and AEC/AGC to true and captures and returns metadata. Metadata will be returned and used for manual camera settings.   
def get_auto_settings(camera):
    """
    Retrieves automatic camera settings.

    Parameters:
    - camera: The camera object.

    Returns:
    - metadata: The metadata object containing automatic camera settings.
    """
    pass

# TODO: Take camera settings logic from main script and put it into a function that sets the camera settings based on metadata from auto settings
def set_camera_controls(camera, metadata):
    """
    Sets camera controls.

    Parameters:
    - camera: The camera object.
    - metadata: The metadata object containing camera settings.

    Returns:
    - None
    """
    pass

# TODO: Take the logic from the camera loop and put it here
def button_capture(button, camera0, camera1, capture_config, new_folder_path, folder_name):
    """
    Capture images when the button is pressed.

    Parameters:
    - button: The GPIO button object.
    - camera0: The NoIR camera object.
    - camera1: The RGB camera object.
    - capture_config: Configuration for capturing images.
    - new_folder_path (str): The path to the newly created folder.
    - folder_name (str): The name of the newly created folder.

    Returns:
    - None
    """
    pass

# TODO: Write a function that will capture an image over regular intervals - 10s, 20s, 30s, whatever
def timed_capture(button, camera0, camera1, capture_config, new_folder_path, folder_name):
    """
    Capture images at regular intervals.

    Parameters:
    - button: The GPIO button object.
    - camera0: The NoIR camera object.
    - camera1: The RGB camera object.
    - capture_config: Configuration for capturing images.
    - new_folder_path (str): The path to the newly created folder.
    - folder_name (str): The name of the newly created folder.

    Returns:
    - None
    """
    pass

# TODO: Write a function that will capture an image triggered by the drone GPS
def gps_capture(button, camera0, camera1, capture_config, new_folder_path, folder_name):
    """
    Capture images triggered by GPS.

    Parameters:
    - button: The GPIO button object.
    - camera0: The NoIR camera object.
    - camera1: The RGB camera object.
    - capture_config: Configuration for capturing images.
    - new_folder_path (str): The path to the newly created folder.
    - folder_name (str): The name of the newly created folder.

    Returns:
    - None
    """
    pass

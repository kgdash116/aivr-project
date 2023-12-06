'''--------------------------------------------------------------------------------------------------------------------
Program name : aivr.py (Testing)
Coded By     : Waqas Kureshy
Date         : 2023-11-29
Updated By   :
Date         :
Version      : v 0.1.1
Copyright    : Copyright (c) 2023 Waqas Kureshy
Purpose      : The aivr script has utility functions. Its intended purpose is to establish a connection with the 
               Unity environment using sockets utilizing the 'ZMQ' library. It offers utility functions for developers to
               interact with the Unity Environment, the utility functions include creating objects including Spheres and 
               Cubes, transmitting webcam feed, creating 3D text and sending video files. 
----------------------------------------------------------------------------------------------------------------------'''



from .aivr_webcam import WebcamController
from datetime import datetime
import sys
import zmq
import cv2
import json
import base64
import time
import os
import threading

CONNECTION_STRING="tcp://127.0.0.1:5555"
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)
MAGENTA = (1, 0, 1)
CYAN = (0, 1, 1)
BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
webcam_controller = None


def colorChecker(color_tuple):
    '''Private Helper Function to check the color tuple i.e wether R,G,B values are between 0 and 1'''
    '''It returns a string representing the color in R,G,B values'''
    if not isinstance(color_tuple, tuple) or len(color_tuple) != 3:
        raise ValueError("COLOR Input must be a tuple of three digits between 0 and 1.")

    for value in color_tuple:
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Each value in the COLOR tuple must be a digit between 0 and 1.")

    result_string = ",".join(map(str, color_tuple))

    return result_string

def _spawn_Position_Checker(spawn_pos):
    '''Private helper function to check the validity of user entered spawn position for objects.'''
    '''This function returns a Boolean value'''
    spawn_position_values = spawn_pos.split(',')
    if len(spawn_position_values) == 3:
        try:
            x_coord, y_coord, z_coord = map(float, spawn_position_values)
            print("Valid spawn position:", x_coord, y_coord, z_coord)
            return True
        except ValueError:
            print("Invalid spawn position input. All three values must be numbers.")
            return False
    else:
        print("Invalid spawn position input format. Enter three values separated by commas (x,y,z).")
        return False

def _object_scale_checker(obj_scale):
    '''Private helper function to check the validity of user entered scale for objects.'''
    '''This function returns a Boolean value'''
    scale_input_values = obj_scale.split(',')
    if len(scale_input_values) == 3:
        try:
            cube_height, cube_width, cube_length = map(float, scale_input_values)
            print("Valid scale:", cube_height, cube_width, cube_length)
            return True
        except ValueError:
            print("Invalid scale input. All three values must be numbers.")
            return False
    else:
        print("Invalid scale input format. Enter three values separated by commas (h,w,l).")
        return False

def _object_rotation_checker(obj_rot):
    '''Private helper function to check the validity of user entered rotation for objects.'''
    '''This function returns a default value if input is wrong or it returns the user input'''
    rotation_input_values = obj_rot.split(',')
    if len(rotation_input_values) == 3:
        try:
            x,y,z = map(float, rotation_input_values)
            print("Valid rotation values:",x,y,z)
            return obj_rot
        except ValueError:
            print("Invalid rotation values. All three values must be numbers.Opting default values")
            return "0,0,0"
    else:
        print("Invalid rotation value format.Three inputs seperated by commas are required.Opting default values.")
        return "0,0,0"


def placeCube(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place an cube in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position and scale for the cube'''
    '''The color for the cube can be passed as a paramter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")

    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return

    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values: ")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)
                



    message = f"ai_vr create_cube {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    print(message)
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeSphere(conn_string, color=RED,object_name=None,spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place a Sphere in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position and radius for the sphere'''
    '''The color for the sphere can be passed as a parameter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")

    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return

    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)

    message = f"ai_vr create_sphere {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeCylinder(conn_string, color=RED,object_name=None,spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place a Cylinder in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position and radius for the sphere'''
    '''The color for the Cylinder can be passed as a parameter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")

    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return
    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)

    message = f"ai_vr create_cylinder {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeCapsule(conn_string, color=RED,object_name=None,spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place a Capsule in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position '''
    '''The color for the Capsule can be passed as a parameter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")
    
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return
    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)

    message = f"ai_vr create_capsule {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()


def placePlane(conn_string, color=RED,object_name=None,spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place a Plane in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position '''
    '''The color for the Plane can be passed as a parameter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")
    
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return

    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)

    message = f"ai_vr create_plane {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()

def placeQuad(conn_string, color=RED,object_name=None,spawn_position_input=None,scale_input=None,object_rotation=None):
    '''Function to place a Quad in the Unity environment based on user input'''
    '''The user is asked for a name, spawn position '''
    '''The color for the Quad can be passed as a parameter to the function '''
    '''as a tuple representing R,G,B values or by usnig a color constant which have been declared above'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)
    if object_name==None or spawn_position_input==None or scale_input==None:
        object_name=input("Enter object name: ")
        if object_name == "":
            print("Invalid object name")
            return
        spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
        scale_input = input("Enter scale (h,w,l), separated by commas: ")
    
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return

    if object_rotation==None:
        object_rotation_input=input("Enter object rotation in (x,y,z) format, or press enter for default values")
        if object_rotation_input=="":
            object_rotation="0,0,0"
        else:
            object_rotation=_object_rotation_checker(object_rotation_input)

    message = f"ai_vr create_quad {spawn_position_input} {scale_input} {object_name} {objectColor} {object_rotation}"
    time.sleep(1)
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeObjectWithJson():
    '''Function to place obects in the Unity environment using input from a json file'''
    '''The user is prompted to add a path to the json file'''
    function_mapping = {
    "cube": placeCube,
    "cylinder": placeCylinder,
    "quad": placeQuad,
    "sphere": placeSphere, 
    "plane": placePlane, 
    "capsule": placeCapsule,}

    file_path = input("Enter the path to the JSON file: ")
    read_json=open(file_path,'r')
    data=json.loads(read_json.read())
    if data is not None:
        if "objects" in data:
            objects = data["objects"]
            print("Objects in the JSON file:")
            for obj in objects:
                try:
                    object_type=obj["object_type"]
                    object_name = obj["object_name"]
                    spawn_position = obj["spawn_position"]
                    object_scale = obj["object_scale"]
                    object_color = obj["object_color"]
                    object_rotation = obj["object_rotation"]
                except KeyError as e:
                    print(f"KeyError: key {e} not found in JSON file")
                    return
                print(f"TYPE: {object_type} NAME: {object_name} POS: {spawn_position} SCALE: {object_scale} COLOR: {object_color} ROT: {object_rotation}")
                colors = object_color.split(',')
                float_values = [float(value) for value in colors]
                result_tuple = tuple(float_values)
                if object_type in function_mapping:
                # Get the function
                    selected_function = function_mapping[object_type]

                # Call the selected function with the parameters from the JSON file
                    selected_function(CONNECTION_STRING,result_tuple,object_name,spawn_position,object_scale,object_rotation)
                else:
                    print(f"Invalid object_type: {object_type}")
        else:
            print("No 'objects' key found in the JSON data.")
    else:
        print("Invalid file path or the file does not contain valid JSON data.")

    


def placeText(conn_string, color=RED):
    '''Function to place Text in the Unity environment by taking in user input'''
    '''It takes the connection string and a color tuple with R,G,B values'''
    '''Color constants can be used as well during function calling, like (aivr.BLUE) '''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    textColor=colorChecker(color)
    text_spawn_position_input = input("Enter text spawn position (x,y,z), separated by commas: ")
    text_spawn_position_values = _spawn_Position_Checker(text_spawn_position_input)
    text_spawn_position_values = text_spawn_position_input.split(',')
    if len(text_spawn_position_values) == 3:
        try:
            x_pos, y_pos, z_pos = map(float, text_spawn_position_values)
            print("Valid spawn position:", x_pos, y_pos, z_pos)
        except ValueError:
            print("Invalid input. All three values must be numbers.")
            return
    else:
        print("Invalid input format. Enter three values separated by commas (x,y,z).")
        return

    font_size = input("Enter font size: ")
    try:
        font_size_value = int(font_size)
        print("Valid font_size: ", font_size_value)
    except ValueError:
        print("Invalid input, value must be a number.")
        return
    text_to_display = input("Enter Text to display: ")
    if (text_to_display == ""):
        print("No text added")
        return

    message = f"ai_vr text_addition {x_pos} {y_pos} {z_pos} {font_size} {textColor} {text_to_display}"
    publisher.send_string(message)
    publisher.close()
    context.term()



def toggleWebcamFeed():
    '''Function for turning webcam feed ON/OFF'''
    '''This function utilizes the WebcamController class from the aivr_webcam file'''
    global webcam_controller
    if (webcam_controller== None):
        webcam_controller=WebcamController()
        webcam_controller.toggle_webcam()
    else:
        webcam_controller.toggle_webcam()

def switchColorMode():
    '''Function for switching webcam feed from RGB to Grayscale and vice-versa'''
    '''This function utilizes the WebcamController class from the aivr_webcam file'''
    global webcam_controller
    if(webcam_controller):
        webcam_controller._toggle_grayscale_mode()


def sendVidLink(conn_string):
    '''This function takes in a path of a video file and sends it to the Unity environment'''
    '''Unity checks the path for validity and then displays the video'''
    '''This function takes in the scale as well as the position of the video object to be placed in Unity.'''
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(conn_string)
    file_path=input("Enter File Path: ")
    if os.path.exists(file_path):
        print(f"The file at {file_path} exists.")
    else:
        print(f"The file at {file_path} does not exist.")
    spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return

    scale_input = input("Enter scale (h,w,l), separated by commas: ")
    scale_input_values = _object_scale_checker(scale_input)
    if (not scale_input_values):
        return

    try:
        print("Sending Video")
        message = f"ai_vr launch_video {spawn_position_input} {scale_input} {file_path}"
        socket.send_string(message)
    finally:
        socket.close()
        context.term()
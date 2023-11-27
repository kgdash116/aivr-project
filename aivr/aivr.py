'''--------------------------------------------------------------------------------------------------------------------
Program name : aivr.py (Testing)
Coded By     : Waqas Kureshy
Date         : 2023-11-26
Updated By   :
Date         :
Version      : v 0.0.10
Copyright    : Copyright (c) 2023 Waqas Kureshy
Purpose      : Establish a connection using sockets, used for placing objects, placing text and transferring webcam feed
               to Unity
----------------------------------------------------------------------------------------------------------------------'''




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

class WebcamController:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5556")
        self.cap = None
        self.webcam_thread = None
        self.is_webcam_on = False
        self.isGrayScaleEnabled=False

    def toggle_webcam(self):
        if self.is_webcam_on:
            # Stop the webcam
            self.is_webcam_on = False
            if self.webcam_thread and self.webcam_thread.is_alive():
                self.webcam_thread.join()
            if self.cap and self.cap.isOpened():
                self.cap.release()
                cv2.destroyAllWindows()

            print("Webcam stopped.")
        else:
            # Start the webcam
            self.is_webcam_on = True
            self.webcam_thread = threading.Thread(target=self._toggle_webcam_on, daemon=True)
            self.webcam_thread.start()
            print("Webcam started.")

    def _toggle_webcam_on(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Webcam not detected or could not be opened.")
            return

        try:
            while self.is_webcam_on:
                ret, frame = self.cap.read()

                if not ret:
                    print("Error: Unable to capture frame.")
                    continue

                if self.isGrayScaleEnabled:
                    #Turn frames to grayscale if isGrayScaleEnabled 
                    gray_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    _, buffer = cv2.imencode('.jpg', gray_frame)
                else:
                    #Send RGB frames    
                    _, buffer = cv2.imencode('.jpg', frame)
                self.socket.send(buffer.tobytes())

        except KeyboardInterrupt:
            self.socket.send(b'STOP')
            print("Terminating webcam frame sender.")

        finally:
            self.cap.release()
            cv2.destroyAllWindows()

    def _toggle_grayscale_mode(self):
        self.isGrayScaleEnabled= not self.isGrayScaleEnabled



def colorChecker(color_tuple):
    '''Helper Function to check the color tuple i.e wether R,G,B values are between 0 and 1'''
    '''It returns a string representing the color in R,G,B values'''
    if not isinstance(color_tuple, tuple) or len(color_tuple) != 3:
        raise ValueError("Input must be a tuple of three digits between 0 and 1.")

    for value in color_tuple:
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Each value in the tuple must be a digit between 0 and 1.")

    result_string = ",".join(map(str, color_tuple))

    return result_string

def _spawn_Position_Checker(spawn_pos):
    spawn_position_values = spawn_pos.split(',')
    if len(spawn_position_values) == 3:
        try:
            x_coord, y_coord, z_coord = map(float, spawn_position_values)
            print("Valid spawn position:", x_coord, y_coord, z_coord)
            return True
        except ValueError:
            print("Invalid input. All three values must be numbers.")
            return False
    else:
        print("Invalid input format. Enter three values separated by commas (x,y,z).")
        return False

def _object_scale_checker(obj_scale):
    scale_input_values = obj_scale.split(',')
    if len(scale_input_values) == 3:
        try:
            cube_height, cube_width, cube_length = map(float, scale_input_values)
            print("Valid scale:", cube_height, cube_width, cube_length)
            return True
        except ValueError:
            print("Invalid input. All three values must be numbers.")
            return False
    else:
        print("Invalid input format. Enter three values separated by commas (h,w,l).")
        return False




def placeObject(conn_string, color=RED):
    '''Function to place an obect in the Unity environment by taking in user input'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)

    object_name=input("Enter object name: ")
    if object_name == "":
        print("Invalid object name")
        return
    spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    

    scale_input = input("Enter scale (h,w,l), separated by commas: ")
    scale_input_values = _object_scale_checker(scale_input)
    if(not scale_input_values):
        return


    message = f"ai_vr createcube {spawn_position_input} {scale_input} {object_name} {objectColor}"
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeSphere(conn_string, color=RED):
    '''Function to place an obect in the Unity environment by taking in user input'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    objectColor=colorChecker(color)

    object_name=input("Enter object name: ")
    if object_name == "":
        print("Invalid object name")
        return
    spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
    spawn_position_values = _spawn_Position_Checker(spawn_position_input)
    if (not spawn_position_values):
        return
    

    try:
        radius_input = input("Enter the radius for the sphere: ")
        radius = float(radius_input)
        print("Valid float value entered:", radius)
    except ValueError:
        print("Invalid input. Please enter a valid float value.")
        return

    


    message = f"ai_vr create_sphere {spawn_position_input} {radius_input} {object_name} {objectColor}"
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeObjectWithJson(conn_string):
    '''Function to place an obect in the Unity environment using input from json file'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    file_path = input("Enter the path to the JSON file: ")
    read_json=open(file_path,'r')
    data=json.loads(read_json.read())
    if data is not None:
        if "objects" in data:
            objects = data["objects"]
            print("Objects in the JSON file:")
            for obj in objects:
                object_name = obj["object_name"]
                if object_name== "" or None:
                    print(f"Invalid object name found")
                    return
                spawn_position = obj["spawn_position"]
                spawn_position_values = spawn_position.split(',')
                if len(spawn_position_values) == 3:
                    try:
                        x_coord, y_coord, z_coord = map(float, spawn_position_values)
                        print("Valid spawn position:", x_coord, y_coord, z_coord)
                    except ValueError:
                        print("Invalid input. All three values must be numbers.")
                        return
                else:
                    print(f"Invalid input format {spawn_position} for object named: '{object_name}'. Enter three values separated by commas (x,y,z).")
                    return
                
                object_scale = obj["object_scale"]
                object_scale_values = object_scale.split(',')
                if len(object_scale_values) == 3:
                    try:
                        cube_height, cube_width, cube_length = map(float, object_scale_values)
                        print("Valid scale:", cube_height, cube_width, cube_length)
                    except ValueError:
                        print("Invalid input. All three values must be numbers.")
                        return
                else:
                    print(f"Invalid input format for object name: {object_name}. Enter three values separated by commas (h,w,l).")
                    return

                object_color = obj["object_color"]
                object_color_values = object_color.split(',')
                if len(object_color_values) == 3:
                    try:
                        r, g, b = map(float, object_color_values)
                        if 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1:
                            print("Valid color:", r, g, b)
                        else:
                            print("Invalid input. All three values must be between 0 and 1.")
                    except ValueError:
                        print("Invalid input. All three values must be numbers.")
                else:
                    print(f"Invalid input format {object_color} for object named: '{object_name}'. Enter three values separated by commas (R,G,B).")
                print(f"Object Name: {object_name}")
                print(f"Spawn Position: {spawn_position}")
                print(f"Object Scale: {object_scale}")
                print(f"Object Color: {object_color}")
                message = f"ai_vr createcube {spawn_position} {object_scale} {object_name} {object_color}"
                publisher.send_string(message)
        else:
            print("No 'objects' key found in the JSON data.")
    else:
        print("Invalid file path or the file does not contain valid JSON data.")

    publisher.close()
    context.term()


def placeText(conn_string, color=RED):
    '''Function to place Text in the Unity environment by taking in user input'''
    '''It takes the connection string and a color tuple with R,G,B values'''
    '''Color constants can be used as well during function calling like aivr.BLUE '''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    textColor=colorChecker(color)
    text_spawn_position_input = input("Enter text spawn position (x,y,z), separated by commas: ")
    text_spawn_position_values = _spawn_Position_Checker(text_spawn_position_input)
    if (not text_spawn_position_values):
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
    global webcam_controller
    if (webcam_controller== None):
        webcam_controller=WebcamController()
        webcam_controller.toggle_webcam()
    else:
        webcam_controller.toggle_webcam()

def switchColorMode():
    global webcam_controller
    if(webcam_controller):
        webcam_controller._toggle_grayscale_mode()


def sendVidLink(conn_string):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(conn_string)
    file_path=input("Enter File Path: ")
    if os.path.exists(file_path):
        print(f"The file at {file_path} exists.")
    else:
        print(f"The file at {file_path} does not exist.")
    spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
    spawn_position_values = spawn_position_input.split(',')
    if len(spawn_position_values) == 3:
        try:
            x_coord, y_coord, z_coord = map(float, spawn_position_values)
            print("Valid spawn position:", x_coord, y_coord, z_coord)
        except ValueError:
            print("Invalid input. All three values must be numbers.")
            return
    else:
        print("Invalid input format. Enter three values separated by commas (x,y,z).")
        return

    scale_input = input("Enter scale (h,w,l), separated by commas: ")
    scale_input_values = scale_input.split(',')
    if len(scale_input_values) == 3:
        try:
            cube_height, cube_width, cube_length = map(float, scale_input_values)
            print("Valid scale:", cube_height, cube_width, cube_length)
        except ValueError:
            print("Invalid input. All three values must be numbers.")
            return
    else:
        print("Invalid input format. Enter three values separated by commas (h,w,l).")
        return

    try:
        #time.sleep(3)
        print("Sending String")
        message = f"ai_vr launch_video {spawn_position_input} {scale_input} {file_path}"
        #message = "ai_vr /Users/waqaskureshy/Pictures/test_videos/test_2.mp4"
        socket.send_string(message)
        #time.sleep(3)
    finally:
        # Close the socket and terminate the context after sending the message
        socket.close()
        context.term()
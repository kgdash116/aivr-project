'''--------------------------------------------------------------------------------------------------------------------
Program name : aivr.py (Testing)
Coded By     : Waqas Kureshy
Date         : 2023-09-21
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

    def toggle_webcam(self):
        if self.is_webcam_on:
            # Stop the webcam
            self.is_webcam_on = False
            #self.socket.send(b'STOP')

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

                _, buffer = cv2.imencode('.jpg', frame)
                self.socket.send(buffer.tobytes())

        except KeyboardInterrupt:
            self.socket.send(b'STOP')
            print("Terminating webcam frame sender.")

        finally:
            self.cap.release()
            cv2.destroyAllWindows()




def colorChecker(color_tuple):
    if not isinstance(color_tuple, tuple) or len(color_tuple) != 3:
        raise ValueError("Input must be a tuple of three digits between 0 and 1.")

    for value in color_tuple:
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Each value in the tuple must be a digit between 0 and 1.")

    result_string = ",".join(map(str, color_tuple))

    return result_string


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


    message = f"ai_vr createcube {spawn_position_input} {scale_input} {object_name} {objectColor}"
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
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(conn_string)

    print(f"COLOR: {color}")
    textColor=colorChecker(color)
    text_spawn_position_input = input("Enter text spawn position (x,y,z), separated by commas: ")
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


    message = f"ai_vr text_addition {x_pos} {y_pos} {z_pos} {font_size} {textColor} {text_to_display}"
    publisher.send_string(message)
    publisher.close()
    context.term()


def getCam():
    '''Function for projecting webcam input to the Unity environment,
        this method supports RGB and GRAYSCALE'''
    window_width = 640
    window_height = 360
    gray_scale_enabled=False
    is_web_cam_enabeled=True

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://127.0.0.1:8555")

    cv2.namedWindow("OpenCVWindow", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("OpenCVWindow", (window_width, window_height))   # 16:9 aspect ratio

    print("Start time:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    print("\nEnter g to toggle Grayscale-RGB")
    print("\nEnter q to quit")
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Could not open camera.")
        sys.exit()


    while (is_web_cam_enabeled):

        identity, message = socket.recv_multipart()
        #print(message)
        ret, frame = cam.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        resized_image = cv2.resize(frame, (window_width, window_height), cv2.INTER_AREA)
        img_gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        try:
            if not gray_scale_enabled:
                _, jpeg_image = cv2.imencode('.jpg', frame)
            else:
                _, jpeg_image = cv2.imencode('.jpg', img_gray)


            socket.send_multipart([identity, jpeg_image.tobytes()])
        except Exception as e:
            print("Error sending image:", str(e))
            break
        # except KeyboardInterrupt:
        #     print("Terminating webcam frame sender.")
        #     cam.release()
        #     cv2.destroyAllWindows()


        cv2.imshow("OpenCVWindow", resized_image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            is_web_cam_enabeled=False
            break
        if key == ord("g"):
            gray_scale_enabled = not gray_scale_enabled



    cam.release()
    cv2.destroyAllWindows()
    print("End time:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    socket.close()
    context.term()

# def getCam():
#     context = zmq.Context()
#     socket = context.socket(zmq.PUB)
#     socket.bind("tcp://127.0.0.1:5556")

#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Error: Webcam not detected or could not be opened.")
#         return

#     try:
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 print("Error: Unable to capture frame.")
#                 continue

#             _, buffer = cv2.imencode('.jpg', frame)
#             #jpg_as_text = base64.b64encode(buffer)

#             socket.send(buffer.tobytes())

#     except KeyboardInterrupt:
#         print("Terminating webcam frame sender.")

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()

#--------------------------------------------------------------
# def toggleWebcamOn():
#     context = zmq.Context()
#     socket = context.socket(zmq.PUB)
#     socket.bind("tcp://127.0.0.1:5556")

#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Error: Webcam not detected or could not be opened.")
#         return

#     try:
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 print("Error: Unable to capture frame.")
#                 continue

#             _, buffer = cv2.imencode('.jpg', frame)
#             #jpg_as_text = base64.b64encode(buffer)

#             #Disabling the opencv window popup as when this the package is 
#             #ran from shell and then closed the opencv window still lingers 
#             #around and freezes
            
#             #cv2.imshow("OpenCVWindow", frame)
#             #if cv2.waitKey(1) & 0xFF == ord('q'):
#             #    break
            
#             socket.send(buffer.tobytes())

#     except KeyboardInterrupt:
#         print("Terminating webcam frame sender.")
#         return

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()
#         socket.close()
#         context.term()

#--------------------------------------------------------------

def toggleWebcamOn():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5556")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Webcam not detected or could not be opened.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Unable to capture frame.")
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            #jpg_as_text = base64.b64encode(buffer)

            # cv2.imshow("OpenCVWindow", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            socket.send(buffer.tobytes())

    except KeyboardInterrupt:
        socket.send(b'STOP')
        print("Terminating webcam frame sender.")

    finally:
        cap.release()
        cv2.destroyAllWindows()

def getCams():
    # webcam_thread = threading.Thread(target=toggleWebcamOn, daemon=True)
    # webcam_thread.start()
    global webcam_controller
    if (webcam_controller== None):
        webcam_controller=WebcamController()
        webcam_controller.toggle_webcam()
    else:
        webcam_controller.toggle_webcam()


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
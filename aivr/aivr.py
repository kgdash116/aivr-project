'''--------------------------------------------------------------------------------------------------------------------
Program name : aivr.py (Testing)
Coded By     : Waqas Kureshy
Date         : 2023-09-21
Updated By   :
Date         :
Version      : v 0.0.7
Copyright    : Copyright (c) 2023 Waqas Kureshy
Purpose      : Establish a connection using sockets, used for placing objects, placing text and transferring webcam feed
               to Unity
----------------------------------------------------------------------------------------------------------------------'''




from datetime import datetime
import sys
import zmq
import cv2
import json





def placeObject():
    '''Function to place an obect in the Unity environment by taking in user input'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:5555")

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


    message = f"ai_vr createcube {spawn_position_input} {scale_input} {object_name}"
    publisher.send_string(message)
    publisher.close()
    context.term()


def placeObjectWithJson():
    '''Function to place an obect in the Unity environment using input from json file'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:5555")

    # read_json=open('data.json','r')
    # data=json.loads(read_json.read())
    # for i in data['objects']:
    #     print(i)


    file_path = input("Enter the path to the JSON file: ")
    read_json=open(file_path,'r')
    data=json.loads(read_json.read())
    if data is not None:
        if "objects" in data:
            objects = data["objects"]
            print("Objects in the JSON file:")
            for obj in objects:
                spawn_position = obj["spawn_position"]
                object_name = obj["object_name"]
                object_scale = obj["object_scale"]
                print(f"Object Name: {object_name}")
                print(f"Spawn Position: {spawn_position}")
                print(f"Object Scale: {object_scale}")
                message = f"ai_vr createcube {spawn_position} {object_scale} {object_name}"
                publisher.send_string(message)
        else:
            print("No 'objects' key found in the JSON data.")
    else:
        print("Invalid file path or the file does not contain valid JSON data.")

    # object_name=input("Enter object name: ")
    # if object_name == "":
    #     print("Invalid object name")
    #     return
    # spawn_position_input = input("Enter spawn position (x,y,z), separated by commas: ")
    # spawn_position_values = spawn_position_input.split(',')
    # if len(spawn_position_values) == 3:
    #     try:
    #         x_coord, y_coord, z_coord = map(float, spawn_position_values)
    #         print("Valid spawn position:", x_coord, y_coord, z_coord)
    #     except ValueError:
    #         print("Invalid input. All three values must be numbers.")
    #         return
    # else:
    #     print("Invalid input format. Enter three values separated by commas (x,y,z).")
    #     return

    # scale_input = input("Enter scale (h,w,l), separated by commas: ")
    # scale_input_values = scale_input.split(',')
    # if len(scale_input_values) == 3:
    #     try:
    #         cube_height, cube_width, cube_length = map(float, scale_input_values)
    #         print("Valid scale:", cube_height, cube_width, cube_length)
    #     except ValueError:
    #         print("Invalid input. All three values must be numbers.")
    #         return
    # else:
    #     print("Invalid input format. Enter three values separated by commas (h,w,l).")
    #     return


    # message = f"ai_vr createcube {spawn_position_input} {scale_input} {object_name}"
    # publisher.send_string(message)
    # publisher.close()
    # context.term()


def placeText():
    '''Function to place Text in the Unity environment by taking in user input'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:5555")

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


    message = f"ai_vr text_addition {x_pos} {y_pos} {z_pos} {font_size} {text_to_display}"
    publisher.send_string(message)
    publisher.close()
    context.term()


def getCam():
    '''Function for projecting webcam input to the Unity environment,
        this method supports RGB and GRAYSCALE'''
    window_width = 640
    window_height = 360
    gray_scale_enabled=False


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


    while True:

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


        cv2.imshow("OpenCVWindow", resized_image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cam.release()
            cv2.destroyAllWindows()
            break
        if key == ord("g"):
            gray_scale_enabled = not gray_scale_enabled




    print("End time:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    socket.close()
    context.term()

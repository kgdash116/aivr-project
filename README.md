# AIVR package
A Python Package that integrates with the Unity environment. This package, allows the user to communicate with the Unity environment, it has many functions, and leverages Machine Learning libraries such as Open-CV, ZeroMQ and numpy.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)


## Installation
- The following instructions are for using the **aivr** package locally.
- Download the Package, and place the **aivr-project** folder in a suitable directory.
- To install the package on **MacOS**, open the machine's terminal.
- First make a virtual environment on your machine. For this please install **virtualenv** by entering the following command.
  ```
  python3 -m pip install --user virtualenv
  ```
- After virtualenv has been installed, create a virtual environment by typing in the following on the terminal, in this case
  the name of the virtual environment is **aivr-venv**.
  ```
  virtualenv -p python3 ~/aivr-venv
  ```
- Now activate the environment, by typing in the following command:
  ```
  source ~/aivr-venv/bin/activate 
  ```
- To install the dependencies, navigate to the **aivr-project directory** and type in the following command:
  ```
  pip3 install -r requirements.txt
  ```
- Next, to install the package, type in the following command:
  ```
  python3 -m pip install -e .     

  ```
- Now the package is installed on your local machine.

- To install the **aivr package** without creating a virtual environment, open the terminal.

- Type in the following command, and change the YOUR-PATH segment to wherever the **aivr-project** folder is located

```
python3 -m pip install YOUR-PATH/aivr-project
```

## Usage

- Assuming the **aivr package** has been installed using the above mentioned steps, we can access the **aivr** package in our python scripts, by simply importing it.
- For demo purposes, open Terminal and type in:
    ```
    python3
    ```
- A Python interpreter will open up. To import the aivr package, type in the following command:
    ```
    import aivr
    ```
- The line above will import the **aivr package**.
- Now methods of the aivr module can be utilised.
- For example, to make a cube in the Unity environment, type in the following command:
    ```
    aivr.placeObject(aivr.CONNECTION_STRING,aivr.GREEN)
    ```
- When this is executed, a prompt appears which asks the user to input the coordinates where the cube is to be placed and so forth.
- **Integration with Unity**: Assuming, Unity is installed, open the Unity environment and open the project named:

    ```
    Python-OpenCV-2022-2-16
    ```
- Next, click on the play button, to enter game mode.
- Now simultaneously the user can launch a python script and make use of the **aivr module** methods.

## Methods:

- The following methods are in the aivr module,method names along with their description are given below:

| Method        | Description           |
| ------------- |:-------------:|
| placeCube(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      | Is used for placing a **cube** in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like **"2,2,2"**. This function than processes the users input with the help of helper functions to check input validity.The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter. |
| placeCapsule(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      |  Is used for placing a **capsule 3D object** in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like **"2,2,2"**. This function than processes the users input with the help of helper functions to check input validity. The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.  |
| placeCylinder(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      |  Is used for placing a **3D cylinder** in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like **"2,2,2"**. This function than processes the users input with the help of helper functions to check input validity.The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.  |
| placeSphere(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      |  Is used for placing a **3D sphere** in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like **"2,2,2"**. This function than processes the users input with the help of helper functions to check input validity. The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.  |
| placeQuad(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      |  Is used for placing a **3D Quad** element in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like "2,2,2". This function than processes the users input with the help of helper functions to check input validity.The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.   |
| placePlane(conn_string, color=RED, object_name=None, spawn_position_input=None,scale_input=None,object_rotation=None)      |  Is used for placing a **plane** in the Unity environment, it takes various input parameters like object scale, object spawn position, color for the object, rotation for the object and a connection strick to make a socket connection to the Receiver socket.If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.The color parameter of the function accepts a tuple, the object_name parameter should be a string and the rest of the parameters (spawn-position_input,scale_input and object_rotation) should be strings with three digits seperated by commas like **"2,2,2"**. This function than processes the users input with the help of helper functions to check input validity.The user has the ability to change the color of the object, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.  |
| placeObjectWithJson() | This method is used for passing a number of creating all sorts of 3D objects in the Unity environment with the help of JSON in one go. This method does not take any parameters. Whn this method is called, the user is asked for a path to the JSON file that contains the object related data. It checks for an array named **objects**, and furthermore checks for objects such as **object_type**, **spawn_position** , **object_name**, **object_rotation**, **object_scale** and **object_color** inside the **objects** array. This function parses the **JSON** file for these key value pairs and then passes along these parameters to their relevant functions based on the **object_type** parameter.Further processing of validity of data is done in each objects own function.    | 
| placeText(conn_string, color=RED) | This method is used for passing user input based text to the Unity environment. It takes the **CONNECTION_STRING** and **color** as  parameters.When invoked it prompts the user to enter the **spawn_position**, **font_size** and the **text to display** . It then checks the validity of the user input with the help of private helper functions. The user has the ability to change the color of the text, the default color is set to **RED**, to choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.| 
| sendVidLink(conn_string) | This method is used for passing a file path of a video element to the Unity environment. It takes the **CONNECTION_STRING** as a parameter which is decalred a s a constant in the aivr.py file. Wen invoked it prompts the user to enter a file path for the video, and then it checks the validity of the path.It prompts the user for the dimensions and the spawn position of the video object to display as well. If the path is valid it sends the path to the Unity environment, where it is then parsed and the video is rendered onto Unity based on the user provided coordinates.   | 
| toggleWebcamFeed() | is used for turning toggling the webcam feed. This method can be used for the transmission of video byte frames obtained from the webcam input to the Unity environment. this same function can be used for toggling webcam feed **ON/OFF**. This function uses the **OpenCV** library to open the users webcam, extract frames, convert it into bytes and then pass them over to the Unity environment, using a dedicated Publisher-Subscriber socket connection. This function makes a object of the **WebController** class that is in the **aivr_webcam.py** file, it then uses the class functions to send and toggle webcam feed. This function runs on a background **thread** so that other functions of the package can be utilised simeltaneously.     |
| switchColorMode() | This function is used for switching video display colors. By default the webcam transmission is in **R,G,B** format, this function can be used to change the colors of the webcam feed from **Grayscale** to **R,G,B** and viceversa. This function uses the same object as created in the toggleWebcamFeed function.     |
| colorChecker(color_tuple) | Takes in a tuple representing a color in terms of R,G,B values, the function check if the tuple has three digits and that if each digit has a value between 0 and 1. This function returns the color tuple in the form of a string, to be passed to the Unity environment as the objects color.    |
| _spawn_Position_Checker(spawn_pos) | Private helper function to check the validity of user entered spawn position for objects.  |
| _object_scale_checker(obj_scale) | Private helper function to check the validity of user entered scale for objects.  |
| _object_rotation_checker(obj_rot) | Private helper function to check the validity of user entered rotation for objects. This function returns a default value if input is wrong or it returns the user input. |

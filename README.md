# AIVR package
Introducing AIVR, a comprehensive Python package that seamlessly amalgamates the robust functionalities of Tensorflow, OpenCV, and ZMQ for enhanced machine learning integration within the Unity environment. AIVR acts as a unified bridge between Python-based machine learning projects and Unity, allowing developers to effortlessly connect, control, and dynamically interact with the Unity environment. With Tensorflow, users can deploy state-of-the-art machine learning models for AI-driven behaviors in Unity. The OpenCV integration empowers developers to seamlessly process camera inputs, conduct image analysis, and implement computer vision tasks. Utilizing ZMQ communication, AIVR facilitates real-time data exchange between Python scripts and Unity, enabling dynamic control of game objects and synchronization of machine learning processes. This versatile package further provides streamlined functionalities for creating game objects, streaming camera inputs, and dynamically manipulating Unity scenes based on machine learning outcomes. AIVR emerges as an indispensable tool, fostering a harmonious synergy between machine learning and Unity development, offering unparalleled flexibility and creativity for developers across various applications. The Unity Module that acts as a counterpart to the AIVR package can be accessesd from this [repository](https://github.com/kgdash116/AIVR---Unity-Project).

## Table of Contents

- [Team](#team)
- [Package](#package)
- [Installation](#installation)
- [Concept](#concept)
- [Usage](#usage)
- [Methods](#methods)


## Team

Meet the team mebers involved in fabricating the AIVR open-source package
Name | Photo | Role | Email
---- | ----- | ---- | ----
Harry Li | <img src="https://user-images.githubusercontent.com/38079632/227462713-9f9a5f60-e869-4c92-a653-98c1e6af724f.jpg" width="100" height="100"> | Project Supervisor & Architect | hua.li@sjsu.edu
Yusuke Yakuwa | <img src="https://user-images.githubusercontent.com/38079632/227462162-c2182a3b-e310-4b65-8d48-9ce06d7f87dd.jpg" width="100" height="100"> | Industrial Advisor | yusuke.yakuwa@ctione.com
Waqas Kureshy | <img src="https://github.com/kgdash116.png" width="100" height="100">| Lead Developer | waqas.kureshy319@gmail.com / waqas.kureshy@sjsu.edu
Prabjyot Obhi | <img src="https://github.com/kgdash116/AIVR---Unity-Project/blob/main/Unity%20screenshots/image_50404609.JPG?raw=true" width="80" height="100" > | Developer | prabjyot.obhi@sjsu.edu


## Package

<pre>
  .
├── LICENSE
├── README.md
├── aivr
│   ├── __init__.py
│   ├── __main__.py
│   ├── __pycache__
│   ├── aivr.py
│   ├── aivr_webcam.py
│   └── data.json 
│   
├── aivr_v1
├── env
│   ├── Include
│   ├── Lib
│   ├── Scripts
│   └── pyvenv.cfg
├── requirements.txt
├── setup.cfg
└── setup.py

</pre>

The above image represents the directory structure for the aivr package.

<p align="center"> <img src="https://github.com/kgdash116/aivr-project/blob/main/Images/AIVR%20Python%20package%20diagram%20ALT%20colors.png?raw=true"> </p>

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
  python3 -m pip install .     

  ```
- Now the package is installed on your local machine.

- To install the **aivr package** without creating a virtual environment, open the terminal.

- Type in the following command, and change the YOUR-PATH segment to wherever the **aivr-project** folder is located

```
python3 -m pip install YOUR-PATH/aivr-project .
```

## Concept

### Placing Objects

<p align="center">
  <img src="https://github.com/kgdash116/aivr-project/blob/main/Images/placeObject%20flow%20diagram%20with%20border.drawio.png?raw=true">
</p>

The AIVR package offers functionality to create all Unity related 3-Dimensional Game Objects through independent methods. These methods run on independent socket connections following the Pub-Sub design pattern. The list of objects includes Sphere, Cube, Capsule, Quad, Plane and Cylinder.

### Placing Text

<p align="center">
  <img src="https://github.com/kgdash116/aivr-project/blob/main/Images/placeText%20flow%20diagram.drawio.png?raw=true">
</p>

AIVR package supports adding text on Unity, with complete control over its 
attributes which are related to spawn position, text font size, text color etc. This operation is also 
conducted using the Publisher-Subscriber Socket configuration, where AIVR assumes the
Publisher connection and Unity’s text handler binds itself with the AIVR package as a Subscriber, 
subscribed to the “aivr” topic. This operation runs on an independent connection. The flow 
diagram below illustrates this operation.

### Sharing Camera Feed

<p align="center">
  <img src="https://github.com/kgdash116/aivr-project/blob/main/Images/aivrwebcamflowchart.png?raw=true">
</p>

This component of the AIVR package is used for sending camera 
streaming data to Unity. This component is controlled by the WebController class, and is ran on an 
independent daemon thread. This operation is controlled through the toggleWebcamFeed( ) 
method which in turn, creates an object of the WebController class and runs it on a background 
thread. The camera output display i.e. ON/OFF control is conducted through the same function. 
Furthermore, the AIVR package has support for toggling the camera color mode transmission i.e. 
frames can be either in Grayscale or R, G, B format. The flowchart below illustrates the 
functioning of the camera input feed handled through the AIVR package, paired up with its Unity
counterpart module.

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
| ------------- |:-------------|
| `placeCube(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)`      | <ul><li>Is used for placing a <strong>cube</strong> in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5, 0.5, 0.5) as a parameter.</li></ul>|
| `placeCapsule(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)` | <ul><li>Is used for placing a <strong>capsule 3D object</strong> in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `placeCylinder(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)` | <ul><li>Is used for placing a <strong>3D cylinder</strong> in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `placeSphere(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)` | <ul><li>Is used for placing a <strong>3D sphere</strong> in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `placeQuad(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)` | <ul><li>Is used for placing a <strong>3D Quad</strong> element in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `placePlane(conn_string, color=RED, object_name=None, spawn_position_input=None, scale_input=None, object_rotation=None)` | <ul><li>Is used for placing a <strong>plane</strong> in the Unity environment.</li><li>Takes various input parameters like object scale, object spawn position, color for the object, rotation for the object, and a connection string to make a socket connection to the Receiver socket.</li><li>If these parameters are not passed as parameters, the user is prompted to add these parameters as user input.</li><li>The color parameter of the function accepts a tuple, the object_name parameter should be a string, and the rest of the parameters (spawn-position_input, scale_input, and object_rotation) should be strings with three digits separated by commas like <strong>"2,2,2"</strong>.</li><li>This function then processes the user's input with the help of helper functions to check input validity.</li><li>The user has the ability to change the color of the object; the default color is set to <strong>RED</strong>.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like <strong>aivr.YELLOW</strong> or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `placeObjectWithJson()` | <ul><li>This method is used for passing a number of creating all sorts of 3D objects in the Unity environment with the help of JSON in one go.</li><li>This method does not take any parameters.</li><li>When this method is called, the user is asked for a path to the JSON file that contains the object-related data.</li><li>It checks for an array named **objects**, and furthermore checks for objects such as **object_type**, **spawn_position**, **object_name**, **object_rotation**, **object_scale**, and **object_color** inside the **objects** array.</li><li>This function parses the **JSON** file for these key value pairs and then passes along these parameters to their relevant functions based on the **object_type** parameter.</li><li>Further processing of validity of data is done in each object's own function.</li></ul>|
| `placeText(conn_string, color=RED)` | <ul><li>This method is used for passing user input based text to the Unity environment.</li><li>It takes the **CONNECTION_STRING** and **color** as parameters.</li><li>When invoked, it prompts the user to enter the **spawn_position**, **font_size**, and the **text to display**.</li><li>It then checks the validity of the user input with the help of private helper functions.</li><li>The user has the ability to change the color of the text; the default color is set to **RED**.</li><li>To choose a specific color, the user can pass one of the declared color constants as a parameter input like **aivr.YELLOW** or pass a color tuple with 3 values like for e.g (0.5,0.5,0.5) as a parameter.</li></ul>|
| `sendVidLink(conn_string)` | <ul><li>This method is used for passing a file path of a video element to the Unity environment.</li><li>It takes the **CONNECTION_STRING** as a parameter which is declared as a constant in the aivr.py file.</li><li>When invoked, it prompts the user to enter a file path for the video, and then it checks the validity of the path.</li><li>It prompts the user for the dimensions and the spawn position of the video object to display as well.</li><li>If the path is valid, it sends the path to the Unity environment, where it is then parsed and the video is rendered onto Unity based on the user-provided coordinates.</li></ul>|
| toggleWebcamFeed() | <ul><li>Is used for turning toggling the webcam feed.</li><li>This method can be used for the transmission of video byte frames obtained from the webcam input to the Unity environment.</li><li>This same function can be used for toggling webcam feed **ON/OFF**.</li><li>This function uses the **OpenCV** library to open the user's webcam, extract frames, convert it into bytes, and then pass them over to the Unity environment, using a dedicated Publisher-Subscriber socket connection.</li><li>This function makes an object of the **WebController** class that is in the **aivr_webcam.py** file, it then uses the class functions to send and toggle webcam feed.</li><li>This function runs on a background **thread** so that other functions of the package can be utilized simultaneously.</li></ul>|
| switchColorMode() | <ul><li>This function is used for switching video display colors.</li><li>By default, the webcam transmission is in **R,G,B** format, this function can be used to change the colors of the webcam feed from **Grayscale** to **R,G,B** and vice versa.</li><li>This function uses the same object as created in the toggleWebcamFeed function.</li></ul>|
| colorChecker(color_tuple) | <ul><li>Takes in a tuple representing a color in terms of R,G,B values.</li><li>The function checks if the tuple has three digits and that each digit has a value between 0 and 1.</li><li>This function returns the color tuple in the form of a string, to be passed to the Unity environment as the object's color.</li></ul>|
| _spawn_Position_Checker(spawn_pos) | <ul><li>Private helper function to check the validity of user-entered spawn position for objects.</li></ul>|
| _object_scale_checker(obj_scale) | <ul><li>Private helper function to check the validity of user-entered scale for objects.</li></ul>|
| _object_rotation_checker(obj_rot) | <ul><li>Private helper function to check the validity of user-entered rotation for objects.</li><li>This function returns a default value if the input is wrong or it returns the user input.</li></ul>|

## Note
A sample data.json file has been provided that works with the `placeObjectWithJson()` function inside the aivr folder.





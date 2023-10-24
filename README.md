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
    python
    ```
- A Python interpreter will open up. To import the aivr package, type in the following command:
    ```
    import aivr
    ```
- The line above will import the **aivr package**.
- Now methods of the aivr module can be utilised.
- For example, to make a cube in the Unity environment, type in the following command:
    ```
    aivr.placeObject()
    ```
- When this is executed, a prompt appears which asks the user to input the coordinates where the cube is to be placed and so forth.
- **Integration with Unity**: Assuming, Unity is installed, open the Unity environment and open the project named:
    ```
    Python-OpenCV-2022-2-16
    ```
- Next, click on the play button, to enter game mode.
- Now simultaneously the user can launch a python script and make use of the **aivr module** methods.

## Methods:

- The following methods in the aivr module along with their description are given below:

| Method        | Description           |
| ------------- |:-------------:|
| placeObject(connection_string, color)      | Used for placing a cube in the Unity environment, once called the user is prompted to enter coordinates separated by commas in the x,y,z format. After, this the user is asked to enter the scale of the cube in terms of length, width and height. |
| placeText(connection_string)      |  Used for placing a text in the Unity environment, once called, the user is prompted to enter coordinates separated by commas in the x,y,z format to place the text at. After, this the user is asked to enter the font size and then finally a prompt is shown to enter the text.   |
| getCam() | Used for displaying the webcam feed in the Unity environment, by default the webcam output is in RGB, the user can toggle the webcam output to grayscale by pressing the 'g' key. To quit the webcam feed display the user has to press the 'q' key.      |  
| colorChecker(color_tuple) | Takes in a tuple representing a color in terms of R,G,B values, the function check if the tuple has three digits and that if each digit has a value between 0 and 1. This function returns the color tuple in the form of a string, to be passed to the Unity environment as the objects color.    |
| placeObjectWithJson(connection_string) | This method is used for passing a number of objects to Unity environment with the help of JSON. This method takes the connection string as a parameter. If this method is used, the user is asked for a path to the JSON file that contains the object related data. It checks for an array named **objects**, and furthermore checks for objects such as **spawn_position** , **object_name**, **object_scale** and **object_color**. It performs checks for all the values that wether they comply to certain thresholds, and then passes them as a message to the unity environment.    |    

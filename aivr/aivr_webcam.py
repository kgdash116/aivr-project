'''--------------------------------------------------------------------------------------------------------------------
Program name : aivr_webcam.py (Testing)
Coded By     : Waqas Kureshy
Date         : 2023-11-29
Updated By   :
Date         :
Version      : v 0.1.1
Copyright    : Copyright (c) 2023 Waqas Kureshy
Purpose      : This script contains the WebController class, this class is used for controlling the webcam feed transmission.
               It supports toggling the webcam feed as well as switching from RGB to Grayscale and vice-versa. 
----------------------------------------------------------------------------------------------------------------------'''



import sys
import zmq
import cv2
import os
import threading

class WebcamController:
    '''WebController class for controlling webcam feed, this class supports turning the feed on/off'''
    '''It also supports RGB and Grayscale feed transmission.'''
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
        '''Private function for toggling webcam feed'''
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
        '''Private function for toggling Graysccale feed.'''
        self.isGrayScaleEnabled= not self.isGrayScaleEnabled

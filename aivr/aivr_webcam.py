import threading
import zmq
import cv2

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
            self.socket.send(b'STOP')

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



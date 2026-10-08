# Python Mini Projects

A small collection of Python and browser experiments with games, computer vision, hand tracking, and an Arduino input.

## Projects

| Project | What it does | Main requirements |
| --- | --- | --- |
| Air Canvas | Draw and erase in the air using hand gestures seen by a webcam. | Python, OpenCV, MediaPipe, NumPy, webcam |
| Keyboard Car Game | Dodge traffic using the left and right arrow keys. | Python, Pygame |
| Potentiometer Car Game | Steer a car game with a potentiometer connected to an Arduino. | Python, Pygame, pySerial, Arduino sending one integer reading per line |
| Webcam Rock Paper Scissors | Play by showing a hand gesture to the webcam. | Python, OpenCV, MediaPipe, webcam |
| Gesture Earth | Rotate and zoom a 3D globe with hand gestures, select countries with a pinch, or use the mouse. | Modern browser, internet, webcam for gestures |

## Run a project

Install the requirements for the project you want to run:

- Keyboard Car Game: `python -m pip install pygame`
- Air Canvas and Webcam Rock Paper Scissors: `python -m pip install opencv-python mediapipe numpy`
- Potentiometer Car Game: `python -m pip install pygame pyserial`

Then open that project's folder and run `python main.py` from a terminal. Webcam projects need a working camera. Press **Esc** to exit; Air Canvas also uses **C** to clear the drawing.

### Gesture Earth

Open a terminal in the repository folder and run `python -m http.server 8000`. Visit `http://localhost:8000/gesture-earth/` in a modern browser. Allow camera access to use hand controls. The project also supports mouse drag, scroll, and click, and loads its JavaScript libraries and country data from public CDNs, so internet access is required.

### Arduino note

The Potentiometer Car Game expects the Arduino to send a whole number from 0 to 1023, one reading per line, at 9600 baud. The original project folder did not include the matching Arduino sketch. In `main.py`, change `COM3` to the port shown for your board if needed.

## Project status

These are small learning projects. The code is written through an iterative workflow combining local AI generation with manual code restructuring and error handling. Hardware behavior depends on the connected Arduino and components. Gesture Earth is a browser project grouped here at the owner's request; it is written in HTML and JavaScript rather than Python.

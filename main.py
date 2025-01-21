# main.py
import cv2 as cv
from filled_shape import capture as detect_shape
from shape_prompt import prompt_for_shape, match_shapes
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cam", "-c", dest='cam', default=False, action='store_true', help="Use cam as source")
parser.add_argument("--debug", default=False, action='store_false', help="show more contours and points")

arg = parser.parse_args()

if arg.cam:
    requested_shape = prompt_for_shape()  # Step 1: Prompt user for shape
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            # Step 2: Detect the shape from the camera feed
            detected_shape = detect_shape(frame, arg.debug)
            
            # Step 3: Check if the detected shape matches the requested shape
            if match_shapes(requested_shape, detected_shape):
                print(f"Success! You made a {detected_shape}")
                break  # Stop once the correct shape is detected
            else:
                print(f"Detected {detected_shape}, waiting for {requested_shape}...")

        k = cv.waitKey(30) & 0xFF
        if k == 27:  # Exit on pressing 'ESC'
            break
    cap.release()
    cv.destroyAllWindows()
else:
    parser.parse_args(['--help'])

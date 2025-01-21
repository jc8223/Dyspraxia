from flask import Flask, render_template, request, jsonify
import cv2 as cv
import time
from filled_shape import capture as detect_shape
from shape_prompt import match_shapes
import pyttsx3 


app = Flask(__name__)
engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('challengeone.html')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

    

@app.route('/detect_shape', methods=['POST'])
def detect_shape_api():
    requested_shape = request.json.get('shape')
    
    # Open the camera
    cap = cv.VideoCapture(0)
    detected_shape = "undefined"
    
    # Prompt user to draw the shape and manually select ROI
    print(f"Please draw the shape: {requested_shape}.")
    
    # Make the capture photo button visible
    print("Press ENTER to capture the photo.")
    while True:
        ret, frame = cap.read()
        if not ret:
            result = "Error accessing the camera."
            return jsonify({'result': result})
        
        cv.imshow("Draw Shape", frame)
        k = cv.waitKey(1) & 0xFF
        if k == 13:
            break
    cv.destroyAllWindows()
    # Allow the user to manually select the ROI
    print("Select the region of interest (ROI) for analysis, then press ENTER.")
    roi = cv.selectROI("Select ROI", frame, showCrosshair=True)
    cv.destroyWindow("Select ROI")  # Close the ROI window once selection is done

    # Crop the frame to the selected ROI
    x, y, w, h = map(int, roi)
    roi_frame = frame[y:y+h, x:x+w]


    # Analyze the cropped region (ROI)
    detected_shape = detect_shape(roi_frame)

    if match_shapes(requested_shape, detected_shape):
        result = f"Success! You made a {detected_shape}."
        speak("Hurray you have did it")
    else:
        result = f"Detected {detected_shape}, expected {requested_shape}."
        speak("Do it again")

    cap.release()
    cv.destroyAllWindows()

    # Return the result to the frontend
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

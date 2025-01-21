import cv2 as cv
import numpy as np

class FilledShape:
    def __init__(self, img):
        self.img = img

    def detect(self, contour, debug):
        shape = "undefined"
        epsilon = 0.03 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(contour)
        
        # Draw bounding box around the shape
        cv.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        font = cv.FONT_HERSHEY_SIMPLEX
        
        # Debug: draw contour points if needed
        if debug:
            cv.drawContours(self.img, [contour], 0, (0, 255, 0), 2)
            for pt in approx:
                cv.circle(self.img, (pt[0][0], pt[0][1]), 5, (255, 0, 0), -1)
        
        # Determine shape based on the number of contour points (approximation)
        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shape = "square"
            else:
                shape = "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"

        # Display shape name on the image
        cv.putText(self.img, shape, (x, y - 10), font, 0.6, (255, 255, 255), 2)
        return shape

    def preprocessing_image(self):
        # Convert to grayscale
        img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur to reduce noise
        blurred = cv.GaussianBlur(img_gray, (5, 5), 0)
        
        # Apply adaptive thresholding for better shape distinction
        threshold = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
        
        # Perform morphological operations to remove small noise
        kernel = np.ones((3, 3), np.uint8)
        threshold = cv.morphologyEx(threshold, cv.MORPH_CLOSE, kernel)
        
        # Detect contours
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        return threshold, contours

def capture(frame, debug=False):
    # Create an object of FilledShape class and process the image
    img_object = FilledShape(frame)
    threshold, contours = img_object.preprocessing_image()
    detected_shape = "undefined"

    # Iterate through contours and detect shapes
    for contour in contours:
        detected_shape = img_object.detect(contour, debug)

    # Show images for debugging (Threshold and Original)
    cv.imshow('Threshold', threshold)
    cv.imshow('Original', frame)

    # Debugging: Print detected shape
    print(f"Detected shape: {detected_shape}")
    
    return detected_shape

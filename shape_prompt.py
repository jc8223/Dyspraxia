# shape_prompt.py

def prompt_for_shape():
    print("Draw one of the following shapes: triangle, square, rectangle, pentagon, circle")
    shape = input("Please type the name of the shape you want to make: ").lower()
    return shape

def match_shapes(requested_shape, detected_shape):
    requested_shape = requested_shape.strip().lower()
    detected_shape = detected_shape.strip().lower()
    return requested_shape == detected_shape

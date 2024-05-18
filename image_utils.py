import cv2
from skimage import io
from skimage import io, measure
import matplotlib.pyplot as plt
import random
import numpy as np


def base_drawing_img(img_path):
    # Assuming 'img' is your loaded image
    img = io.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply GaussianBlur to reduce image noise in the edge detected image
    blurred_img = cv2.GaussianBlur(gray_img, (3, 3), 0)

    # Apply Canny Edge Detector
    edges = cv2.Canny(blurred_img, threshold1=60, threshold2=220)

    # Convert the grayscale image to black and white (binary)
    _, binary_img = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY_INV)

    # Convert the inverted image back to RGB for color text overlay
    bw_img_colored = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2RGB)

    gray_img_2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Convert the grayscale image to black and white (binary)
    _, binary_img_2 = cv2.threshold(gray_img_2, 50, 255, cv2.THRESH_BINARY)

    # Convert the inverted image back to RGB for color text overlay
    bw_img_colored_2 = cv2.cvtColor(binary_img_2, cv2.COLOR_GRAY2RGB)

    # Blending both images
    alpha = 0.5  # Weight of the first image
    beta = 1.0 - alpha  # Weight of the second image
    blended_img = cv2.addWeighted(bw_img_colored, alpha, bw_img_colored_2, beta, 0)
    return blended_img


def base_drawing_img_without_edge_detection(img_path: str):

    # Assuming 'img' is your loaded image
    img = io.imread(img_path)

    gray_img_2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Convert the grayscale image to black and white (binary)
    _, binary_img_2 = cv2.threshold(gray_img_2, 100, 255, cv2.THRESH_BINARY)

    # Convert the inverted image back to RGB for color text overlay
    bw_img_colored_2 = cv2.cvtColor(binary_img_2, cv2.COLOR_GRAY2RGB)

    return bw_img_colored_2


def process_img(img_path: str, outputs):
    print("Launching magic drawing script")
    img = io.imread(img_path)

    # Create a figure and a 1x2 grid of subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Display the original image on the first subplot
    axes[0].imshow(img)
    axes[0].set_title("Original Image")
    axes[0].axis("off")  # Turn off axis numbers and ticks

    blended_img = base_drawing_img_without_edge_detection(img_path)

    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    hues = [
        (0, 10),
        (11, 23),
        (24, 40),
        (41, 70),
        (71, 95),
        (96, 130),
        (131, 165),
        (166, 180),
    ]
    colors = ["red", "ora", "yel", "gre", "lblue", "dblue", "pur", "red"]
    values = outputs + [outputs[0]]

    for i, hue in enumerate(hues):
        print("Analyzing color " + str(colors[i]))
        min_hue = hue[0]
        max_hue = hue[1]
        mask = cv2.inRange(hsv, (min_hue, 20, 20), (max_hue, 255, 255))

        # Label connected components
        labels = measure.label(mask, connectivity=2)
        props = measure.regionprops(labels)

        # Define a minimum area threshold
        min_area = 1000  # Adjust this value to your needs

        # Filter regions based on area
        large_regions = [region for region in props if region.area > min_area]

        print("Number of large regions found " + str(len(large_regions)))

        # Process each of the five largest regions
        for idx, region in enumerate(large_regions, 1):
            # Get the centroid of each region
            y_centroid, x_centroid = np.mean([coord for coord in region.coords], axis=0)
            random_point = random.choice(region.coords)
            y, x = random_point  # coords are in (row, col) format, which maps to (y, x)

            # Convert centroid coordinates to integer for indexing and text placement
            # x, y = int(x), int(y)
            x, y = int(x_centroid), int(y_centroid)
            # Overlay text on the original image at the centroid of each mask
            cv2.putText(
                blended_img,
                values[i],
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2,
            )
    original_height, original_width = blended_img.shape[:2]
    # New dimensions
    # Desired max width and height
    max_width = 800
    max_height = 600

    # Calculate the scale factor while maintaining the aspect ratio
    scale_width = max_width / original_width
    scale_height = max_height / original_height
    scale = min(scale_width, scale_height)

    # New dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Resize the image
    resized_img = cv2.resize(blended_img, (new_width, new_height))

    return resized_img

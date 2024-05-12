import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, measure
from tkinter import Tk, Canvas, NW, Button, ttk
from PIL import Image, ImageTk
import random  # Import random for random selection
from image_utils import base_drawing_img, base_drawing_img_without_edge_detection, process_img


if __name__ == "__main__":
    # Create a window
    print("Tkinter app running")
    window = Tk()
    window.title("Magic Drawing")
    # Optionally change the overall theme
    window.configure(bg='white')
    window.attributes('-fullscreen', True)
    style = ttk.Style(window)
    style.theme_use('clam')  # Try different themes: 'alt', 'default', 'classic', 'clam', etc.

    # Define a style for buttons
    style.configure('TButton', font=('Helvetica', 12, 'bold'), foreground='white', background='purple', padding=10)

    # Convert the image to PIL format and then to ImageTk format
    cv_img = cv2.cvtColor(cv2.imread("drawing_4.png"), cv2.COLOR_BGR2RGB)
    original_height, original_width = cv_img.shape[:2]
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
    resized_img = cv2.resize(cv_img, (new_width, new_height))
    height, width, no_channels = cv_img.shape
    img = Image.fromarray(resized_img)
    imgtk = ImageTk.PhotoImage(image=img)

    # Set up a canvas and add the image to it
    # Setup the first canvas with the image
    canvas1 = Canvas(window, width=new_width, height=new_height)
    canvas1.grid(row=0, column=0)
    canvas1.create_image(0, 0, anchor=NW, image=imgtk)

    # Setup the second canvas as a placeholder
    canvas2 = Canvas(window, width=new_width, height=new_height, bg='grey')
    canvas2.grid(row=0, column=1)

    def update_canvas2():
        print("cc")
        processed_img = process_img()  # Get the processed image
        if processed_img is not None:
            # Convert the processed image to a format suitable for Tkinter
            processed_img = Image.fromarray(processed_img)
            imgtk2 = ImageTk.PhotoImage(image=processed_img)
            # Clear the previous image
            canvas2.delete("all")
            # Create new image on canvas2
            canvas2.create_image(0, 0, anchor=NW, image=imgtk2)
            # Important: keep a reference!
            canvas2.image = imgtk2

    # Add a button below the canvases
    button = ttk.Button(window, text="Process", command=update_canvas2, style='TButton')
    button.grid(row=1, column=0, columnspan=2)  # Span across both columns
    window.mainloop()  # Exits when the window is closed

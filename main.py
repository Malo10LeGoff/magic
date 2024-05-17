import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, measure
from tkinter import Tk, Canvas, NW, Button, ttk, Label, Listbox, filedialog, NW
from PIL import Image, ImageTk
import random  # Import random for random selection
from image_utils import (
    process_img,
)


def open_image(canvas, img_path):
    # Open file dialog and get the filename
    print("cc")
    file_types = [
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg"),
        ("JPEG files", "*.jpeg"),
    ]
    filepath = filedialog.askopenfilename(filetypes=file_types)
    img_path[0] = filepath
    print("here is the img path:" + img_path[0])
    if not filepath:  # If no file is selected
        return

    # Load the image using OpenCV
    cv_img = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)

    # Resize the image
    scale = min(
        canvas.winfo_width() / cv_img.shape[1], canvas.winfo_height() / cv_img.shape[0]
    )
    resized_img = cv2.resize(
        cv_img, (int(cv_img.shape[1] * scale), int(cv_img.shape[0] * scale))
    )

    # Convert to a format suitable for Tkinter
    img = Image.fromarray(resized_img)
    imgtk = ImageTk.PhotoImage(image=img)

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=NW, image=imgtk)
    canvas.image = imgtk  # Keep a reference to avoid garbage collection
    # Hide the button after the image is loaded


if __name__ == "__main__":
    # Create a window
    print("Tkinter app running")
    window = Tk()
    window.title("Magic Drawing")
    # Optionally change the overall theme
    window.configure(bg="white")
    window.attributes("-fullscreen", True)
    style = ttk.Style(window)
    style.theme_use(
        "clam"
    )  # Try different themes: 'alt', 'default', 'classic', 'clam', etc.

    # Define a style for buttons
    style.configure(
        "TButton",
        font=("Helvetica", 12, "bold"),
        foreground="white",
        background="purple",
        padding=10,
    )

    # Define a style for the label
    label_style = {
        "font": ("Helvetica", 16, "bold"),
        "foreground": "purple",
        "background": "white",
    }

    # Add a label at the top left
    label = Label(window, text="MagicProf", **label_style)
    label.grid(row=0, column=0, sticky="NW", padx=10, pady=10)

    # Configure grid column weights (0, 1, 2, 3 - four columns in total)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=2)
    window.columnconfigure(2, weight=2)
    window.columnconfigure(3, weight=1)

    # Set up a canvas and add the image to it
    # Setup the first canvas with the image
    canvas1 = Canvas(window, width=800, height=600)
    canvas1.grid(row=1, column=1, padx=(0, 30))

    # Define button to load images and add it to the canvas
    img_path = ["dummy"]
    load_button = ttk.Button(
        window, text="Upload Image", command=lambda: open_image(canvas1, img_path)
    )
    load_button.grid(row=0, column=1, pady=(0, 0))

    # Setup the second canvas as a placeholder
    canvas2 = Canvas(window, width=800, height=600, bg="grey")
    canvas2.grid(row=1, column=2, padx=(30, 0))

    # Listbox for color selection
    color_list = Listbox(window, height=10, width=15, bg="white", exportselection=0)
    colors = [
        "Red",
        "Blue",
        "Green",
        "Yellow",
        "Purple",
        "Orange",
    ]  # Add more colors as needed
    for color in colors:
        color_list.insert("end", color)
    color_list.grid(row=2, column=0, sticky="W", padx=10)

    def update_canvas2():
        print("cc")
        processed_img = process_img(img_path[0])  # Get the processed image
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
    button = ttk.Button(window, text="Process", command=update_canvas2, style="TButton")
    button.grid(row=2, column=1)  # Span across both columns
    window.mainloop()  # Exits when the window is closed

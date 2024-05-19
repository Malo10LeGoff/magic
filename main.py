import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, measure
from tkinter import Tk, Canvas, NW, Button, ttk, Label, Frame, filedialog, NW, Entry
from PIL import Image, ImageTk
import random  # Import random for random selection
from image_utils import (
    process_img,
)


def focus_entry(event):
    print("focusing mf")
    event.widget.focus_set()


def retrieve_entries(entries, outputs):
    # This function retrieves the content of all entries
    for index, entry in enumerate(entries, start=1):
        user_input = entry.get()  # Get the content of the entry
        outputs.append(user_input)
        print(f"Content of Entry {index}: {user_input}")


def save_image(processed_img):
    # Ensure there is an image to save
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filepath:  # If a file path is provided
        processed_img.save(filepath)  # Save the image
        print("Image saved successfully at:", filepath)


def open_image(canvas, img_path):
    # Open file dialog and get the filename
    print("ccooo")
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
    window.columnconfigure(0, weight=1, minsize=100)
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
    
    # Frame to hold the entries and labels
    entry_frame = Frame(window, bg="white")
    entry_frame.grid(row=3, column=1, sticky="ew")

    # Labels and entries
    outputs = []
    entries = []
    colors = ["Red", "Orange", "Yellow", "Green", "Light Blue", "Dark Blue", "Purple"]
    for i, color in enumerate(colors, start=1):
        label = Label(entry_frame, text=f"{color}:", font=('Arial', 12), bg='white', fg='black')
        label.grid(row=i, column=0, sticky='e', padx=(10, 2), pady=5)

        entry = Entry(entry_frame, font=('Arial', 12), bg='white', fg='black')
        entry.config(state='normal')
        entry.grid(row=i, column=1, sticky='ew', padx=(2, 10), pady=5)
        entry.bind("<Button-1>", focus_entry)

        entries.append(entry)
    
    entry_frame.columnconfigure(1, weight=1)

    img_tbd = []

    def update_canvas2(img_tbd):
        retrieve_entries(entries=entries, outputs=outputs)
        processed_img = process_img(img_path[0], outputs)  # Get the processed image
        if processed_img is not None:
            # Convert the processed image to a format suitable for Tkinter
            processed_img = Image.fromarray(processed_img)
            img_tbd.append(processed_img)
            imgtk2 = ImageTk.PhotoImage(image=processed_img)
            # Clear the previous image
            canvas2.delete("all")
            # Create new image on canvas2
            canvas2.create_image(0, 0, anchor=NW, image=imgtk2)
            # Important: keep a reference!
            canvas2.image = imgtk2

    # Add a button below the canvases
    button = ttk.Button(window, text="Process", command=lambda: update_canvas2(img_tbd=img_tbd), style="TButton")
    button.grid(row=3, column=2)  # Span across both columns

    # Add a button to save the processed image
    save_button = ttk.Button(window, text="Download Image", command=lambda: save_image(img_tbd[0]), style="TButton")
    save_button.grid(row=4, column=2)  # Positioned below the process button
    window.mainloop()  # Exits when the window is closed

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog
import os


class ImageHandler:
    def __init__(self, ImageAnnotationTool):
        self.ImageAnnotationTool = ImageAnnotationTool

    def open_image(self):
        self.ImageAnnotationTool.annotation_handler.save_txt()
        self.ImageAnnotationTool.save_annotated_image()

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.webp")])
        if file_path:
            self.ImageAnnotationTool.image_path = file_path
            self.load_image()

    def load_image(self):
        try:
            if self.ImageAnnotationTool.image_path:
                print("Loading Image")
                self.ImageAnnotationTool.canvas.delete("all")
                self.ImageAnnotationTool.annotations_history = []  # Reset annotation history when loading a new image
                self.ImageAnnotationTool.AnnotationEditor.update_list()
                self.ImageAnnotationTool.box_counter = 1  # Reset box counter
                self.ImageAnnotationTool.original_image = Image.open(self.ImageAnnotationTool.image_path)
                self.update_displayed_image()
                self.ImageAnnotationTool.image_name = os.path.splitext(os.path.basename(self.ImageAnnotationTool.image_path))[0]
                self.ImageAnnotationTool.txt_file_path = os.path.join("annotations_txt", f"{self.ImageAnnotationTool.image_name}_annotations.txt")
                self.ImageAnnotationTool.Rectangles.raise_rectangle()
        except Exception as e:
            print(f"Error opening image '{self.ImageAnnotationTool.image_path}': {e}")

    def load_selected_image(self, event):
        self.ImageAnnotationTool.annotation_handler.save_txt()
        self.ImageAnnotationTool.save_annotated_image()
        selected_index = self.ImageAnnotationTool.listbox_images.curselection()
        if selected_index:
            selected_image = self.ImageAnnotationTool.listbox_images.get(selected_index)
            self.ImageAnnotationTool.image_path = os.path.join(self.ImageAnnotationTool.image_directory, selected_image)
            self.load_image()

    def update_displayed_image(self):
        print("Updating")
        # Calculate scaling factors for width and height
        width_factor = self.ImageAnnotationTool.canvas.winfo_width() / self.ImageAnnotationTool.original_image.width
        height_factor = self.ImageAnnotationTool.canvas.winfo_height() / self.ImageAnnotationTool.original_image.height

        # Choose the minimum scaling factor to fit the image in the canvas
        scale_factor = min(width_factor, height_factor)

        # Resize the image
        resized_image = self.ImageAnnotationTool.original_image.resize(
            (int(self.ImageAnnotationTool.original_image.width * scale_factor), int(self.ImageAnnotationTool.original_image.height * scale_factor)),
        )

        # Update the Tkinter PhotoImage object on the canvas
        self.image = ImageTk.PhotoImage(resized_image)
        self.ImageAnnotationTool.canvas.config(scrollregion=self.ImageAnnotationTool.canvas.bbox(tk.ALL))
        self.ImageAnnotationTool.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        self.ImageAnnotationTool.Rectangles.raise_rectangle()

    def on_window_resize(self, event):
        if self.ImageAnnotationTool.image_path:
            self.update_displayed_image()

import os
import tkinter as tk
from tkinter import filedialog


class DirectoryHandler:
    def __init__(self, ImageAnnotationTool):
        self.ImageAnnotationTool = ImageAnnotationTool
        self.annotated_images_directory = "annotated_images"
        self.annotations_txt_directory = "annotations_txt"

    def create_directories(self):
        # Check and create the annotated images directory if it doesn't exist
        if not os.path.exists(self.annotated_images_directory):
            os.makedirs(self.annotated_images_directory)
            print(f"Created directory: {self.annotated_images_directory}")

        # Check and create the annotations_txt directory if it doesn't exist
        if not os.path.exists(self.annotations_txt_directory):
            os.makedirs(self.annotations_txt_directory)
            print(f"Created directory: {self.annotations_txt_directory}")

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.ImageAnnotationTool.image_directory = folder_path
            self.ImageAnnotationTool.listbox_images.delete(0, tk.END)
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
            self.ImageAnnotationTool.listbox_images.insert(tk.END, *image_files)

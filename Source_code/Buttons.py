import tkinter as tk
from tkinter import ttk, filedialog

class Buttons:

    def __init__(self, ImageAnnotationTool):
        self.ImageAnnotationTool    = ImageAnnotationTool
        self.BUTTON_WIDTH           = self.ImageAnnotationTool.BUTTON_WIDTH

    def create_buttons(self, lower_left_frame):
        self.open_folder(lower_left_frame)
        self.open_image(lower_left_frame)
        self.save_annotated_image(lower_left_frame)
        self.Next_image(lower_left_frame)
        self.add_class(lower_left_frame)
    
    def open_folder(self, lower_left_frame):
        self.button_open_folder = ttk.Button(lower_left_frame, text="Open Folder", command=self.ImageAnnotationTool.DirectoryHandler.open_folder, width=self.BUTTON_WIDTH)
        self.button_open_folder.pack(side=tk.BOTTOM, padx=5, pady=5)

    def open_image(self, lower_left_frame):
        self.button_open = ttk.Button(lower_left_frame, text="Open Image", command=self.ImageAnnotationTool.ImageHandler.open_image, width=self.BUTTON_WIDTH)
        self.button_open.pack(side=tk.BOTTOM, padx=5, pady=5)

    def save_annotated_image(self, lower_left_frame):
        self.button_save_annotated_image = ttk.Button(lower_left_frame, text="Save Annotated Image", command=self.ImageAnnotationTool.save_annotated_image, width=self.BUTTON_WIDTH)
        self.button_save_annotated_image.pack(side=tk.BOTTOM, padx=5, pady=5)

    def Next_image(self, lower_left_frame):
        self.button_Next_image = ttk.Button(lower_left_frame, text="Next Image", command=self.ImageAnnotationTool.image_navigator.load_next_image, width=self.BUTTON_WIDTH)
        self.button_Next_image.pack(side=tk.BOTTOM, padx=5, pady=5)

    def add_class(self, lower_left_frame):
        self.button_add_class = ttk.Button(lower_left_frame, text="Add Class", command=self.ImageAnnotationTool.ClassSelector.add_class, width=self.BUTTON_WIDTH)
        self.button_add_class.pack(side=tk.BOTTOM, padx=5, pady=5)

    

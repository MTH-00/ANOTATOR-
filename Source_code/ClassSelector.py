import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkcolorpicker import askcolor

class ClassSelector:
    def __init__(self, ImageAnnotationTool):
        self.ImageAnnotationTool = ImageAnnotationTool
        self.class_labels = ["Animal", "Human", "Car"]  # Default class labels
        self.class_colors = {
            "Animal": "red",
            "Human": "green",
            "Car": "blue"
        }  # Default class colors

    def menu(self, frame):
        # Combobox for selecting existing classes
        self.combobox_class = ttk.Combobox(frame, values=self.class_labels)
        self.combobox_class.pack(side=tk.BOTTOM, anchor=tk.W)
        self.combobox_class.set("Animal")  # Set default class

        # Label for displaying "Select Class:"
        self.label_class = ttk.Label(frame, text="Select Class:")
        self.label_class.pack(side=tk.BOTTOM, anchor=tk.W)

    def add_class(self):
        new_class = simpledialog.askstring("Add Class", "Enter the name of the new class:")
        if new_class and new_class not in self.class_labels:
            # Ask the user to pick a color for the new class
            color, _ = askcolor(parent=self.ImageAnnotationTool.master, title=f"Choose Color for {new_class}")

            if color:
                color_str = "#{:02X}{:02X}{:02X}".format(int(color[0]), int(color[1]), int(color[2]))
                self.class_labels.append(new_class)
                self.class_colors[new_class] = color_str
                print(f"Class '{new_class}' added with color '{color}'!")

                print(self.class_colors)
                self.update_class_menu()
            else:
                messagebox.showwarning("Warning", "Color selection canceled.")
        else:
            # Display a warning if the class already exists or the user canceled the input
            if new_class:
                warning_message = f"Class '{new_class}' already exists. Please choose a different name."
            else:
                warning_message = "Class addition canceled."
            messagebox.showwarning("Warning", warning_message)

    def update_class_menu(self):
        current_value = self.combobox_class.get()
        self.combobox_class['values'] = list(self.class_colors.keys())
        self.combobox_class.set(current_value)

import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcolorpicker import askcolor
from tkinter import ttk

class TwoButtonPopup:
    def __init__(self, master, message, image_annotation_tool):
        self.result = None
        self.image_annotation_tool = image_annotation_tool
        self.master = master

        # Create Label for the message
        self.label = tk.Label(master, text=message)
        self.label.pack(side=tk.LEFT, pady=0)

        # Create Delete Button
        self.delete_button = tk.Button(master, text="Delete", command=self.image_annotation_tool.AnnotationEditor.delete_annotation)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=15)

        # Create Relabel Button
        self.relabel_button = tk.Button(master, text="Relabel", command=self.image_annotation_tool.AnnotationEditor.relabel_annotation)
        self.relabel_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def on_close(self):
        self.master.grab_release()
        self.master.destroy()
        self.image_annotation_tool.Rectangles.draw_rectangles()



class AnnotationEditor:
    def __init__(self, image_annotation_tool):
        self.image_annotation_tool = image_annotation_tool
        self.selected_index = 0
        self.selected_annotation = 0
        self.TwoButtonPopup = None

    def Annotation_list(self, frame):
        # Create a Listbox to display annotations
        self.listbox_annotations = tk.Listbox(frame, height=13)
        self.listbox_annotations.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox_annotations.bind("<ButtonRelease-1>", self.select_annotation)

        # Add a scrollbar to the Listbox
        scrollbar = tk.Scrollbar(frame, command=self.listbox_annotations.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_annotations.config(yscrollcommand=scrollbar.set)

    def update_list(self):
        # Clear existing items in the listbox
        self.listbox_annotations.delete(0, tk.END)

        # Iterate over annotations_history and add each annotation to the listbox
        for i, (box, label) in enumerate(self.image_annotation_tool.annotations_history):
            label_and_box = f"{label}-{i + 1}"
            self.listbox_annotations.insert(tk.END, label_and_box)

        print("Listbox updated with annotations from annotations_history.")

    def select_annotation(self, event):
        self.selected_index = self.listbox_annotations.nearest(event.y)
        print(self.selected_index + 1)
        if (self.selected_index + 1):
            self.selected_annotation = self.listbox_annotations.get(self.selected_index)
            print(self.selected_annotation)
            self.create_popup()

    def create_popup(self):
        # Create popup for annotation editing
        root = tk.Tk()
        root.title("Annotation Editor")


        # Calculate the position to center the dialog
        width = 300  # Adjust the width as needed
        height = 100  # Adjust the height as needed
        x = (self.image_annotation_tool.master.winfo_screenwidth() - width) // 2
        y = (self.image_annotation_tool.master.winfo_screenheight() - height) // 2

        self.TwoButtonPopup = TwoButtonPopup(root, f"Selected annotation: {self.selected_annotation}\n\nChoose an option:", self.image_annotation_tool)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.mainloop()

    def delete_annotation(self):
        # Check if a valid index is selected
        if self.selected_index is not None:
            # Remove the annotation at the selected index from annotations_history
            if 0 <= self.selected_index < len(self.image_annotation_tool.annotations_history):
                deleted_annotation = self.image_annotation_tool.annotations_history.pop(self.selected_index)
                print(f"Deleted annotation: {deleted_annotation}")

                # Close the TwoButtonPopup
                self.TwoButtonPopup.on_close()

                # Update the listbox
                self.update_list()

                print(self.image_annotation_tool.annotations_history)
                self.image_annotation_tool.Rectangles.draw_rectangles()
            else:
                print("Invalid selected index.")
        else:
            print("No annotation selected.")

    def relabel_annotation(self):
        print(f"{self.selected_index} Rela")

        # Get the existing class of the selected annotation
        existing_class = self.image_annotation_tool.annotations_history[self.selected_index][1]

        # Ask the user whether to choose from existing classes or create a new class
        choice = messagebox.askquestion("Relabel Annotation", f"Do you want to relabel to an existing class or create a new class?\n\nExisting class: {existing_class}")

        if choice == 'yes':  # User chooses to relabel to an existing class
            # Center the dialog window on the screen
            dialog = tk.Toplevel(self.image_annotation_tool.master)
            dialog.title("Select Existing Class")

            # Calculate the position to center the dialog
            dialog_width = 300  # Adjust the width as needed
            dialog_height = 100  # Adjust the height as needed
            dialog_x = (self.image_annotation_tool.master.winfo_screenwidth() - dialog_width) // 2
            dialog_y = (self.image_annotation_tool.master.winfo_screenheight() - dialog_height) // 2

            # Set the geometry to center the dialog
            dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")

            # Combobox for selecting existing classes
            self.combobox_class = ttk.Combobox(dialog, values=self.image_annotation_tool.ClassSelector.class_labels)
            self.combobox_class.set(existing_class)  # Set default value to existing class
            self.combobox_class.pack(padx=10, pady=10)

            # Button to confirm the selection
            confirm_button = tk.Button(dialog, text="OK", command=lambda: self.handle_existing_class_selection(self.combobox_class.get(), dialog))
            confirm_button.pack(pady=10)
            self.update_list()
        else:  # User chooses to create a new class
            new_class = simpledialog.askstring("Relabel Annotation", "Enter the name of the new class:")

            if new_class and new_class not in self.image_annotation_tool.ClassSelector.class_labels:
                # Ask the user to pick a color for the new class
                color, _ = askcolor(parent=self.image_annotation_tool.master, title=f"Choose Color for {new_class}")

                if color:
                    color_str = "#{:02X}{:02X}{:02X}".format(int(color[0]), int(color[1]), int(color[2]))
                    self.image_annotation_tool.ClassSelector.class_labels.append(new_class)
                    self.image_annotation_tool.ClassSelector.class_colors[new_class] = color_str
                    print(f"Class '{new_class}' added with color '{color}'.")
                    self.image_annotation_tool.ClassSelector.update_class_menu()

                    # Update the class label in the annotations_history
                    self.image_annotation_tool.annotations_history[self.selected_index] = (
                        self.image_annotation_tool.annotations_history[self.selected_index][0], new_class
                    )
                    print(f"Relabeled annotation to '{new_class}'.")
                    self.image_annotation_tool.Rectangles.draw_rectangles()
                    self.update_list()
                else:
                    messagebox.showwarning("Warning", "Color selection canceled.")
            else:
                messagebox.showwarning("Warning", "Invalid class name or class addition canceled.")

        # Close the TwoButtonPopup
        self.TwoButtonPopup.on_close()
        self.update_list()

    def handle_existing_class_selection(self, selected_class, dialog):
        """
        Handles the selection of an existing class from the dropdown menu.
        Updates the class label in annotations_history and redraws rectangles.
        """
        if selected_class and selected_class in self.image_annotation_tool.ClassSelector.class_labels:
            # Update the class label in the annotations_history
            self.image_annotation_tool.annotations_history[self.selected_index] = (
                self.image_annotation_tool.annotations_history[self.selected_index][0], selected_class
            )
            print(f"Relabeled annotation to '{selected_class}'.")
            self.image_annotation_tool.Rectangles.draw_rectangles()
            self.update_list()

        dialog.destroy()

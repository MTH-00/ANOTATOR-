import os
import tkinter as tk


class ImageNavigator:
    def __init__(self, image_annotation_tool):
        self.image_annotation_tool = image_annotation_tool
        self.current_index = 0

    def load_next_image(self):
        self.image_annotation_tool.annotation_handler.save_txt()
        self.image_annotation_tool.canvas.delete("all")

        if self.image_annotation_tool.image_directory:
            image_files = [f for f in os.listdir(self.image_annotation_tool.image_directory)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]

            if self.current_index < len(image_files) - 1:
                self.image_annotation_tool.save_annotated_image()

                self.current_index += 1
                next_image = image_files[self.current_index]
                self.image_annotation_tool.image_path = os.path.join(
                    self.image_annotation_tool.image_directory, next_image
                )
                self.image_annotation_tool.ImageHandler.load_image()
                self.update_listbox_selection()

    def update_listbox_selection(self):
        if self.image_annotation_tool.image_path:
            image_name = os.path.basename(self.image_annotation_tool.image_path)
            selected_index = self.image_annotation_tool.listbox_images.get(0, tk.END).index(image_name)
            self.image_annotation_tool.listbox_images.selection_clear(0, tk.END)
            self.image_annotation_tool.listbox_images.selection_set(selected_index)
            self.image_annotation_tool.listbox_images.see(selected_index)

    def reset_index(self):
        self.current_index = 0

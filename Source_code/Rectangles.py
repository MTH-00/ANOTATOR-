from PIL import Image, ImageDraw, ImageTk, ImageColor
import tkinter as tk


class Rectangles:
    
    def __init__(self, ImageAnnotationTool):
        self.ImageAnnotationTool = ImageAnnotationTool
        self.box_counter = 0
        self.rectangle_id = 0
        self.text_id = 0

    def draw_rectangles(self):
        print("Drawing")
        self.ImageAnnotationTool.canvas.delete("Rect")

        for i, (box, label) in enumerate(self.ImageAnnotationTool.annotations_history):
            if len(box) == 4 and box[0] < box[2] and box[1] < box[3]:
                bounding_box_color = self.ImageAnnotationTool.ClassSelector.class_colors.get(label, "pink")

                # Draw colored-filled rectangle on the canvas
                self.ImageAnnotationTool.rect_color_id = self.ImageAnnotationTool.canvas.create_rectangle(
                    box[0], box[1], box[0] + 70, box[1] + 20,
                    fill=bounding_box_color, tags="Rect"
                )

                # Draw rectangle with outline on the canvas
                self.rectangle_id = self.ImageAnnotationTool.canvas.create_rectangle(
                    box[0], box[1], box[2], box[3], outline=bounding_box_color, tags="Rect"
                )

                # Automatically select text color for readability
                text_color = "black" if sum(ImageColor.getcolor(bounding_box_color, "RGBA")[:3]) > 384 else "white"

                # Display class label and box number on the colored rectangle
                text = f"{label} - {i + 1}"
                text_width, text_height = ImageDraw.Draw(Image.new('RGB', (1, 10))).textbbox((0, 0), text)[2] - \
                                        ImageDraw.Draw(Image.new('RGB', (1, 10))).textbbox((0, 0), text)[0], \
                                        ImageDraw.Draw(Image.new('RGB', (1, 10))).textbbox((0, 0), text)[3] - \
                                        ImageDraw.Draw(Image.new('RGB', (1, 10))).textbbox((0, 0), text)[1]

                self.text_id = self.ImageAnnotationTool.canvas.create_text(
                    box[0] + 5, box[1] + 5, text=text, fill=text_color, anchor=tk.NW, width=(text_width + 100), tags="Rect"
                )

    def raise_rectangle(self):
        # Raise the rectangle and text to the front
        self.ImageAnnotationTool.canvas.tag_raise("Rect")

from PIL import Image, ImageDraw, ImageTk, ImageColor, ImageFilter
import tkinter as tk
from tkinter import filedialog
import os

from BoundingBoxSaver import BoundingBoxSaver
from Buttons import Buttons
from ClassSelector import ClassSelector
from Image_navigator import ImageNavigator
from AnnotationHandler import AnnotationHandler
from AnnotationEditor import AnnotationEditor
from Rectangles import Rectangles
from DirectoryHandler import DirectoryHandler
from ImageHandler import ImageHandler


class ImageAnnotationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("Annotator")
        self.master.attributes('-topmost', False)
        self.master.state('zoomed')

        self.image_path = None
        self.image_directory = None
        self.annotated_images_directory = "annotated_images"
        self.annotated_image = None

        self.edit_mode = False  # Flag to track editing mode
        self.selected_box = None  # Index of the selected bounding box
        self.resizing_handle = None  # Handle for resizing (if any)
        self.BUTTON_WIDTH = 20

        # Initialize variables for bounding box creation
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.box_counter = 1  # Counter for box numbers

        self.annotations_history = []

        # Initialize variables for image name and path
        self.image_name = None
        self.txt_file_path = None
        self.original_image = None

        # Create instances of classes
        self.bounding_box_saver = BoundingBoxSaver()
        self.annotation_handler = AnnotationHandler(self)
        self.image_navigator = ImageNavigator(self)
        self.ClassSelector = ClassSelector(self)
        self.AnnotationEditor = AnnotationEditor(self)
        self.Rectangles = Rectangles(self)
        self.DirectoryHandler = DirectoryHandler(self)
        self.ImageHandler = ImageHandler(self)
        self.Buttons = Buttons(self)

        self.DirectoryHandler.create_directories()
        self.create_widgets()

        # Bind mouse events for bounding box creation
        self.canvas.bind("<ButtonPress-1>", self.on_click_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Bind the <Configure> event to the on_window_resize method with a delay
        self.master.bind("<Configure>", lambda event: self.master.after(500, self.ImageHandler.on_window_resize, event))

    def create_widgets(self):
        # Create a paned window for dividing the main window into two panes
        self.paned_window = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned_window.pack(expand=True, fill=tk.BOTH)

        # Create the left pane for chat history (image list)
        self.left_pane = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_pane)

        # Create another paned window within the left pane
        self.left_paned_window = tk.PanedWindow(self.left_pane, orient=tk.VERTICAL)
        self.left_paned_window.pack(expand=True, fill=tk.BOTH)

        # Create the right pane for displaying images and annotations
        self.right_pane = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_pane)

        # Create a Tkinter canvas for displaying the image
        self.canvas = tk.Canvas(self.right_pane)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Create the upper part of the left pane (you can customize this part)
        upper_left_frame = tk.Frame(self.left_paned_window)
        self.left_paned_window.add(upper_left_frame)

        # Create the middle part of the left pane
        middle_left_frame = tk.Frame(self.left_paned_window)
        self.left_paned_window.add(middle_left_frame)

        # Create the lower part of the left pane (you can customize this part)
        lower_left_frame = tk.Frame(self.left_paned_window)
        self.left_paned_window.add(lower_left_frame)

        self.Buttons.create_buttons(lower_left_frame)

        self.ClassSelector.menu(lower_left_frame)
        self.AnnotationEditor.Annotation_list(middle_left_frame)

        # Create a listbox for displaying image files in the selected directory
        self.listbox_images = tk.Listbox(upper_left_frame, height=13)
        self.listbox_images.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox_images.bind("<ButtonRelease-1>", self.ImageHandler.load_selected_image)

        # Add a scrollbar to the listbox
        scrollbar = tk.Scrollbar(upper_left_frame, command=self.listbox_images.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_images.config(yscrollcommand=scrollbar.set)

    def save_annotated_image(self):
        if self.image_path and self.annotations_history:
            self.annotated_image = Image.open(self.image_path).convert("RGBA")

            # Calculate scaling factors for width and height
            width_factor = self.canvas.winfo_width() / self.annotated_image.width
            height_factor = self.canvas.winfo_height() / self.annotated_image.height

            # Choose the minimum scaling factor to fit the image in the canvas
            scale_factor = min(width_factor, height_factor)

            # Resize the image
            self.annotated_image = self.annotated_image.resize(
                (int(self.annotated_image.width * scale_factor), int(self.annotated_image.height * scale_factor)),
            )

            draw = ImageDraw.Draw(self.annotated_image)

            for i, (box, label) in enumerate(self.annotations_history):
                if len(box) == 4 and box[0] < box[2] and box[1] < box[3]:
                    bounding_box_color = self.ClassSelector.class_colors.get(label, "pink")
                    draw.rectangle(box, outline=bounding_box_color)

                    # Automatically select text color for readability
                    text_color = "black" if sum(ImageColor.getcolor(bounding_box_color, "RGBA")[:3]) > 384 else "white"

                    # Display class label and box number on the colored rectangle
                    text = f"{label} - {i + 1}"
                    text_width, text_height = draw.textbbox((0, 0), text)[2] - draw.textbbox((0, 0), text)[0], \
                                             draw.textbbox((0, 0), text)[3] - draw.textbbox((0, 0), text)[1]
                    draw.rectangle(
                        [box[0], box[1], box[0] + text_width + 10, box[1] + text_height + 10],
                        fill=bounding_box_color
                    )
                    draw.text((box[0] + 5, box[1] + 5), text, fill=text_color)

            self.annotated_image = self.annotated_image.convert("RGB")

            annotated_image_name = os.path.basename(self.image_path)
            annotated_image_path = os.path.join(
                self.annotated_images_directory, annotated_image_name.replace('.', '_annotated.')
            )
            self.annotated_image.save(annotated_image_path)

            self.annotation_handler.save_txt()
            print(f"Annotated image saved: {annotated_image_path}")

    def on_click_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        selected_class = self.ClassSelector.combobox_class.get()
        bounding_box_color = self.ClassSelector.class_colors.get(selected_class, "pink")

        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline=bounding_box_color, tags="annotation"
        )

        # Add colored rectangle on the left top corner during annotation
        rect_width = 50
        rect_height = 20

        self.rect_color_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x + rect_width, self.start_y + rect_height,
            fill=bounding_box_color,
            tags="annotation"
        )

        # Automatically select text color for readability
        text_color = "black" if sum(ImageColor.getcolor(bounding_box_color, "RGBA")[:3]) > 384 else "white"

        # Display class label and box number on the colored rectangle during annotation
        text = f"{selected_class} - {self.box_counter}"
        text_width, text_height = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text)[2] - \
                                ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text)[0], \
                                ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text)[3] - \
                                ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text)[1]
        self.text_id = self.canvas.create_text(
            self.start_x + 5, self.start_y + 5, text=text, fill=text_color, anchor=tk.NW, width=(text_width + 100),
            tags="annotation"
        )

        self.box_counter += 1

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

        # Update position of colored rectangle and text during dragging
        self.canvas.coords(self.rect_color_id, self.start_x, self.start_y, self.start_x + 50, self.start_y + 20)
        self.canvas.coords(self.text_id, self.start_x + 5, self.start_y + 5)

    def on_button_release(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.annotation_handler.save_annotations()
        self.canvas.delete("annotation")

        self.Rectangles.draw_rectangles()




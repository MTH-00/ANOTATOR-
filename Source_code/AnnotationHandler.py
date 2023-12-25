class AnnotationHandler:
    def __init__(self, image_annotation_tool):
        self.image_annotation_tool = image_annotation_tool
        self.box_counter = 1  # Counter for box numbers

    def save_annotations(self):
        if self.image_annotation_tool.rect_id:
            x1, y1, x2, y2 = self.image_annotation_tool.canvas.coords(self.image_annotation_tool.rect_id)
            image_coords = (x1, y1, x2, y2)
            selected_class = self.image_annotation_tool.ClassSelector.combobox_class.get()

            # Save the annotation in the history
            self.image_annotation_tool.annotations_history.append((image_coords, selected_class))

            self.image_annotation_tool.AnnotationEditor.update_list()
            print(f"Annotations saved for class '{selected_class}'.")
            print(self.image_annotation_tool.annotations_history)

    def save_txt(self):
        # Save bounding box information for the current image
        if self.image_annotation_tool.image_path:
            self.image_annotation_tool.bounding_box_saver.save_bounding_boxes(
                self.image_annotation_tool.image_path, self.image_annotation_tool.annotations_history
            )

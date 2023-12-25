import os

class BoundingBoxSaver:
    def __init__(self, txt_folder="annotations_txt"):
        self.txt_folder = txt_folder

    def save_bounding_boxes(self, image_path, annotations):
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_file_path = os.path.join(self.txt_folder, f"{image_name}_annotations.txt")

        # Ensure the directory exists
        os.makedirs(self.txt_folder, exist_ok=True)

        # Extract existing data from the file if it exists
        existing_data = self.extract_existing_data(txt_file_path)

        with open(txt_file_path, "w") as txt_file:
            for i, (box, label) in enumerate(annotations):
                # Combine label, box number, and coordinates
                line = f"{label}-{i + 1}: {box[0]} {box[1]} {box[2]} {box[3]}"

                # Check if the line is not repetitive
                if line not in existing_data:
                    txt_file.write(line + '\n')

        print(f"Bounding box history saved for {image_path} in {txt_file_path}.")

    def extract_existing_data(self, txt_file_path):
        existing_data = set()

        # Check if the file exists
        if os.path.exists(txt_file_path):
            # Read all lines from the annotations file
            with open(txt_file_path, "r") as txt_file:
                lines = txt_file.readlines()

            for line in lines:
                # Extract label and coordinates
                parts = line.split("-")
                if len(parts) == 2:
                    existing_data.add(parts[1].strip())
        print("Existing")
        print(existing_data)
        return existing_data

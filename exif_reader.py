import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from exiftool import ExifToolHelper


class ExifReader:
    def __init__(self, image_path=None, debug=0):
        self.image_path = image_path
        self.exif_data = {}
        self.option = "Read"
        self.debug = debug
        if __name__ == "__main__":
            self.arg_handler()
        # Default option is Read
        # Set debug to 1 for verbose output

    def arg_handler(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("image_path", help="Absolute path of image file")
        parser.add_argument("-r", "--read", help="Exif Read Mode", action='store_true')
        parser.add_argument("-w", "--write", help="Exif Write Mode", action='store_true')
        try:
            args = parser.parse_args()
        except Exception as e:
            print("Error: No image path specified. ", e)
            sys.exit()
        self.image_path = args.image_path
        if args.read:
            self.print_exif_data()
        elif args.write:
            self.write_exif()
            exit()
        else:
            self.print_exif_data()

    def read_exif(self):
        print("Entering read_exif method")
        try:
            image = Image.open(self.image_path)
            exif_info = image.getexif()
            if exif_info is not None:
                for tag_id, value in exif_info.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    self.exif_data[tag_name] = value
            else:
                print("No EXIF data found.")
            image.close()
        except Exception as e:
            print(f"Error reading EXIF data: {e}", file=sys.stderr)

    def write_exif(self):
        self.print_exif_tags_eth()
        tag = input("Enter the tag you want to modify: ")
        new_value = input("Enter the new value: ")
        with ExifToolHelper() as et:
            try:
                et.set_tags(self.image_path, {tag: new_value})
                print(f"Updated {tag} to {new_value} in {self.image_path}")
            except Exception as e:
                print(f"Failed to update {tag}. Please ensure the tag is valid. Error: {e}")
                sys.exit()

    def get_exif_data(self):
        self.read_exif()
        return self.exif_data

    def print_exif_data(self):
        exif_dict_items = self.get_exif_data().items()
        for tag, value in exif_dict_items:
            if tag != "MakerNote":
                print(f"{tag}: {value}") 

    def print_exif_tags(self):
        exif_dict_items = self.get_exif_data().items()
        for tag, value in exif_dict_items:
            if tag != "MakerNote":
                print(f"{tag}, ") 
    # Using Pillow methods to print exif tags. May be deprecated in future.

    def print_exif_tags_eth(self):
        with ExifToolHelper() as et:
            if self.debug:
                for d in et.get_metadata(self.image_path):
                    for k, v in d.items():
                        print(f"Dict: {k} = {v}")
            else: 
                for d in et.get_metadata(self.image_path):
                    for k, v in d.items():
                        k = k.split(":")[-1]
                        print(f"{k} = {v}")


if __name__ == "__main__":
    a = ExifReader()

# For testing purposes.

import sys, argparse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class ExifReader:
    def __init__(self, image_path = None):
        self.image_path = image_path
        self.exif_data = {}
        self.option = "Read"
        if __name__ == "__main__":
            self.arg_handler()
        # Default option is Read
        
    def arg_handler(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("image_path", help = "Absolute path of an image file")
        parser.add_argument("-r", "--read" , help = "Exif Read Mode", action = 'store_true')
        parser.add_argument("-w", "--write" , help = "Exif Write Mode", action = 'store_true')
        try:
            args = parser.parse_args()
        except:
            print("Error: No image path specified. ")
            exit()
        self.image_path = args.image_path
        if (args.read):
            self.print_exif_data()
        elif (args.write):
            print ("Write function currently not implemented")
            exit()
        else:
            self.print_exif_data()

    def read_exif(self):
        print("Entering read_exif method")
        try:
            image = Image.open(self.image_path)
            exif_info = image._getexif()
            if exif_info is not None:
                for tag_id, value in exif_info.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    self.exif_data[tag_name] = value
            else:
                print("No EXIF data found.")
        except Exception as e:
            print(f"Error reading EXIF data: {e}", file=sys.stderr)

    def get_exif_data(self):
        self.read_exif()
        return self.exif_data
    
    def print_exif_data(self):
        for tag, value in self.get_exif_data().items():
            if (tag != "MakerNote"):
                print(f"{tag}: {value}") 


if __name__ == "__main__":
        a = ExifReader()

# For testing purposes. 
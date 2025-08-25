import sys
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
        try:
            print(sys.argv[1])
            self.image_path = sys.argv[1]
        except:
            print("Error: no input file or command")
            exit()


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
        a.print_exif_data()

# For testing purposes. 
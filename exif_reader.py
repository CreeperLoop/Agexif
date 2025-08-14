import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
class ExifReader:
    def __init__(self, image_path):
        self.image_path = image_path
        # self.config_path = config_path
        self.exif_data = {}
        self.gui_exif_data = {}
        
    # Config file currently is only for stating the components needed for GUI program. 

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
    
    def gui_exif_data(self):
        self.get_exif_data()
        

if __name__ == "__main__":
    image = ExifReader(sys.argv[1])
    image.read_exif()
    for tag, value in image.get_exif_data().items():
        if (tag != "MakerNote"):
            print(f"{tag}: {value}") 

# For testing purposes. 
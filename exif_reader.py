import sys, argparse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class ExifReader:
    def __init__(self, image_path = None, debug = 1):
        self.image_path = image_path
        self.exif_data = {}
        self.option = "Read"
        self.debug = debug
        if __name__ == "__main__":
            self.arg_handler()
        # Default option is Read
        # Setting debug code to 1 will add arrary index after each line of printed exif data
        
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
            self.write_exif()
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
            image.close()
        except Exception as e:
            print(f"Error reading EXIF data: {e}", file=sys.stderr)

    def write_exif(self):
        print("Entering write_exif method")
        try:
            with Image.open(self.image_path) as image:
                # Get existing EXIF data
                exif_info = image.getexif()
                # Show available tags first
                print("\nAvailable EXIF tags:")
                self.print_exif_tags()
                # Get tag input from user
                tag = input("\nEnter the Tag you would like to adjust: ")
                # Find the tag ID for the specified tag name
                tag_id = None
                for key, value in TAGS.items():
                    if value.lower() == tag.lower():
                        tag_id = key
                        break
                if tag_id is None:
                    print(f"Error: Tag '{tag}' not found in EXIF specifications.")
                    return
                # Get the new value from user
                new_value = input("Enter the new value: ")
                # Update EXIF data
                exif_info[tag_id] = new_value.encode('utf-8')
                print (exif_info[tag_id])
                print (type(exif_info[tag_id]))
                # Create a new image with updated EXIF
                # image.save(self.image_path, exif=exif_info)
                print (type(exif_info))
                print(f"Successfully updated {tag} to: {new_value}")
        except Exception as e:
            print(f"Error writing EXIF data: {e}", file=sys.stderr)

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
        


if __name__ == "__main__":
        a = ExifReader()

# For testing purposes. 
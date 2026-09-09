from PIL import Image
import os

cat_folder = "../data/train/cat"

files = os.listdir(cat_folder)

img_path = os.path.join(cat_folder, files[0])

img = Image.open(img_path)

print("Ảnh:", img_path)
print("Kích thước:", img.size)
print("Mode:", img.mode)

img.show()
from PIL import Image
from datetime import datetime
"""
Merge two unlike images using pillow
"""

def even(n):
    if n % 2 == 0:
        return True
    return False

im1 = Image.open(input("filepath 1: "))
im2 = Image.open(input("filepath 2: "))

w = im1.width if im1.width < im2.width else im2.width
h = im1.height if im1.height < im2.height else im2.height

im1.resize((w, h))
im2.resize((w, h))

im3 = Image.new("RGB", (w, h))

for x in range(0, w):
    for y in range(0, h):
        if (not even(x) and not even(y)) or (even(x) and even(y)):
            im3.putpixel((x, y), im1.getpixel((x, y)))
        elif (even(x) and not even(y)) or (not even(x) and even(y)):
            im3.putpixel((x, y), im2.getpixel((x, y)))

im3.save("out/" + datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S") + ".jpeg")
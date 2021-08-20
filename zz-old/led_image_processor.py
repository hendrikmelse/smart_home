from PIL import Image

image = Image.open("/var/www/html/uploads/image.jpg")
pixels = image.load()

width, height = image.size

x_pixels = list(range(int(width * 60 / height)))
x_pixels.reverse()
y_pixels = list(range(59, -1, -1))

f = open("image.txt", "w")

for x in x_pixels:
    s = ""
    for y in y_pixels:
        for i in pixels[int(x * width / len(x_pixels)), int(y * height / 60)]:
            s = s + '{:02x}'.format(i)
    f.write(s + "\n")

f.close()

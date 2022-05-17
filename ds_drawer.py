from turtle import color
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# const
box_size = 200
box_thick = 5
img_size = 2000
padding = 50
font_size = 70
options = ['Nhà máy lớn', 'Nhà máy nhỏ', 'Không làm gì']
situations = ["Thị trường tốt", "Thị trường xấu"]
veri_peri = (102, 103, 171)

image_array = np.array([[255 for i in range(img_size)]
                        for i in range(img_size)])

print(image_array.shape)

img = Image.fromarray(image_array).convert(mode='RGB')

draw = ImageDraw.Draw(img)

draw.rectangle([padding, (img_size-box_size)/2,
                padding + box_size, (img_size-box_size)/2 + box_size],
               width=box_thick, outline=veri_peri)

font = ImageFont.truetype('./arial.ttf', font_size)

tail_padding = img_size/(len(options)*len(situations))
mid_padding = img_size/len(options)

start_mid = padding
start_tail = 0

for option in options:
    draw.line((padding + box_size, (img_size-box_size)/2 + box_size/2,
              img_size/4, start_mid + padding + box_size/2), fill=veri_peri, width=box_thick)

    draw.text((img_size/4, start_mid + padding - font_size),
              option, font=font, fill="black")
    draw.ellipse((img_size/4, start_mid + padding,
                  img_size/4 + box_size, start_mid + padding + box_size),
                 outline=veri_peri, width=box_thick)

    for situation in situations:
        draw.line((img_size/4 + box_size, start_mid + padding + box_size/2, (img_size/3)
                  * 2, start_tail + padding + font_size*0.5), fill=veri_peri, width=box_thick)
        draw.text(((img_size/3)*2, start_tail + padding),
                  situation, font=font, fill='black', width=box_thick)

        start_tail = start_tail + tail_padding
    start_mid = start_mid + mid_padding

img.show()

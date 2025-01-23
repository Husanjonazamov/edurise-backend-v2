import uuid

import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpRequest


class Certificate:

    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.font = self.get_font(160)

    def get_qr(self, url):
        img = qrcode.make(url)
        img.save("helpers/assets/qr.png")

        return Image.open("helpers/assets/qr.png")

    def get_font(self, size, font=None):

        if font is None:
            font = "helpers/assets/Font-1.ttf"
        return ImageFont.truetype(font, size)

    def write(self, text, x, y):
        fill = (0, 0, 0)
        if self.color is not None:
            fill = self.color

        return self.draw.text((x, y), text, font=self.font, fill=fill)

    def generate(self, request: HttpRequest, FIO, course, complate, color):
        self.color = color
        
        self.write(FIO, 180, 950)

        self.color = (119, 221, 4)
        self.font = self.get_font(90)

        self.write(course, 180, 1200)

        self.color = None
        self.font = self.get_font(100)
        self.write(complate, 180, 1340)

        self.filename = f"{uuid.uuid4()}.png"
        self.filepath = f"media/temp/{self.filename}"

        self.image.paste(self.get_qr(request.build_absolute_uri(f"/web/media/certificates/{self.filename}")),
                         (2200, 150))

        self.image.save(self.filepath)

        return self.filepath, self.filename

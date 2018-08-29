from random import randint

import torch
from PIL import ImageDraw, Image, ImageFont
from torch.utils.data.dataset import Dataset

from scribbler.document.parser import parse_document
from scribbler.resources.resources_helper import list_resources, get_random_text, peak_resource, get_random_background, count_resource
from scribbler.utils.image.image import image_pillow_to_numpy


class DocumentGenerator(Dataset):

    def __init__(self):
        self.documents = [parse_document(path) for path in list_resources("structures")]

    def __len__(self):
        return 1024

    def __getitem__(self, index):
        document = self.documents[randint(0, len(self.documents) - 1)]
        document.generate_random()
        image = document.to_image()

        # image = image_pillow_to_numpy(image)
        return image, document.get_baselines()


class LineGenerator:

    def __init__(self, labels):
        self.lst = labels

    def generate(self, index):
        text_start = randint(0, 5)
        text_end = randint(0, 50)
        text_top = randint(0, 5)
        text_bottom = randint(0, 5)

        text = get_random_text()

        font_height = randint(8, 30)
        font = ImageFont.truetype(peak_resource("fonts", index))

        total_width = 0
        lefts = []
        widths = []
        max_height = 0

        for i in range(0, len(text)):
            while True:
                try:
                    font_width, font_height = font.getsize(text[i])
                    break
                except OSError:
                    # print("Warning : execution context too long ! Continuing...")
                    font = ImageFont.truetype(peak_resource("fonts", 0))

            lefts.append(text_start + total_width)
            widths.append(font_width)
            total_width = total_width + font_width
            max_height = max(max_height, font_height)

        image_width = text_start + text_end + total_width
        image_height = text_top + text_bottom + font_height
        image = Image.new('RGBA', (image_width, image_height))
        image_draw = ImageDraw.Draw(image)

        for i in range(0, len(text)):
            image_draw.text((lefts[i], text_top), text[i], font=font, fill=(randint(0, 128), randint(0, 128), randint(0, 128)))
            widths[i] = widths[i] / image_width
            lefts[i] = lefts[i] / image_width

        image = image.rotate(randint(-3, 3), expand=True, resample=Image.BICUBIC)

        image_width, image_height = image.size
        background = get_random_background(image_width, image_height)
        background.paste(image, (0,0), image)

        return background, "".join(text)

    def get_labels(self):
        return self.lst


class LineGeneratedSet(Dataset):

    def __init__(self, labels="", width=None, height=32, transform=True, loss=None):
        self.width = width
        self.height = height
        self.document_generator = LineGenerator(labels)
        self.transform = transform
        self.loss = loss

    def __getitem__(self, index):
        image_pillow, label = self.generate_image_with_label(index)
        image = image_pillow_to_numpy(image_pillow)

        try:
            return torch.from_numpy(image), (self.loss.preprocess_label(label, image.shape[2]), label, image.shape[2])
        except:
            return self.__getitem__(index)

    def __len__(self):
        return count_resource("fonts") * 5

    def generate_image_with_label(self, index):
        index = index % count_resource("fonts")

        image, document = self.document_generator.generate(index)
        width, height = image.size
        if self.width is not None:
            image = image.resize((self.width, self.height), Image.ANTIALIAS)
        else:
            image = image.resize((width * self.height // height, self.height), Image.ANTIALIAS)

        return image, document

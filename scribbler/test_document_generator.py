from random import randint

from scribbler.generator import DocumentGenerator
from scribbler.utils.image.image import show_numpy_image

def main():
    line_generator = DocumentGenerator()

    for i in range(0, 4):
        image, _ = line_generator.__getitem__(randint(0, line_generator.__len__()))
        show_numpy_image(image, invert_axes=False)


if __name__ == '__main__':
    main()
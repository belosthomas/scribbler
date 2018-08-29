from random import randint

from scribbler.generator import LineGenerator
from scribbler.utils.image.image import show_numpy_image

def main():
    line_generator = LineGenerator()

    for i in range(0, 4):
        image, text = line_generator.__getitem__(randint(0, line_generator.__len__()))
        print(text)
        show_numpy_image(image.cpu().numpy())


if __name__ == '__main__':
    main()
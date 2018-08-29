from random import randint

from PIL import ImageDraw

from scribbler.generator import DocumentGenerator

def main():
    line_generator = DocumentGenerator()

    for i in range(0, 4):
        image, baselines = line_generator.__getitem__(randint(0, line_generator.__len__()))
        image_drawer = ImageDraw.Draw(image)

        for bl in baselines:
            image_drawer.line((bl[0], bl[1], bl[2], bl[3]), fill=(256, 0, 0))

        print(baselines)
        image.show()


if __name__ == '__main__':
    main()
from PIL import Image, ImageDraw, ImageFont
import argparse
import glob
import os

def get_parser():
    parser = argparse.ArgumentParser(description="fig2gif")
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("--duration", type=int, default=200)
    #parser.add_argument("--loop", type=int, default=1)
    args = parser.parse_args()
    return args

def main():
    args = get_parser()

    files = sorted(glob.glob("{}/*.png".format(args.input)))
    images = list(map(lambda file: Image.open(file), files))
    os.makedirs("{}/tmp".format(args.input), exist_ok=True)

    for i in range(len(images)):
        text = "{} steps".format((i+1)*10)
        font = ImageFont.truetype("font/arial.ttf", 32)
        size = font.getsize(text)
        images[i].putalpha(255)
        draw = ImageDraw.Draw(images[i])
        draw.text((images[i].size[0]-size[0]-30, images[i].size[1]-size[1]-10), text, font=font, fill=(0,0,0))
        images[i].save("{}/tmp/{:04}.png".format(args.input, i))

    files = sorted(glob.glob("{}/tmp/*.png".format(args.input)))
    images = list(map(lambda file: Image.open(file).quantize(), files))

    images[0].save("{}/output.gif".format(args.input), save_all=True, append_images=images[1:], duration=args.duration, disposal=2, optimize=False, loop=0)

if __name__ == "__main__":
    main()
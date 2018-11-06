from PIL import Image
import argparse

ascii_char = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray/unit)]



parser = argparse.ArgumentParser()
parser.add_argument('-file')  # 输入文件
parser.add_argument('-o', '--output')  # 输出文件
parser.add_argument('-width', '--width', type=int, default=80)  # 输出字符画宽
parser.add_argument('-height', '--height', type=int, default=80)  # 输出字符画高

args = parser.parse_args()


if __name__ == '__main__':
    file_path = args.file
    resize_width = args.width
    resize_height =args.height
    out_path = args.output

    im = Image.open(file_path)
    im = im.resize((resize_width, resize_height), Image.NEAREST)
    txt = ""
    for i in range(resize_height):
        for j in range(resize_width):
            txt += get_char(*im.getpixel((j,i)))
        txt += "\n"

    print(txt)

    if out_path:
        with open(out_path, 'w') as f:
            f.write(txt)
    else:
        with open("output.txt", 'w') as f:
            f.write(txt)

from PIL import Image
import numpy as np
import getopt
import sys


def get_average_color(arr, x, y, x_limit, y_limit, mosaic_size):
    sum_of_average = np.mean(arr[x:x_limit, y:y_limit])
    return int(sum_of_average)


def change_color(arr, x, y, x_limit, y_limit, color):
    arr[x:x_limit, y:y_limit] = color


def img_to_gray_mosaic(img, gradation, mosaic_size):
    arr = np.array(img)
    height = len(arr)
    width = len(arr[1])
    step_of_gradation = 255 // gradation
    x = 0
    while x < width:
        x_limit = min(width, x + mosaic_size[0])
        y = 0
        while y < height:
            y_limit = min(height, y + mosaic_size[1])
            average_grey_color = get_average_color(arr, x, y, x_limit, y_limit, mosaic_size)
            grey_color = int(average_grey_color // step_of_gradation) * step_of_gradation
            change_color(arr, x, y, x_limit, y_limit, grey_color)
            y += mosaic_size[1]
        x += mosaic_size[0]
    return Image.fromarray(arr)


def main(args):
    input_file = "img2.jpg"
    output_file = "res.jpg"
    mosaic_size = 10, 10
    gradation = 5
    try:
        opts, args = getopt.getopt(
            args, 'i:o:g:s:', ['input=', 'output=', 'gradation=', 'size='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for (arg, value) in opts:
        if arg == '-i' or arg == '--input':
            input_file = value.strip()
            if not input_file.endswith('.jpg'):
                print('Input file should be of type jpg')
                exit(2)
        if arg == '-o' or arg == '--output':
            output_file = value.strip()
        if arg == '-g' or arg == '--gradation':
            gradation = int(value.strip())
        if arg == '-s' or arg == '--size':
            mosaic_size = tuple(map(int, value.strip().split(',')))
            if len(mosaic_size) != 2:
                print("Size should be 2 numbers separated by ',' (10,10)")
    if input_file is None:
        print('Input file is None')
        exit(2)
    img = Image.open(input_file)
    res = img_to_gray_mosaic(img, gradation, mosaic_size)
    res.save(output_file)


if __name__ == "__main__":
    main(sys.argv[1:])

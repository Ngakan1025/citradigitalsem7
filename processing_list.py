from PIL import Image, ImageOps
from math import cos, log, sin, floor

from pyscreeze import pixel


def ImgNegative(img_input, coldepth):
    # solusi 1
    # img_output=ImageOps.invert(img_input)
    # solusi 2
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i, j] = (255-r, 255-g, 255-b)
            # if i < j:
            #     pixels[i, j] = (255-r, 255-g, 255-b)
            # else:
            #     pixels[i, j] = (r, g, b)

    # memastikan output yang masih sama dengan bit aslinhya
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def rotating(img_input, coldepth, deg):
    if coldepth != 24:
        img_input = img_input.convert("RGB")
        input_pixels = img_input.load()

    horizontal_size = img_input.size[0]
    vertical_size = img_input.size[1]

    img_output = Image.new("RGB", img_input.size)
    output_pixels = img_output.load()

    x0 = horizontal_size//2
    y0 = vertical_size//2

    for x1 in range(horizontal_size):
        for y1 in range(vertical_size):
            radian = deg * 22/7 / 180

            # rotation formula with center of free rotation
            # source : https://homepages.inf.ed.ac.uk/rbf/HIPR2/rotate.htm
            x2 = int((x1-x0)*cos(radian) - (y1-y0)*sin(radian)+x0)
            y2 = int((x1-x0)*sin(radian) + (y1-y0)*cos(radian)+y0)
            if (x2 >= horizontal_size or y2 >= vertical_size or x2 < 0 or y2 < 0):
                output_pixels[x1, y1] = (0, 0, 0)
            else:
                output_pixels[x1, y1] = input_pixels[x2, y2]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def clipping(intensity):
    if intensity < 0:
        return 0
    if intensity > 255:
        return 255
    return intensity


def ImgBrightness(img_input, coldepth, enlightenment_value):
    if coldepth != 24:
        img_input = img_input.convert("RGB")
    input_pixels = img_input.load()

    img_output = Image.new("RGB", img_input.size)
    output_pixels = img_output.load()

    horizontal_size = img_output.size[0]
    vertical_size = img_output.size[1]

    for x in range(horizontal_size):
        for y in range(vertical_size):
            R = clipping(input_pixels[x, y][0] + enlightenment_value)
            G = clipping(input_pixels[x, y][1] + enlightenment_value)
            B = clipping(input_pixels[x, y][2] + enlightenment_value)
            output_pixels[x, y] = (R, G, B)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


# def ImgBlending(img_input_1, img_input_2, coldepth):
#     if coldepth != 24:
#         img_input_1 = img_input_1.convert('RGB')
#         input_pixels_1 = img_input_1.load()

#         img_input_2 = img_input_2.convert('RGB')
#         input_pixels_2 = img_input_2.load()

#         img_output = Image.new(
#             "RGB", (img_input_1.size[0], img_input_1.size[1]))
#         output_pixels = img_output.load()

#     for x in range(img_input_1.size[0]):
#         for y in range(img_input_1.size[1]):
#             r = input_pixels_1[x, y][0] - input_pixels_2[x, y][0]
#             g = input_pixels_1[x, y][1] - input_pixels_2[x, y][1]
#             b = input_pixels_1[x, y][2] - input_pixels_2[x, y][2]
#             output_pixels[x, y] = (r, g, b)

#             # if there is a difference
#             # between pixel 1 & pixel 2, use pixels 2
#             if(r > 0 or g > 0 or b > 0):
#                 output_pixels[x, y] = input_pixels_2[x, y]

#     if coldepth == 1:
#         img_output = img_output.convert("1")
#     elif coldepth == 8:
#         img_output = img_output.convert("L")
#     else:
#         img_output = img_output.convert("RGB")

#     return img_output


# def ImgBlending(img_input_1, coldepth, img_input_2, coldepth2, alpha, alpha2):
#     if coldepth != 24:
#         img_input_1 = img_input_1.convert("RGB")
#     elif coldepth2 != 24:
#         img_input_2 = img_input_2.convert("RGB")

#     img_output = Image.new("RGB", (img_input_1.size[0], img_input_1.size[1]))
#     output_pixels = img_output.load()

#     for i in range(img_output.size[0]):
#         for j in range(img_output.size[1]):
#             color1 = img_input_1.getpixel((i, j))
#             color2 = img_input_2.getpixel((i, j))
#             r = int(color1[0]*alpha) + int(color2[0]*alpha2)
#             g = int(color1[1]*alpha) + int(color2[1]*alpha2)
#             b = int(color1[2]*alpha) + int(color2[2]*alpha2)
#             output_pixels[i, j] = (r, g, b)

#     if coldepth == 1:
#         img_output = img_output.convert("1")
#     elif coldepth == 8:
#         img_output = img_output.convert("L")
#     else:
#         img_output = img_output.convert("RGB")

#     return img_output


def ImgLogarithmic(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')
        C = 40
        img_output = Image.new(
            'RGB', (img_input.size[0], img_input.size[1]))
        pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i, j] = (int(C*log(1+r)),
                            int(C*log(1+g)),
                            int(C*log(1+b)))
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgPowerLaw(img_input, coldepth, gamma):
    # solusi 1
    # img_output=ImageOps.autocontrast(img_input, cutoff=0, ignore=None)

    # solusi 2
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[1], img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            # print(r)
            pixels[i, j] = (int(255*(r/255)**gamma),
                            int(255*(r/255)**gamma), int(255*(b/255)**gamma))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def flipping(img_input, coldepth, type):
    img_input = img_input
    input_pixels = img_input.load()

    if coldepth != 24:
        img_input = img_input.convert("RGB")

    horizontal_size = img_input.size[0]
    vertical_size = img_input.size[1]

    img_output = Image.new("RGB", img_input.size)
    output_pixels = img_output.load()

    for x in range(horizontal_size):
        for y in range(vertical_size):
            if type == "vertical":
                output_pixels[x, y] = input_pixels[x, vertical_size-1-y]
            elif type == "horizontal":
                output_pixels[x, y] = input_pixels[horizontal_size-1-x, y]
            else:
                output_pixels[x, y] = input_pixels[horizontal_size -
                                                   1-x, vertical_size-1-y]
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def translation(img_input, coldepth, shift):
    if coldepth != 24:
        img_input = img_input.convert("RGB")
        input_pixels = img_input.load()

        img_output = Image.new(
            'RGB', (img_input.size[1], img_input.size[0]))
        output_pixels = img_output.load()

    start_m = shift[0]
    start_n = shift[1]

    if shift[0] < 0:
        start_m = 0
    if shift[1] < 0:
        start_n = 0

    for x in range(start_m, img_input.size[0]):
        for y in range(start_n, img_input.size[1]):
            new_x = x - shift[0]
            new_y = y - shift[1]

            if(new_x >= img_input.size[0] or new_y >= img_input.size[1] or new_x < 0 or new_y < 0):
                output_pixels[x, y] = (0, 0, 0)
            else:
                output_pixels[x, y] = input_pixels[new_x, new_y]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def zooming(img_input, coldepth, scale):
    if coldepth != 24:
        img_input = img_input.convert("RGB")

    img_output = Image.new(
        "RGB", (img_input.size[0]*scale, img_input.size[1]*scale))
    output_pixels = img_output.load()

    horizontal_size = img_output.size[0]
    vertical_size = img_output.size[1]

    for x in range(horizontal_size):
        for y in range(vertical_size):
            r, g, b = img_input.getpixel((x/scale, y/scale))
            output_pixels[x, y] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def shringking(img_input, coldepth, scale):
    if coldepth != 25:
        img_input = img_input.convert("RGB")

    img_output = Image.new(
        "RGB", (int(img_input.size[0]/scale), int(img_input.size[1]/scale)))
    output_pixels = img_output.load()

    horizontal_size = img_output.size[0]
    vertical_size = img_output.size[1]

    for x in range(horizontal_size):
        for y in range(vertical_size):
            r, g, b = img_input.getpixel((x*scale, y*scale))
            output_pixels[x, y] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgGrayscale(img_input, coldepth):
    # solusi 1
    # img_output=ImageOps.invert(img_input)
    # solusi 2
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    pixelss = img_input.load()
    horizontal_size = img_input.size[0]
    vertical_size = img_input.size[1]
    img_output = Image.new('RGB', (horizontal_size, vertical_size))
    pixels = img_output.load()

    for i in range(horizontal_size):
        for j in range(vertical_size):
            r, g, b = pixelss[i, j]
            # pixels[i, j] = (255-r, 255-g, 255-b)
            # if i < j:
            # if i < horizontal_size//2:

            if i+j <= vertical_size:
                if i < j:
                    pixels[i, j] = (255-r, 255-g, 255-b)
                else:
                    pixels[i, j] = (r, g, b)
            elif i > j:
                pixels[i, j] = (255-r, 255-g, 255-b)
            # elif i < j:
            #     pixels[i, j] = (r, g, b)
            else:
                pixels[i, j] = (r, g, b)

    # memastikan output yang masih sama dengan bit aslinhya
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgShrinking(img_input, coldepth):

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    N = 2
    rowOut, colOut = int(img_input.size[0]/N), int(img_input.size[1]/N)

    img_output = Image.new('RGB', (rowOut, colOut))
    pixels = img_output.load()

    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((floor(i*N), floor(j*N)))
            pixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgRotate270(img_input, coldepth, direction=270):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    pixels = img_input.load()
    horizontalSize = img_input.size[0]
    verticalSize = img_input.size[1]
    img_output = Image.new("RGB", (verticalSize, horizontalSize))
    newPixels = img_output.load()
    if direction == 270:
        for i in range(horizontalSize):
            for j in range(verticalSize):
                r, g, b = pixels[i, j]
                newPixels[j, horizontalSize-1-i] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output


def ImgFlippingHorizontal(img_input, coldepth):

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    PIXEL = img_input.load()

    ukuran_horizontal = img_input.size[0]
    ukuran_vertikal = img_input.size[1]

    img_output = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    PIXEL_BARU = img_output.load()

    for x in range(ukuran_horizontal):
        for y in range(ukuran_vertikal):
            PIXEL_BARU[x, y] = PIXEL[ukuran_horizontal - 1 - x, y]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgRotate180(img_input, coldepth, direction=180):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    pixels = img_input.load()
    horizontalSize = img_input.size[0]
    verticalSize = img_input.size[1]
    img_output = Image.new("RGB", (horizontalSize, verticalSize))
    newPixels = img_output.load()
    if direction == 180:
        for i in range(horizontalSize):
            for j in range(verticalSize):
                r, g, b = pixels[i, j]
                newPixels[horizontalSize-1-i, verticalSize-1-j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output


def ImgBlending(img_input, img_input2, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    pixels = img_input.load()
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    npixels = img_output.load()
    img_input2 = img_input2.resize(
        (img_input.size[0]//2, img_input.size[1]//2))
    pixels2 = img_input2.load()

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = pixels[i, j]
            if i < img_input.size[0]//2 and j < img_input.size[1]//2:
                r2, g2, b2 = pixels2[i, j]
                npixels[i, j] = (r//2 + r2//2, g//2 + g2//2, b//2 + b2//2)
            else:
                npixels[i, j] = pixels[i, j]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgBlending2(img_input, img_input2, coldepth):
    if coldepth != 24:

        img_input2 = ImgShrinking(img_input2, coldepth)
        img_input2 = ImgRotate270(img_input2, coldepth, direction=270)
        img_input = ImgFlippingHorizontal(img_input, coldepth)
        img_input = img_input.convert('RGB')
        img_input2 = img_input2.convert('RGB')

    pixels = img_input.load()
    pixels2 = img_input2.load()
    horizontalSize = img_input.size[0]
    verticalSize = img_input.size[1]
    horizontalSize2 = img_input2.size[0]
    verticalSize2 = img_input2.size[1]
    img_output = Image.new('RGB', (horizontalSize, verticalSize))
    pixelsbaru = img_output.load()
    for i in range(horizontalSize):
        for j in range(verticalSize):
            if i < horizontalSize2 and j < verticalSize2:
                r1, g1, b1 = pixels[i, j]
                r2, g2, b2 = pixels2[i, j]
                pixelsbaru[i, j] = (r1//2+r2//2, g1//2+g2//2, b1//2+b2//2)

            else:
                pixelsbaru[i, j] = pixels[i, j]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgFlippingVertikal(img_input, coldepth):

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    PIXEL = img_input.load()

    ukuran_horizontal = img_input.size[0]
    ukuran_vertikal = img_input.size[1]

    img_output = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    PIXEL_BARU = img_output.load()

    for x in range(ukuran_horizontal):
        for y in range(ukuran_vertikal):
            PIXEL_BARU[x, y] = PIXEL[x, ukuran_vertikal - 1 - y]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgFlippingVerHor(img_input, coldepth):
    #img_output = img_input.transpose(Image.FLIP_LEFT_RIGHT)

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[0]):
            r, g, b = img_input.getpixel(
                ((img_output.size[0]-1)-i, (img_output.size[1]-1)-j))
            pixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgBlending3(img_input, img_input2, coldepth):
    if coldepth != 24:

        img_input2 = ImgShrinking(img_input2, coldepth)
        # img_input2 = ImgFlippingVertikal(img_input2, coldepth)
        # img_input = ImgRotate180(img_input, coldepth)
        img_input = ImgFlippingHorizontal(img_input, coldepth)
        img_input = img_input.convert('RGB')
        img_input2 = img_input2.convert('RGB')

    pixels = img_input.load()
    pixels2 = img_input2.load()
    horizontalSize = img_input.size[0]
    verticalSize = img_input.size[1]
    horizontalSize2 = img_input2.size[0]
    verticalSize2 = img_input2.size[1]
    img_output = Image.new('RGB', (horizontalSize, verticalSize))
    pixelsbaru = img_output.load()
    for i in range(horizontalSize):
        for j in range(verticalSize):
            if i < horizontalSize2 and j < verticalSize2:
                r1, g1, b1 = pixels[i, j]
                r2, g2, b2 = pixels2[i, j]
                pixelsbaru[i, j] = (r1//2+r2//2, g1//2+g2//2, b1//2+b2//2)
# horizontalSize*2-1-i, j
            else:
                pixelsbaru[i, j] = pixels[i, j]

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return ImgFlippingVertikal(img_output, coldepth)


def ImgWajik(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    pixels = img_input.load()
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    npixels = img_output.load()
    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = pixels[i, j]
            if abs(i - img_input.size[0]//2) + abs(j - img_input.size[1]//2) < img_input.size[0]//2:
                # Gray = (r + g + b)//3
                npixels[i, j] = (255-r, 255-g, 255-b)
            else:
                npixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgBulat(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    pixel = img_input.load()
    # make a new image with same size as input image
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    # load the pixels
    pixels = img_output.load()

    # make a variable to store the center of the image
    center_x = img_input.size[0]//2
    center_y = img_input.size[1]//2

    # make a variable to store the radius of the image
    radius_x = img_input.size[0]//2
    radius_y = img_input.size[1]//2

    # make a variable to store the color of the image
    color = (255, 255, 255)

    # make a loop to make the eclipse shape
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            if (i-center_x)**2/radius_x**2 + (j-center_y)**2/radius_y**2 <= 1:
                r, g, b = img_input.getpixel((i, j))
                pixels[i, j] = (255-r, 255-g, 255-b)
            else:
                pixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgFlip4(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    pixels = img_input.load()
    horizontalSize = img_input.size[0]
    verticalSize = img_input.size[1]
    img_output = Image.new("RGB", (horizontalSize*2, verticalSize*2))
    newPixels = img_output.load()
    for i in range(horizontalSize):
        for j in range(verticalSize):
            r, g, b = pixels[i, j]
            newPixels[i, j] = (r, g, b)
            newPixels[i, verticalSize*2-1-j] = (r, g, b)
            newPixels[horizontalSize*2-1-i, j] = (r, g, b)
            newPixels[horizontalSize*2-1-i, verticalSize*2-1-j] = (r, g, b)
# j, horizontalSize-1-i
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output


def ImgFlip4_2(img_input, coldepth):

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    output_image = Image.new(
        'RGB', (int(img_input.size[1]/2), int(img_input.size[0]/2)))
    pixels = output_image.load()

    for i in range(output_image.size[0]):
        for j in range(output_image.size[1]):
            r, g, b = img_input.getpixel((i*2, j*2))
            pixels[i, j] = (r, g, b)

    canvas = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    canvas_pixels = canvas.load()

    for i in range(output_image.size[0]):
        for j in range(output_image.size[1]):
            r, g, b = output_image.getpixel((i, j))
            canvas_pixels[i, j] = (r, g, b)
            canvas_pixels[output_image.size[0]*2-1-i, j] = (r, g, b)
            canvas_pixels[i, output_image.size[1]*2-1-j] = (r, g, b)
            # rotating image 90 degree clockwise
            r, g, b = output_image.getpixel((j, output_image.size[0]-i-1))
            canvas_pixels[i+output_image.size[0],
                          j+output_image.size[1]] = (r, g, b)

    if coldepth == 1:
        output_image = output_image.convert("1")
    elif coldepth == 8:
        output_image = output_image.convert("L")
    else:
        output_image = output_image.convert("RGB")

    return canvas

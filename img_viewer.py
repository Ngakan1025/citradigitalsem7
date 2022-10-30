import PySimpleGUI as sg
import os.path
from PIL import Image, ImageOps
from processing_list import *
# Kolom Area No 1: Area open folder and select image
file_list_column = [
    [sg.Text("Open Image Folder :"), ],
    [
        sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),
        sg.FolderBrowse(),
    ],
    [sg.Text("Choose an image from list :"), ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(18, 10), key="ImgList"
        )
    ],
    [sg.HSeparator()],
    [sg.Text("Image Information:"), ],
    [sg.Text(size=(20, 1), key="ImgSize"), ],
    [sg.Text(size=(20, 1), key="ImgColorDepth"), ],
]
# Kolom Area No 2: Area viewer image input
image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]
# Kolom Area No 3: Area Image info dan Tombol list of processing
list_processing = [
    [sg.Text("List of Processing:"), ],
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative"), ],

    [sg.Button("Image Rotating", size=(20, 1), key="image_rotating"), ],
    [sg.Text("Image Rotating : ", key="text_rotating", visible=False), ],
    [sg.Slider(range=(0, 360), size=(19, 20), orientation='h',
               key="slider_rotating", default_value=0, visible=False), ],
    [sg.Button("Apply", size=(20, 1), key="submit_rotating", visible=False), ],

    [sg.Button("Image Brightness", size=(20, 1), key="ImgBrightness"), ],
    [sg.Text("Image Brightness : ", key="text_brightness", visible=False), ],
    [sg.Slider(range=(0, 255), size=(19, 20), orientation='h',
               key="slider_brightness", default_value=0, visible=False), ],
    [sg.Button("Apply", size=(20, 1), key="submit_brightness", visible=False), ],

    [sg.HSeparator()],
    [sg.Button("Image Blending", size=(20, 1), key="ImgBlending")],
    [
        sg.In(size=(15, 1), enable_events=True,
              key="img_input_2", disabled=True),
        sg.FileBrowse(key="browse_img_input_2", disabled=True)
    ],
    [sg.Button("Apply", size=(20, 1), key="submit_blending", visible=False), ],

    [sg.HSeparator()],
    [sg.Button("Image Power law", size=(20, 1), key="ImgPowerLaw")],

    [sg.Button("Image Logarithmic", size=(20, 1), key="ImgLogarithmic")],

    [sg.Button("Image Flipping", size=(20, 1), key="image_flipping")],
    [sg.Text("Image Flipping : ", key="text_flipping", visible=False), ],
    [sg.Button("Horizontal", size=(20, 1),
               key="submit_horizontal", visible=False), ],
    [sg.Button("Vertical", size=(20, 1), key="submit_vertical", visible=False), ],
    [sg.Button("Vertical Horizontal", size=(20, 1),
               key="submit_vertical_horizontal", visible=False), ],

    [sg.Button("Image Translation", size=(20, 1), key="image_translation")],
    [sg.Text("Image Translation : ", key="text_translation", visible=False), ],
    [sg.Text("x value:", visible=False, key="text_translate_x"), ],
    [sg.In(default_text=0, size=(9, 1), visible=False, key="input_x_translation"), ],
    [sg.Text("y value:", visible=False, key="text_translate_y"), ],
    [sg.In(default_text=0, size=(9, 1), visible=False, key="input_y_translation"), ],
    [sg.Button("Apply", size=(20, 1), key="submit_translation", visible=False), ],

    [sg.Button("Image Zooming", size=(20, 1), key="image_zooming")],
    [sg.Text("Image Zooming : ", key="text_zooming", visible=False), ],
    [sg.Slider(range=(2, 4), size=(19, 20), orientation='h',
               key="slider_zooming", visible=False), ],
    [sg.Button("Apply", size=(20, 1), key="submit_zooming", visible=False), ],

    [sg.Button("Image Shringking", size=(20, 1), key="image_shringking")],
    [sg.Text("Image Shringking : ", key="text_shringking", visible=False), ],
    [sg.Slider(range=(2, 4), size=(19, 20), orientation='h',
               key="slider_shringking", visible=False), ],
    [sg.Button("Apply", size=(20, 1), key="submit_shringking", visible=False), ],

    [sg.HSeparator()],

    [sg.Button("Image Silang", size=(20, 1), key="ImgGrayscale"), ],
    [sg.Button("Image Wajik", size=(20, 1), key="ImgWajik"), ],
    [sg.Button("Image Bulat", size=(20, 1), key="ImgBulat"), ],
    [sg.Button("Image Flip4", size=(20, 1), key="ImgFlip4"), ],
    [sg.Button("Image Flip4(2)", size=(20, 1), key="ImgFlip42"), ],
    [sg.Button("Image Blending 2", size=(20, 1), key="ImgBlending2")],
    [
        sg.In(size=(15, 1), enable_events=True,
              key="imginput_2", disabled=True),
        sg.FileBrowse(key="browseimg_input_2", disabled=True)
    ],
    [sg.Button("Apply", size=(20, 1), key="submit_blending2", visible=False), ],

    [sg.Button("Image Blending 3", size=(20, 1), key="ImgBlending3")],
    [
        sg.In(size=(15, 1), enable_events=True,
              key="imginput2", disabled=True),
        sg.FileBrowse(key="browseimg_input2", disabled=True)
    ],
    [sg.Button("Apply", size=(20, 1), key="submit_blending3", visible=False), ],


    [sg.HSeparator()],
    [sg.Button("Reset", size=(20, 1), key="cancel", visible=False), ]
]
# Kolom Area No 4: Area viewer image output
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]
# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(list_processing),
        sg.VSeperator(),
        sg.Column(image_viewer_column2),
    ]
]
window = sg.Window("Mini Image Editor", layout)
# Run the Event Loop
# nama image file temporary setiap kali processing output
filename_out = "out.png"
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["ImgList"].update(fnames)
    elif event == "ImgList":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["ImgFolder"], values["ImgList"][0]
            )
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
            window["ImgProcessingType"].update(filename)
            window["ImgOutputViewer"].update(filename=filename)
            img_input = Image.open(filename)
            # img_input.show()

            # Size
            img_width, img_height = img_input.size
            window["ImgSize"].update(
                "Image Size : "+str(img_width)+" x "+str(img_height))

            # Color depth
            mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32,
                                "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
            coldepth = mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update("Color Depth : "+str(coldepth))
        except:
            pass
    elif event == "ImgNegative":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Negative")
            img_output = ImgNegative(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgGrayscale":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Silang")
            img_output = ImgGrayscale(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "image_rotating":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Rotating")
            # Rotating
            window["text_rotating"].update(visible=True)
            window["slider_rotating"].update(visible=True)
            window["submit_rotating"].update(visible=True)
        except:
            pass

    elif event == "ImgBrightness":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Brigtness")
            # Brigthness
            window["text_brightness"].update(visible=True)
            window["slider_brightness"].update(visible=True)
            window["submit_brightness"].update(visible=True)
        except:
            pass
    elif event == "ImgBlending":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Blending")
            # Blending
            window["submit_blending"].update(visible=True)
            window["img_input_2"].update(disabled=False)
            window["browse_img_input_2"].update(disabled=False)
        except:
            pass
    elif event == "ImgLogarithmic":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Logaritmic")

            img_output = ImgLogarithmic(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgPowerLaw":
        try:
            window["ImgProcessingType"].update("Image Power Law")
            img_output = ImgPowerLaw(img_input, coldepth, 4)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "image_flipping":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Flipping")
            # Flipping
            window["text_flipping"].update(visible=True)
            window["submit_horizontal"].update(visible=True)
            window["submit_vertical"].update(visible=True)
            window["submit_vertical_horizontal"].update(visible=True)
        except:
            pass
    elif event == "image_translation":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Translation")
            # Translation
            window["text_translation"].update(visible=True)
            window["text_translate_x"].update(visible=True)
            window["input_x_translation"].update(visible=True)
            window["text_translate_y"].update(visible=True)
            window["input_y_translation"].update(visible=True)
            window["submit_translation"].update(visible=True)
        except:
            pass
    elif event == "image_zooming":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Zooming")
            # Zooming
            window["text_zooming"].update(visible=True)
            window["slider_zooming"].update(visible=True)
            window["submit_zooming"].update(visible=True)
        except:
            pass
    elif event == "image_shringking":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Shringking")
            # Shringking
            window["text_shringking"].update(visible=True)
            window["slider_shringking"].update(visible=True)
            window["submit_shringking"].update(visible=True)
        except:
            pass
    elif event == "ImgWajik":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Wajik")
            img_output = ImgWajik(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgBulat":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Bulat")
            img_output = ImgBulat(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgFlip4":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Flip4")
            img_output = ImgFlip4(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgFlip42":

        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Flip4(2)")
            img_output = ImgFlip4_2(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "ImgBlending2":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Blending 2")
            # Blending
            window["submit_blending2"].update(visible=True)
            window["imginput_2"].update(disabled=False)
            window["browseimg_input_2"].update(disabled=False)
        except:
            pass
    elif event == "ImgBlending3":
        try:
            window["cancel"].update(visible=True)
            window["ImgProcessingType"].update("Image Blending 3")
            # Blending
            window["submit_blending3"].update(visible=True)
            window["imginput2"].update(disabled=False)
            window["browseimg_input2"].update(disabled=False)
        except:
            pass
    elif event == "submit_rotating":
        try:
            deg = int(values["slider_rotating"])
            img_output = rotating(img_input, coldepth, deg)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_brightness":
        try:
            value = int(values["slider_brightness"])
            window["ImgProcessingType"].update("Image Brightness")
            img_output = ImgBrightness(img_input, coldepth, value)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_blending":
        try:
            filename = values['img_input_2']
            img_input2 = Image.open(filename)

            window["ImgProcessingType"].update("Image Blending")
            img_output = ImgBlending(img_input, img_input2, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_horizontal":
        try:
            type = "horizontal"
            window["ImgProcessingType"].update("Image Flipping Horizontal")
            output_image = flipping(img_input, coldepth, type)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "submit_vertical":
        try:
            type = "vertical"
            window["ImgProcessingType"].update("Image Flipping Vertical")
            output_image = flipping(img_input, coldepth, type)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "submit_vertical_horizontal":
        try:
            type = "vertical_herizontal"
            window["ImgProcessingType"].update(
                "Image Flipping Vertical Horizontal")
            output_image = flipping(img_input, coldepth, type)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_translation":
        try:
            x = int(values["input_x_translation"])
            y = int(values["input_y_translation"])
            shift = [x, y]
            window["ImgProcessingType"].update("Image Translation")
            output_image = translation(img_input, coldepth, shift)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_zooming":
        try:
            scale = int(values["slider_zooming"])
            window["ImgProcessingType"].update("Zoom In")
            output_image = zooming(img_input, coldepth, scale)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_shringking":
        try:
            scale = int(values["slider_shringking"])
            window["ImgProcessingType"].update("Image Shringking")
            output_image = shringking(img_input, coldepth, scale)
            output_image.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_blending2":
        try:
            filename = values['imginput_2']
            img_input2 = Image.open(filename)

            window["ImgProcessingType"].update("Image Blending 2")
            img_output = ImgBlending2(img_input, img_input2, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "submit_blending3":
        try:
            filename = values['imginput2']
            img_input2 = Image.open(filename)

            window["ImgProcessingType"].update("Image Blending 3")
            img_output = ImgBlending3(img_input, img_input2, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    elif event == "cancel":
        try:
            img_output = img_input
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)

            window["cancel"].update(visible=False)
            window["ImgProcessingType"].update("")
            # Brigthness
            window["text_brightness"].update(visible=False)
            window["slider_brightness"].update(visible=False)
            window["submit_brightness"].update(visible=False)
            # Rotating
            window["text_rotating"].update(visible=False)
            window["slider_rotating"].update(visible=False)
            window["submit_rotating"].update(visible=False)
            # submit blending
            window["submit_blending"].update(visible=False)
            window["img_input_2"].update(disabled=True)
            window["browse_img_input_2"].update(disabled=True)
            # Flipping
            window["text_flipping"].update(visible=False)
            window["submit_horizontal"].update(visible=False)
            window["submit_vertical"].update(visible=False)
            window["submit_vertical_horizontal"].update(visible=False)
            # Translation
            window["text_translation"].update(visible=False)
            window["text_translate_x"].update(visible=False)
            window["input_x_translation"].update(visible=False)
            window["text_translate_y"].update(visible=False)
            window["input_y_translation"].update(visible=False)
            window["submit_translation"].update(visible=False)
            # Zooming
            window["text_zooming"].update(visible=False)
            window["slider_zooming"].update(visible=False)
            window["submit_zooming"].update(visible=False)
            # Shringking
            window["text_shringking"].update(visible=False)
            window["slider_shringking"].update(visible=False)
            window["submit_shringking"].update(visible=False)
        except:
            pass

window.close()

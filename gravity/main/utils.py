import os, secrets
from typing import List
from PIL import Image
from flask import current_app


def save_trans_plot(plot_path, random=True):
    # Open and deal with path and name
    img = Image.open(plot_path)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(plot_path)

    if random: plot_name = random_hex + f_ext
    else: plot_name = 'transparent_temp' + f_ext

    plot_path = os.path.join(current_app.root_path, 'static/orbit_plots', plot_name)

    # Convert white background to transpatent
    rgba = img.convert("RGBA")
    datas = rgba.getdata()

    newData = []
    for item in datas:
        print(item[:3])
        if item[:3] == (255, 255, 255):  # white colour
            # replacing it with a transparent value
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    # Save new image
    rgba.putdata(newData)
    rgba.save(plot_path)

    return plot_name

def convert_to_list(string: str) -> List[float]:
    message = 'wrong format, example str: "1, 1, 1"'
    try:
        list = (string).replace(' ', '').split(',')
        list = [float(x) for x in list]
    except:
        raise ValueError(message)
    if len(list) != 3 or len(list) != 2:
        raise ValueError(message)
    return list
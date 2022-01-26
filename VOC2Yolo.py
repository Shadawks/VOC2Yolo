from xml.dom import minidom
from tkinter.filedialog import askdirectory
from tkinter import Tk
import os, glob, time
root = Tk(); root.withdraw();

#CONFIG
NAMES = {
    'bus': 0,
    'car': 1,
    'truck': 2,
}

def get_coords(size, rect):
    x = (rect[0] + rect[1]) / 2.0 * (1.0 / size[0])
    y = (rect[2] + rect[3]) / 2.0 * (1.0 / size[1])
    w = (rect[1] - rect[0]) * (1.0 / size[0])
    h = (rect[3] - rect[2]) * (1.0 / size[1])
    return (x,y,w,h)
    
start = time.time()
directory = askdirectory(title="Select the directory of the VOC dataset")

print(f'[ i ] Converting VOC dataset to YOLO format...\n[ i ] Directory: {directory}')
for file in glob.glob(directory + "/*.xml"):
    xmldoc = minidom.parse(file)
    object_list = xmldoc.getElementsByTagName('object')

    size = xmldoc.getElementsByTagName('size')[0]
    width = int(size.getElementsByTagName('width')[0].firstChild.data)
    height = int(size.getElementsByTagName('height')[0].firstChild.data)

    for obj in object_list:
        obj_name = obj.getElementsByTagName('name')[0].firstChild.data
        if obj_name in NAMES:
            label_idx = str(NAMES[obj_name]) 
        else:
            print(f"Object not found: {obj_name}")
            exit()

        bndbox = obj.getElementsByTagName('bndbox')[0]
        xmin = float(bndbox.getElementsByTagName('xmin')[0].firstChild.data)
        ymin = float(bndbox.getElementsByTagName('ymin')[0].firstChild.data)
        xmax = float(bndbox.getElementsByTagName('xmax')[0].firstChild.data)
        ymax = float(bndbox.getElementsByTagName('ymax')[0].firstChild.data)
        with open(file[:-4]+'.txt', 'a') as save:
            save.write(label_idx + " " + " ".join([("%.6f" % i) for i in get_coords((width, height), (xmin, xmax, ymin, ymax))]) + '\n')

print(f'[ + ] Done!\n[ i ] Time: {round(time.time() - start, 2)}s')

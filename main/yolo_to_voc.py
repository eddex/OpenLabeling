# Script to convert yolo annotations to voc format

# Sample format
#<annotation>
#    <folder>input</folder>
#    <filename>signal-3979.jpg</filename>
#    <path>/home/larry/git/OpenLabeling/main/input/signal-3979.jpg</path>
#    <source>
#        <database>Unknown</database>
#    </source>
#    <size>
#        <width>416</width>
#        <height>416</height>
#        <depth>3</depth>
#    </size>
#    <segmented>0</segmented>
#    <object>
#        <name>9</name>
#        <pose>Unspecified</pose>
#        <truncated>0</truncated>
#        <difficult>0</difficult>
#        <bndbox>
#            <xmin>140</xmin>
#            <ymin>281</ymin>
#            <xmax>164</xmax>
#            <ymax>333</ymax>
#        </bndbox>
#    </object>
#</annotation>
import os
import xml.etree.cElementTree as ET
from PIL import Image

ANNOTATIONS_DIR_PREFIX = "output/YOLO_darknet/"

DESTINATION_DIR = "output/PASCAL_VOC"

CLASS_MAPPING = {
    '0': '1',
    '1': '2',
    '2': '3',
    '3': '4',
    '4': '5',
    '5': '6',
    '6': '7',
    '7': '8',
    '8': '9',
    '9': 'start'
    # Add your remaining classes here.
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "input"
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "path").text = "{}/input/{}.jpg".format(os.getcwd(), file_prefix)
    print(os.getcwd())
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(root, "segmented").text = "0"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = str(voc_label[0])
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(int(voc_label[1]))
        ET.SubElement(bbox, "ymin").text = str(int(voc_label[2]))
        ET.SubElement(bbox, "xmax").text = str(int(voc_label[3]))
        ET.SubElement(bbox, "ymax").text = str(int(voc_label[4]))
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file(file_name):
    file_prefix = file_name.split(".txt")[0]
    image_file_name = "{}.jpg".format(file_prefix)
    img = Image.open("{}/{}".format("input", image_file_name))
    w, h = img.size
    file_path = '{}{}'.format(ANNOTATIONS_DIR_PREFIX, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split(' ', 5)
            if CLASS_MAPPING.get(data[0]) == None:
                print ("Error class {} doesn't exist!".format(data[0]))
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_name))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()

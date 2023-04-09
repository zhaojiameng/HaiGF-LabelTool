import xml.etree.ElementTree as ET
import json
import os

def convert_xml_to_json(xml_file_path, json_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    data = {}
    data['annotations'] = []
    for obj in root.findall('object'):
        annotation = {}

        name = obj.find('name').text
        annotation['label'] = name

        bbox = obj.find('bndbox')
        annotation['xmin'] = int(float(bbox.find('xmin').text))
        annotation['ymin'] = int(float(bbox.find('ymin').text))
        annotation['xmax'] = int(float(bbox.find('xmax').text))
        annotation['ymax'] = int(float(bbox.find('ymax').text))

        data['annotations'].append(annotation)

    with open(json_file_path, 'w') as f:
        json.dump(data, f)

def convert_folder_to_json(xml_folder_path, json_folder_path):
    if not os.path.exists(json_folder_path):
        os.makedirs(json_folder_path)

    for filename in os.listdir(xml_folder_path):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(xml_folder_path, filename)
            json_file_path = os.path.join(json_folder_path, filename[:-4] + '.json')
            convert_xml_to_json(xml_file_path, json_file_path)

def convert_json_to_xml(json_file_path, xml_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    root = ET.Element('annotation')

    filename_elem = ET.SubElement(root, 'filename')
    filename_elem.text = data['filename']

    size_elem = ET.SubElement(root, 'size')
    width_elem = ET.SubElement(size_elem, 'width')
    width_elem.text = str(data['width'])
    height_elem = ET.SubElement(size_elem, 'height')
    height_elem.text = str(data['height'])
    depth_elem = ET.SubElement(size_elem, 'depth')
    depth_elem.text = str(data['depth'])

    for annotation in data['annotations']:
        object_elem = ET.SubElement(root, 'object')

        name_elem = ET.SubElement(object_elem, 'name')
        name_elem.text = annotation['label']

        bndbox_elem = ET.SubElement(object_elem, 'bndbox')
        xmin_elem = ET.SubElement(bndbox_elem, 'xmin')
        xmin_elem.text = str(int(annotation['xmin']))
        ymin_elem = ET.SubElement(bndbox_elem, 'ymin')
        ymin_elem.text = str(int(annotation['ymin']))
        xmax_elem = ET.SubElement(bndbox_elem, 'xmax')
        xmax_elem.text = str(int(annotation['xmax']))
        ymax_elem = ET.SubElement(bndbox_elem, 'ymax')
        ymax_elem.text = str(int(annotation['ymax']))

    tree = ET.ElementTree(root)
    tree.write(xml_file_path)

def convert_folder_to_xml(json_folder_path, xml_folder_path):
    if not os.path.exists(xml_folder_path):
        os.makedirs(xml_folder_path)

    for filename in os.listdir(json_folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(json_folder_path, filename)
            xml_file_path = os.path.join(xml_folder_path, os.path.splitext(filename)[0] + '.xml')
            convert_json_to_xml(json_file_path, xml_file_path)
            
if __name__ == '__main__':
    xml_folder_path = 'D:/bubbleImage/pre_label'
    json_folder_path = 'D:/bubbleImage/pre_label_json'
    convert_folder_to_json(xml_folder_path, json_folder_path)

   




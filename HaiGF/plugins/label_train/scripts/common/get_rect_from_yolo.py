def get_rect_from_yolo(yolo_path):
    labels = []
    with open(yolo_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            label = {}
            line = line.strip()
            line = line.split(' ')
            label['class'] = line[0]
            label['x_center'] = float(line[1])
            label['y_center'] = float(line[2])
            label['width'] = float(line[3])
            label['height'] = float(line[4])
            labels.append(label)
    return labels
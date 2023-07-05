import base64
import json
import requests
import numpy as np

url = "http://aiapi.ihep.ac.cn:42901/v1/inference"
model = "meta/segment_anything_model"
api_key = 'HmwJJYFBoIuwXkrRrmGzwUZhbnCSgh'

def prompt_segment(input_points=None, input_labels=None, input_boxes=None, img=None):
    messages = {}
    """
    convert image to base64
    """
    if img is not None:
        with open(img, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        messages["img"] = encoded_image

    messages["auto_mask"] = False
    if input_points is not None:
        messages["input_points"] = input_points
    if input_labels is not None:
        messages["input_labels"] = input_labels
    if input_boxes is not None:
        messages["input_boxes"] = input_boxes

    return get_mask_from_sam(messages)

def auto_segment(img=None):
    messages = {}
    """
    convert image to base64
    """
    if img is not None:
        with open(img, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        messages["img"] = encoded_image

    messages["auto_mask"] = True

    return get_mask_from_sam(messages)

def get_mask_from_sam(messages:dict, stream=False):
    """
    send the request
    """
    response = requests.post(
        url,
        json={
            "model": model,
            "api_key": api_key,
            "stream": stream,
            "messages": messages,
        },
        timeout=1000,
        stream=True
    )
    if response.status_code != 200:
        raise Exception(f"Got status code {response.status_code} from server: {response.text}")

    data = response.json()
    if data['status_code'] != 42901:
        raise Exception(f"Got status code {data['status_code']} from server: {data['message']}")
    """the message is a mask list, transform it to a numpy array, and save it as a jpg file"""
    mask = data['message']
    mask = np.array(mask)
    """
    return the mask, or save it as a jpg file, or do something else
    :case1:plot mask on the image
            # 假设原图和掩码存在变量img和mask中
            # 调整掩码的颜色通道，以便将其叠加在原图上
            mask = mask[:, :, np.newaxis]
            mask = np.concatenate([mask, mask, mask], axis=2)

            # 将原图和掩码叠加在一起
            overlay = np.where(mask == 0, img, 0.5 * img + 0.5 * mask)

            

    surely the mask returned is a list, not a numpy array
    """
    return mask

    
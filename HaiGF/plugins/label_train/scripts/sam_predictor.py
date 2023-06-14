import base64
import json
import requests
import numpy as np

url = "http://127.0.0.1:42901/v1/inference"
model = "hepai/segment_anything"
api_key = 'HmwJJYFBoIuwXkrRrmGzwUZhbnCSgh'
def get_mask_from_sam(auto_mask=False, input_point=None, input_label=None, input_box=None, img=None, stream=False, stream_interval=0):
    """
    get mask from sam via hai
    :param auto_mask: auto mask
    :param input_point: input point
    :param input_label: input label
    :param input_box: input box
    :param img: image
    """

    """
    convert image to base64
    """
    with open(img, "rb") as image_file:
        image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    """
    prepare the messages
    """
    if auto_mask:
        messages = {
            "auto_mask": auto_mask,
            "img": encoded_image,
        }
    else:
        messages = {
            "auto_mask": auto_mask,
            "input_point": input_point,
            "input_label": input_label,
            "input_box": input_box,
            "img": encoded_image,
        }

    """
    send the request
    """
    response = requests.post(
        url,
        json={
            "model": model,
            "api_key": api_key,
            "stream": stream,
            "stream_interval": stream_interval,  # additional stream interval
            "messages": messages,
        },
        
        stream=True
    )
    if response.status_code != 200:
        raise Exception(f"Got status code {response.status_code} from server: {response.text}")


    if not stream:
        # print(response.content)  # 只有非流式相应才能查看内容
        data = response.json()
        """the message is a mask list, transform it to a numpy array, and save it as a jpg file"""
        mask = data['message']
        mask = np.array(mask)
        # plt.imsave('mask2.jpg', mask)
        # print(f'data: {data} {type(data)} {data.keys()}')

    else:
        full_response = ""
        print('streaming:')
        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if not chunk:
                continue
            # line = line.decode('utf-8')
            chunk = chunk.decode('utf-8')
            if chunk == "[DONE]":
                break
            # print(f'line: {line}')
            # print(f'chunk: {chunk}')
            # print(chunk, end='')
            full_response += chunk
            print(f'\r{full_response}', end='')
        print('\n')

    """
    return the mask, or save it as a jpg file, or do something else
    """
    return mask

    
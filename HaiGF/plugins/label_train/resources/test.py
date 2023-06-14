import requests
import numpy as np

# url = 'http://192.168.32.148:4998/upload'
# file_path = 'HaiGF/plugins/label_train/resources/000000.jpg'

# with open(file_path, 'rb') as file:
#     response = requests.post(url, files={'file': file})

# if response.status_code == 200:
#     print('Upload success')
# else:
#     print('Upload failed')

# input_point = np.array([[170, 280]])
# input_label = np.array([1])
# url = 'http://127.0.0.1:4997/predict'
# data = {'auto_mask': False, 'input_data': {'img_path':'notebooks/images/dog.jpg', 'input_point': input_point.tolist(), 'input_label': input_label.tolist() }}

# response = requests.post(url, json=data)

# if response.status_code == 200:
#     output_data = response.json()['output_data']
#     print('Output data:', output_data)
# else:
#     print('Error:', response.text)
from gradio_client import Client

client = Client("http://localhost:7579/")
result = client.predict(
				"C:/Users/dell/Desktop/OIP.jfif", 	# str representing input in 'parameter_5' Image component
				"dog",	# str representing input in 'Detection Prompt' Textbox component
				0.25,	# int | float representing input in 'Box Threshold' Slider component
				0.25,	# int | float representing input in 'Text Threshold' Slider component
                "sample1.jpg",	# str representing input in 'parameter_6' Image component
                fn_index=0,
)
print(result)

# import requests

# url = 'http://localhost:7579/api/predict'
# with open('C:/Users/dell/Desktop/OIP.jfif', 'rb') as f:
#     files = {'input_image': f}
#     data = {"grounding_caption": "dog", "box_threshold": 0.25, "text_threshold": 0.25, "fn_index": 0}
#     response = requests.post(url, files=files, data=data)

# if response.status_code == 200:
#     print(response.json()["outputs"])
# else:
#     print('Error:', response.text)
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

input_point = np.array([[170, 280]])
input_label = np.array([1])
url = 'http://127.0.0.1:4997/predict'
data = {'auto_mask': False, 'input_data': {'img_path':'notebooks/images/dog.jpg', 'input_point': input_point.tolist(), 'input_label': input_label.tolist() }}

response = requests.post(url, json=data)

if response.status_code == 200:
    output_data = response.json()['output_data']
    print('Output data:', output_data)
else:
    print('Error:', response.text)
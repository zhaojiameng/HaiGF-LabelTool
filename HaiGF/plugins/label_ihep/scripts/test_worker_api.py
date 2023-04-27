import requests
import json
from json import JSONDecodeError

model = "hepai/demo_model"

# 获取worker地址
response = requests.post(
    "http://192.168.68.22:42901/get_worker_address",
    json={
        "model": model,
    }
)
print(response.json())

# 设置数据集
response = requests.post(
    "http://192.168.68.22:42901/worker_generate_stream",
    json={
        #"model": "hepai/demo_model",
        "model": model,
        "task": "set_dataset",
        # "model": "gpt2/fast-tokenizer",
        "dataset_name": "hep_qa_datasets",
    }
)
print(response.json())

# 获取数据集信息
response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                        json={ 
                            "model": model,
                            "task": "get_dataset_info",
                            "dataset_name": "hep_qa_datasets",
                            "info": "label_list",
                        }
                    )

print(response.json())

# 以流式响应的方式获取10条数据，起始位置为 index，如果 index不设置，则随机
response = requests.post("http://192.168.68.22:42901/worker_generate_stream", 
                        json={
                         "model": model, # 模型名称，一个模型对应一个worker
                         "dataset_name": "hep_qa_datasets", # 数据集名称
                         "task": "get_data_stream", # 获取数据流
                         "number": 10, # 获取10条数据
                         "index": 0, # 起始位置为 index，如果 index不设置，则随机
                         "read_lock": True, # 设置为读取已经锁定的数据
                         "read_label": True, # 设置为读取已经标注的数据
                         "stream": True # 设置为流式响应
                         }, 
                        stream=True # 设置为流式响应
                        )


# 解析stream并输出每个字典的元素
stream = b""
for chunk in response.iter_content(chunk_size=10):
    stream += chunk
    # 查找字典的结束位置
    dict_end = stream.find(b"\0", 0)
    if dict_end == -1:
        # 如果没有找到下一个字典的结束位置，退出循环
        continue
    
    # 解析并输出
    try:
        dict = json.loads(
            stream[0:dict_end].decode("utf-8"))
        index = dict['index']
        data = dict['data']
        print("id: ", data['id'],
              "question: ", data['question'],
              "category: ", data.get('category', None),
              "answer_quality: ", data.get('answer_quality', None))
        stream = stream[dict_end+1:]
    except JSONDecodeError:
        continue


for i in range(1):
    index = i
    print("index: ", index)
    # 以列表的方式获取10条数据，起始位置为 index，如果 index不设置，则随机
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                        json={
                            "model": model,
                            "task": "read_data",
                            "dataset_name": "hep_qa_datasets",
                            "index": index,
                            "number": 10,
                            "read_lock": True,
                            "read_label": True,
                            }
                        )
    #for chunk in response.iter_content(chunk_size=1024):
    #    print(chunk.decode("utf-8"))
    data_part = response.json()['message']
    for data in data_part:
        index = data['index']
        data = data['data']
        print("id: ", data['id'],
              "question: ", data['question'],
              "category: ", data.get('category', None),
              "answer_quality: ", data.get('answer_quality', None))

    # 修改标签
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                        json={
                            "model": model,
                            "task": "annotation",
                            "dataset_name": "hep_qa_datasets",
                            "method": "update_label",
                            "index": index,
                            "category": "hep",
                            "answer_quality": 0, 
                            }
                        )
    print(response.json())
    
    # update_label_by_ai
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                             json={
                                 "model": model,
                                 "task": "annotation",
                                 "dataset_name": "hep_qa_datasets",
                                 "method": "update_label_by_ai",
                                 "index": index,
                                 "category": "hep",
                                 "answer_quality": 0,
                                 "proxy": "http://127.0.0.1:1095",  # 代理
                                 "ai_api_key": "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",
                             }
                             )
    print(response.json())
    
    # read data
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                             json={
                                 "model": model,
                                 "task": "read_data",
                                 "dataset_name": "hep_qa_datasets",
                                 "index": 20,
                                 "number": 10,
                                 "read_lock": True,
                             }
                             )
    data_part = response.json()['message']
    for data in data_part:
        # print(data)
        index = data['index']
        data = data['data']
        print("id: ", data['id'],
            "question: ", data['question'],
            "category: ", data.get('category', None),
            "answer_quality: ", data.get('answer_quality', None))


# 保存数据集到硬盘
response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                            json={
                                "model": model,
                                "task": "save_dataset",
                                "dataset_name": "hep_qa_datasets",
                            }
                            )
print(response.json())
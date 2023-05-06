import requests
import json
from json import JSONDecodeError

model = "hepai/demo_model"


def get_data(user=None):
    
    # 以列表的方式获取10条数据，起始位置为 index，如果 index不设置，则随机
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                        json={
                            "model": model,
                            "task": "read_data",
                            "dataset_name": "hep_qa_datasets",
                           
                            "number": 50,
                            "read_locked": True,
                            "read_labeled": False,
                            "user": user,
                            
                            }
                        )
    data_part = response.json()['message']
    # print(data_part)
    return data_part

def update_label(index, category, answer_quality, artificial_answer, labeler):
    # update label
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                        json={
                            "model": model,
                            "task": "annotation",
                            "dataset_name": "hep_qa_datasets",
                            "method": "update_label",
                            "index": index,
                            "category": category,
                            "answer_quality": int(answer_quality), 
                            "artificial_answer": artificial_answer,
                            "user": labeler,
                            }
                        )
    # print(response.json())
    
    return response.json()

def save_dataset(user):
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                            json={
                                "model": model,
                                "task": "save_dataset",
                                "dataset_name": "hep_qa_datasets",
                                "user": user,

                            }
                            )
    print(response.json())

def get_list(info, user):
    """info:category_list, label_list"""
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                            json={
                                "model": model,
                                "task": "get_dataset_info",
                                "dataset_name": "hep_qa_datasets",
                                "info": info,
                                "user": user,
                            }
                            )
    
    return response.json()['message']

def ai_annotiation(index):
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
    return response.json()['message']

def set_datasets(user):
    """set_datasets"""
    response = requests.post("http://192.168.68.22:42901/worker_generate_stream",
                            json={
                                "model": model,
                                "user": user,
                                "task": "set_dataset",
                                "dataset_name": "hep_qa_datasets",
                            }
                            )
    
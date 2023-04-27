import hai

models = hai.Model.list()  # 列出可用模型
print(models)

system_prompt = "You are ChatGPT, answering questions conversationally"


api_key = 'h89nWl6gH3NK0F1NFSNzPF0bKV0ORN'

def get_annotation(question, answer, labelList):
    prompt = f"阅读下面的问题和答案，从下面的categorys中选择一个category，仅返回一个键为category,值为categorys中的元素的键值对，不确定的时候值为Others。\n问题：{question}\n答案：{answer}\ncategorys：{labelList}"
    result = hai.LLM.chat( # 生成对话
            model='hepai/gpt-3.5-turbo',
            api_key=api_key,
            messages=[
                
                {"role": "system", "content": system_prompt},   
                {"role": "user", "content": prompt},
            ],  
            stream=True,
        )
    full_result = ""    
    for i in result:
        full_result += i
    print(full_result)
    return full_result




    

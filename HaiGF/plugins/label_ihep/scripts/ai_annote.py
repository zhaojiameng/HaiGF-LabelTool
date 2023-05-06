import hai

models = hai.Model.list()  # 列出可用模型
print(models)

system_prompt = "You are ChatGPT, answering questions conversationally"


api_key = 'HmwJJYFBoIuwXkrRrmGzwUZhbnCSgh'

def get_annotation(question, answer, labelList):
    prompt = f"阅读下面的问题和答案, 判断其涉及的领域category,仅返回一个键值对 category:value,当你的判断category在categorys中出现时,value为该category,若不在或不确定时,value为Others。\n问题：{question}\n答案：{answer}\ncategorys：{labelList}"
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
    return full_result




    

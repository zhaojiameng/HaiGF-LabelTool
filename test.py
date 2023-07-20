# 查看模型是否已经注册
import hai

host = 'aiapi.ihep.ac.cn'  # 模型服务器地址
port = 42901  # 模型服务器端口
# hai.Model.list(host=host, port=port)
print(hai.Model.list(host=host, port=port))



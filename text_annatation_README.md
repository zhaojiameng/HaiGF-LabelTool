# 标注文本问答对
代码所在位置： HaiGF/Plugins/label_ihep

## 启动方式
创建环境：
conda create -f environment.yml
运行入口文件：python run_framework.py
运行界面如 'HaiGF/Plugins/label_ihep/GUI界面'所示

## 要点
'HaiGF/Plugins/label_ihep/script/data_process'文件
get_data方法：从服务器获取原始数据，需按自己需求更改接口
get_list方法：获取标注标签列表，可直接定义

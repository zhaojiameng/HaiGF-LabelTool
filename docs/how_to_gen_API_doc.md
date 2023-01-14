
## 如何自动生成API文档

本文介绍如何使用[Sphinx](https://github.com/sphinx-doc/sphinx)自动生成Python软件的API文档。

生成的文档通过浏览器访问，界面如图：
![API_doc_example](https://zhangzhengde0225.github.io/images/blog/api_doc_example.png)


### 1. 安装Sphinx和初始化

```bash
pip install -U sphinx  # 安装Sphinx

cd docs/api_doc  # 进入生成文档的保存目录
sphinx-quickstart  # 初始化Sphinx
```
初始化后，会创建配置文件`conf.py`和`index.rst`等文件。
其中，`conf.py`是Sphinx的配置文件，`index.rst`是Sphinx的主页文件。

### 2. 生成文档

```bash
make html  # 生成html文档
```
生成的文档在`docs/api_doc/_build/html`目录下，入口是`index.html`，可以直接用浏览器打开。

进行后面的配置后，可以直接执行`make html`重新生成文档。

### 3. 更新API文档具体内容
详细配置方法参考[Sphinx官方文档](https://www.sphinx-doc.org/zh_CN/master/usage/quickstart.html)。
#### （1） 配置`conf.py`

`conf.py`指定了项目名、版权、作者信息，以及生成文档的格式等。

+ **切换主题**
在`conf.py`中，可以指定主题。默认主题是`alabaster`，可以切换到`furo`主题。
    ```python
    html_theme = 'furo'
    ```
    注意：使用`furo`主题，需要安装`furo`包: `pip install furo`。

#### （2） 配置`index.rst`

`index.rst`采用reStructedText语法（[rst语法规则](https://blog.csdn.net/u012294613/article/details/122512623)），与markdown类似。主页面的内容可以在`index.rst`中修改。
其中，包含目录树。

### 4. 发布文档

#### （1） 通过Python http.server发布

> 注意：该方案无加密验证，简单方便，但不安全，适用于测试环境，不适用于生产环境，用于生产请参考（2）。

将文档发布到本机端口`8000`上:
```bash
cd docs/api_doc
python -m http.server -d _build/html 8000
```
可以通过`http://localhost:8000`或主机的ip地址`http://<your ip>:8000`访问。


#### (2) 通过Nginx发布安全的文档访问服务

TODO










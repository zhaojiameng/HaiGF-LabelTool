


## 如何翻译GUI界面

GUI通常用英文开发，如需要快速翻译成其他语言，例如中文，可以使用工具。

### 1.自动搜索.py文件内的需翻译的文本，生成翻译ts文件

使用lupdate工具，自动搜索需要翻译的文本，生成翻译ts文件。lupdate工具使用pip安装PyQt5或PySIde2时自动安装。

```bash
pyside2-lupdate <path to your .py files> -ts <.ts save path>
# i.e. pyside2-lupdate hai_ltt/gui_framework/main_window/main_window.py -ts hai_ltt/gui_framework/translate/translate_zh_CN.ts
```
可以同时指定多个.py文件，或多次运行，生成1个ts文件

注意：lupdate工具搜索.py文件内的`self.tr()`函数，所以需要在需要翻译的文本前加上`self.tr()`。
例如：
```python
self.setWindowTitle(self.tr('HAI GUI Framework'))
```

>或者使用本项目的脚本搜索所有.py文件，生成ts文件：`python scripts/gen_ts.py`

### 2.手动翻译ts文件，生成qm文件

#### 1.安装[Qt Linguist](https://doc.qt.io/qt-5/qtlinguist-index.html)

如果使用anaconda安装PyQt5，则Linguist安装路径在`<conda path>/bin/linguist`或`<conda path>/envs/<env name>/linguist`，例如：`/home/zzd/anaconda3/bin/linguist`.

也可以到[Qt官网](https://www.qt.io/download)下载安装包。
安装后打开Qt Linguist，打开刚才生成的ts文件，即可开始翻译。

启动linguist，并加载.ts文件后可以看到如下界面：
![linguist](https://zhangzhengde0225.github.io/images/blog/linguist.png)

手动翻译：选择一个`上下文`，选中一个`源文`，在`Trabslation to 简体中文(中国)`下方输入翻译后的文本，并按`ALT+Enter`保存和自动切换到下一个文本。

生成.qm文件，点击菜单栏`文件`->`发布`，生成的qm文件保存在.ts文件同目录下。

### 3.加载qm文件实现翻译

在启动主程序前，加载翻译文件，即可自动翻译GUI界面。
```python
translator = QTranslator()
translator.load("<path to .qm file>")  # 加载.qm文件，若文件不存在，则不翻译

app = QApplication(sys.argv)
app.installTranslator(translator)  # 安装翻译器
```

若需要翻译其他语言，采用同样的方法，生成对应语言的ts文件和qm文件，加载qm文件即可。



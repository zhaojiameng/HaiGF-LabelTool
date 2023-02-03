

# 1. Introduction

HAI GUI是可扩展、轻量化的用于开发基于机器学习算法的应用程序的框架。

+ 采用模块化设计，可扩展性强，可灵活添加新的模块。
+ 采用基于HAI算法库的前后端分离设计，实现界面的轻量化。

## 1.1 Main Window
![hai_gui_framework](https://zhangzhengde0225.github.io/images/blog/hai_gui_framework_1280.gif)


主界面分为5个模块：核心功能栏、主侧栏、中央控件、辅助侧栏和面板栏。

### 1.1.1 核心功能栏
核心功能栏在左侧，由图标工具组成，例如：资源管理器、标注工具、AI工具等，可通过点击图标切换到相应的模块。可通过开发插件添加新的功能。

### 1.1.2. 主侧栏
主侧栏是核心功能的具体展开，由一个不可移动的左侧Dock坞构成，包含标题、标题右侧工具图标和内容工具。可开发控件添加到主侧栏，并与核心功能绑定。

### 1.1.3. 中央控件
中央控件用于展示核心功能的具体内容、可视化数据并与人进行交互。
中央控件基于选项卡(Tab)和页面(Page)的设计，可通过选项卡切换不同的页面。可通过开发控件添加到中央控件，并与核心功能或主侧栏的操作绑定。
在中央控件内部，通过QSplitter实现自动分屏器，可通过拖动Tab实现自动分屏。

### 1.1.4. 辅助侧栏
辅助侧栏位于主界面的右侧，用于展示详细属性、信息，设置一些参数等。

### 1.1.5. 面板栏
面板栏位于主界面的底部，通过对选项卡的方式实现多个输出。


# 2. How to develop plugin

实现插件的主要步骤如下：
- 在`HaiGF/plugins`目录下创建新的文件夹，文件夹名即为插件名，例如：`hai_tools`。
- 在`hai_tools`文件夹下创建`__init__.py`文件，用于初始化插件。
- 在`__init__.py`文件中创建插件类，继承`HPlugin`类，并重写`install`方法。
- 在`HaiGF/__main__.py`中启动UI时，安装插件。
- 插件安装后，可通过插件类名访问插件对象，例如`hai_tools`插件类名为`AIPlugin`，通过`mw.AIPlugin`或`mw.plugins["AIPlugin"]`访问插件。

## 2.1 Create custom plugin

HGF提供了插件父类`HPlugin`，继承该类后，自动获得主窗口及其五个主要部件的引用, 便于窗口交互。
```python
from HaiGF import HPlugin

class CustomerPlugin(HPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        """
        继承后，自动获得如下对象：
        self.mw:  HMainWindow  # 主窗口
        self.cfb: HMainWidow.core_func_bar  # 核心功能栏
        self.msb: HMainWindow.main_side_bar  # 主侧边栏
        self.cw:  HMainWindow.central_widget  # 中央控件
        self.asb: HMainWindow.aux_side_bar  # 辅助侧边栏
        self.pw:  HMainWindow.panel_widget  # 面板控件
        """
        pass
    
    def install(self):
        """
        需要重写该函数，实现插件安装时的操作，例如：在核心功能栏添加action，在主侧栏添加控件等。
        """
        pass

    def custom_func(self):
        """
        自定义函数，可通过插件类名访问，例如：mw.CustomerPlugin.custom_func()
        """
        pass
```
插件与主界面的交互详见文档。

## 2.2 Install plugin when start UI

在`HaiGF/__main__.py`中，调用`install_plugin`函数，安装插件。
```python
from HaiGF.plugins.<CUSTOMER PLUGIN FOLD> import CustomerPlugin

mw.install_plugin(CustomerPlugin)  # 继承了HPlugin的自定义类直接传入即可
```

## 2.3 Access plugin object

插件安装后，可通过插件类名`mw.<PLUGIN NAME>`或`mw.plugins["<PLUGIN NAME>"]`访问插件对象.

Example:
```python
ai_plugin = mw.CustomerPlugin  # 通过插件类名访问插件对象
ai_plugin = mw.plugins["CustomerPlugin"]  # 通过插件类名访问插件对象
```










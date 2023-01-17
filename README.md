<!-- [![Stars](https://img.shields.io/github/stars/zhangzhengde0225/damei)](
https://github.com/zhangzhengde0225/damei)
[![Open issue](https://img.shields.io/github/issues/zhangzhengde0225/damei)](
https://github.com/zhangzhengde0225/damei/issues)
[![Source_codes](https://img.shields.io/static/v1?label=Download&message=src&color=orange)](
https://github.com/zhangzhengde0225/damei/archive/refs/heads/master.zip) -->
[![Source_codes](https://img.shields.io/static/v1?label=ReadDocs&message=API&color=blue)](
http://47.114.37.111)

## HAI GUI 框架

HAI GUI Framework是可扩展、轻量化的用于开发基于机器学习算法的应用程序的框架。

+ 采用模块化设计，可扩展性强，可灵活添加新的模块。
+ 采用基于HAI算法库的前后端分离设计，实现界面的轻量化。

## 主界面
![hai_gui_framework](https://zhangzhengde0225.github.io/images/blog/hai_gui_framework_1280.gif)


主界面分为5个模块：核心功能栏、主侧栏、中央控件、辅助侧栏和面板栏。

### 1. 核心功能栏Core Func Bar
核心功能栏在左侧，由图标工具组成，例如：资源管理器、标注工具、AI工具等，可通过点击图标切换到相应的模块。可通过开发插件添加新的功能。

### 2. 主侧栏
主侧栏是核心功能的具体展开，由一个不可移动的左侧Dock坞构成，包含标题、标题右侧工具图标和内容工具。可开发控件添加到主侧栏，并与核心功能绑定。

### 3. 中央控件
中央控件用于展示核心功能的具体内容、可视化数据并与人进行交互。
中央控件基于选项卡(Tab)和页面(Page)的设计，可通过选项卡切换不同的页面。可通过开发控件添加到中央控件，并与核心功能或主侧栏的操作绑定。
在中央控件内部，通过QSplitter实现自动分屏器，可通过拖动Tab实现自动分屏。

### 4. 辅助侧栏
辅助侧栏位于主界面的右侧，用于展示详细属性、信息，设置一些参数等。

### 5. 面板栏
面板栏位于主界面的底部，通过对选项卡的方式实现多个输出。
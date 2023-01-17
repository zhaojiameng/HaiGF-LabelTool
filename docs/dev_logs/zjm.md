
# 2023.01.09-13日志

## 问题描述

1.实现画布（canvas)页面，点击主侧栏的文件时，将文件展示到画布上。（暂时只考虑图片）

2.画布随窗体放缩， 画布可在窗体内放缩

## 问题1思路

1.画布实现思路：graphicsScene作为画布，借助graphicsView呈现。

2.根据画布特征重写mousePress, mouseRelease等函数

3.写加载图片函数。基于cv,通过文件路径进行加载。

4.绑定主侧栏双击文件信号到加载图片函数上。

```
加载图片闪退
```



QLabel显示图片，可行。

```
def __init__(self, parent=None, icon=None, title=None, **kwargs):
        super().__init__(parent, icon, title, **kwargs)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.img = QtWidgets.QLabel(self)
        self.img.setObjectName("img")
        self.openImg = QtWidgets.QPushButton(self)
        self.openImg.setObjectName("openImg")
        self.openImg.clicked.connect(self.load_img(filePath='000000.jpg'))
        self.horizontalLayout.addWidget(self.img)
        self.horizontalLayout.addWidget(self.openImg)

    def load_img(self,filePath):
        image = QtGui.QPixmap(filePath)
        self.img.setPixmap(image)
        self.img.show()

```



## 问题2思路

1.页面添加布局，画布是单控件，任一布局都可。

将画布控件加入布局，实现随窗体放缩。 （实现）

2.重写wheelEvent，实现画布在窗体内的放缩。



## 其它

1.examples界面，针对range控制条，实现数值的显示

2.解决运行时，报unknown的警告。






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

## 2.5-2.12日志
label_train插件开发

1.主侧栏双击图片，加载到annotate_train页面
2.鼠标悬浮在图片上时，显示位置，pix和值
3.ROI的绘制，， 三维数据求均值到一维后，画出曲线， ROI可移动，同步更新曲线
4.等值线的绘画，图片右侧是阈值。随阈值更改，更新等值线。

## 2.23
1.label_train插件主测栏添加   canny边缘检测
2.点击“canny”边缘检测，作用于右侧imageAnalysis中的图片
3.右键菜单一 ：撤销操作，还原至进行canny边缘检测之前
  右键菜单二： 保存标注， 自动计算每个检测轮廓的最小外接矩形，以yolo格式保存
canny也不能分割出气泡和背景

## 2.27
1.撤销边缘检测的功能更改为：运行旁的“撤销”按钮触发
2.线、圆形、椭圆、矩形、多边形ROI的实现，用于标注
3.ROI分析，等值分析抽离成功能，放入主侧栏

## 2.28
1.roi区域做为标注形状，放入shape数组，重构roi绘制逻辑

## 3.1
1.句柄连线是贝塞尔曲线的ROI
问题1：直线仍绘制
问题2：左键点击新增句柄的功能在直线上
问题3：贝塞尔曲线的控制

* 局部放大功能,标注功能
1.双击时，将局部区域展示到新的tab
2.在新的tab页，鼠标点击拖动绘制标签框
3.右键选择保存
4.在原页拖动局部区域，新tab页的区域数据跟随变化
5.切页自动保存上一页的标注

问题
Traceback (most recent call last):
  File "d:\hai-gui-framework\HaiGF\plugins\label_train\widgets\msb_widget.py", line 62, in on_cancel_roiButton_clicked
    plg.cancel_ROI()
  File "d:\hai-gui-framework\HaiGF\plugins\label_train\antrain_plugin.py", line 108, in cancel_ROI
    if not self.page in self.cw.pages:
  File "d:\hai-gui-framework\HaiGF\gui_framework\widgets\central_widgets\central_widget.py", line 109, in pages
    return self.current_tab_widget().pages
  File "d:\hai-gui-framework\HaiGF\gui_framework\widgets\central_widgets\central_widget.py", line 125, in current_tab_widget
    assert pos is not None, '多个TabWidget时，需要传入pos参数'
AssertionError: 多个TabWidget时，需要传入pos参数             解决

关闭tab时,调用的函数名，是否可重写。
关闭tab时，分屏线还在，存在的tab不能全部填充

矩形框是局部图片的矩形框，保存的时候应当是以全图的角度来保存。 解决
何时进行保存，改换局部的时候，已有的矩形，如何处理            解决

编辑标签，点击cancel,置为‘'的问题                          解决

* control键开启图像处理
完成

* 贝塞尔曲线，不规则多边形功能
1.重写QgraphicsPloygonItem
2.a键开启编辑模式，绘制控制点、顶点，改变形状               解决
3.点击曲线边，新增点                                      解决
4.右击顶点，移除顶点，至少保留一个顶点                      解决

问题：
移动的问题：拖拽移动 解决 （不平滑，有残影）
死点：某些区域无法显示curve,这些区域的点不能响应
初始在极点附近，随形状拖拽变化

残影和死点是控制点及连线的问题

* 形状删除功能
1.当有形状时，右键开启不同的菜单
2.判断右键是否在形状上，开启删除菜单

问题：2的问题，判断处理很慢，roi形状判断不出来

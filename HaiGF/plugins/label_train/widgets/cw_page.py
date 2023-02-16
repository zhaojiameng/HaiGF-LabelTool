"""
The cw page.
It is a ImageAnalysis tool.
"""
import os
from pathlib import Path
import cv2
from PIL import Image
import numpy as np
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMenu, QAction, QFileDialog
from PySide2.QtGui import QCursor
from PySide2.QtCore import Qt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from HaiGF import HPage, HGF
from HaiGF.plugins.label_train.widgets.isocurve import MyIsocurve
from HaiGF.utils import general



import damei as dm


logger = dm.get_logger('cw_page')
here = Path(__file__).parent.parent

class ImageAnalysisPage(HPage):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.p = parent
        self.set_title(self.tr('annotate_train'))
        self.set_icon(HGF.ICONS('label_train'))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_rightmenu)
        self.image = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.getContextMenus(self.mousePressEvent)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.win = pg.GraphicsLayoutWidget()
        self.win.resize(800, 800)
        # self.win.addParentContextMenus(self.layout, self.layout_menu, self.win.mousePressEvent)
        self.layout.addWidget(self.win)
        self.p1 = self.win.addPlot(title="")
        self.p1.setMenuEnabled(False)

        # Item for displaying image data
        self.img = pg.ImageItem()
        self.img.hoverEvent = self.imageHoverEvent
        self.p1.addItem(self.img)

        self.create_ROI()
        # self.updatePlot()
        
        self.create_isocurve()

        # Contrast/color control
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.win.addItem(self.hist)
       

    
        
        self.create_isoLine()

        # set position and scale of image
        # tr = QtGui.QTransform()
        # self.img.setTransform(tr.scale(0.2, 0.2).translate(-50, 0))

        # zoom to fit image
        # self.p1.autoRange()  


        
        # Another plot area for displaying ROI data
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.p2.setMaximumHeight(250)
        self.p2.setMenuEnabled(False)
        self.win.show()

        self.txt = 'hello world'

    def create_rightmenu(self):
        """create rightmenu on layout"""
        #菜单对象
        self.layout_menu = QMenu(self)

        self.actionA = QAction(u'保存数据',self)#创建菜单选项对象
        self.actionA.setShortcut('Ctrl+S')#设置动作A的快捷键
        self.layout_menu.addAction(self.actionA)#把动作A选项对象添加到菜单self.win_menu上

        self.actionB = QAction(u'删除数据',self)
        self.layout_menu.addAction(self.actionB)

        self.actionA.triggered.connect(self.save_annotation) #将动作A触发时连接到槽函数 button
        self.actionB.triggered.connect(self.save_all_annotation)

        self.layout_menu.popup(QCursor.pos())#声明当鼠标在win控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    def save_annotation(self):
            """save single annotation"""
            print('okok-------')

   
    def save_all_annotation(self):
        """save all annotion on a image"""
        txt=self.txt
        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/" ,'txt(*.txt)')
        file=open(filepath,'w')
        print(filepath)
        file.write(txt)


    def create_img(self, img_path=None):
        """prepare the input image to analysis"""
        if img_path == None:
            data = np.random.normal(size=(200, 100))
            data[20:80, 20:80] += 2.
            data = pg.gaussianFilter(data, (3, 3))
            data += np.random.normal(size=(200, 100)) * 0.1
        else:
            assert isinstance(img_path, str)
                
            assert os.path.exists(img_path), f'img path not exists: {img_path}'
            # data = cv2.imread(img_path)
            data = Image.open(img_path)
        self.image = np.array(data)
        # build isocurves from smoothed data
        """axis=2 show zhe correct data ,why"""
        self.iso.setData(pg.gaussianFilter(self.image.mean(axis=2), (2, 2)))
        self.img.setImage(self.image)
        self.updatePlot()

    def create_ROI(self):
        self.roi = pg.ROI([200, 400], [100, 50])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.p1.addItem(self.roi)
        self.roi.setZValue(10)  # make sure ROI is drawn above image
        self.roi.sigRegionChanged.connect(self.updatePlot)
        
    # Callbacks for handling user interaction
    def updatePlot(self):
        selected = self.roi.getArrayRegion(self.image, self.img)
        d2 = selected.mean(axis=0)
        """3d data, but 1d data asked"""
        self.p2.plot(d2.mean(axis=1), clear=True)

    def create_isocurve(self):
        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=65, pen='g')
        # self.iso = MyIsocurve(level=65, pen='g')
        self.iso.setParentItem(self.img)
        self.iso.setZValue(5)
       
    

        
    def updateIsocurve(self):
        self.iso.setLevel(self.isoLine.value())
    
    def create_isoLine(self):
        # Draggable line for setting isocurve level
        self.isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        self.hist.vb.addItem(self.isoLine)
        self.hist.vb.setMouseEnabled(y=False) # makes user interaction a little easier
        self.isoLine.setValue(120)
        self.isoLine.setZValue(1000) # bring iso line above contrast controls
        self.isoLine.sigDragged.connect(self.updateIsocurve)



    def imageHoverEvent(self, event):
        """Show the position, pixel, and value under the mouse cursor.
        """
        if event.isExit():
            self.p1.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.image.shape[0] - 1))
        j = int(np.clip(j, 0, self.image.shape[1] - 1))
        # i = (np.clip(i, 0, self.image.shape[0] - 1))
        # j = (np.clip(j, 0, self.image.shape[1] - 1))
        # i = i.astype(np.int)
        # j = j.astype(np.int)
        val = self.image[i, j]
        ppos = self.img.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.p1.setTitle("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %s" % (x, y, i, j, val))


    #计算两数之和
    def add(self,a,b):
        return a+b
    

    #中国最好的三所大学
    def best_three_university(self):
        return '清华大学','北京大学','复旦大学'

        
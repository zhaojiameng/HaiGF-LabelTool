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
from HaiGF.plugins.label_train.my_ROI import MyPolyLineROI, MyRectROI, MyCircleROI, MyEllipseROI, MyLineROI, MyPolygonROI
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
      
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.win = pg.GraphicsLayoutWidget()
        self.win.resize(800, 800)
    
        self.layout.addWidget(self.win)
        self.p1 = self.win.addPlot(title="")
        self.p1.setMenuEnabled(False)

        # Item for displaying image data
        self.img = pg.ImageItem()
        self.img.hoverEvent = self.imageHoverEvent
        self.p1.addItem(self.img)

        self.win.show()
        self.txt = 'hello world'
        self.roi2 = None
        self.roiAny = None

    def analysis_ROI(self):
        if hasattr(self, 'p2'):
            print('ROI already here')
            return
        # Another plot area for displaying ROI data
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.p2.setMaximumHeight(250)
        self.p2.setMenuEnabled(False)

        self.create_ROI()
        self.updatePlot()

    def analysis_iso(self):
        if hasattr(self, 'hist'):
            print('iso already here')
            return
        self.create_isocurve()

        # Contrast/color control
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        #设置self.hist的高度与self.p1的高度一致
        self.hist.setMaximumHeight(self.p1.height())
        #添加self.hist到self.win中，位于self.p1的右边
        self.win.addItem(self.hist, row=0, col=2)
       
        self.create_isoLine()
        # build isocurves from smoothed data
        """axis=2 show zhe correct data ,why"""
        self.iso.setData(pg.gaussianFilter(self.image.mean(axis=2), (2, 2)))

    def cancel_iso(self):
        if not hasattr(self, 'hist'):
            print('No iso here')
            return
        self.iso.setData(None)
        self.win.removeItem(self.hist)
        del self.hist


    def create_rightmenu(self):
        """create rightmenu on layout"""
        #菜单对象
        self.layout_menu = QMenu(self)

        self.actionA = QAction(u'保存标注 & roi',self)#创建菜单选项对象
        # self.actionA.setShortcut('Ctrl+S')#设置动作A的快捷键
        self.layout_menu.addAction(self.actionA)#把动作A选项对象添加到菜单self.win_menu上

        self.actionB = QAction(u'保存标注 & canny',self)
        self.layout_menu.addAction(self.actionB)

        self.actionA.triggered.connect(self.save_all_roiAnno) #将动作A触发时连接到槽函数 button
        self.actionB.triggered.connect(self.save_all_annotation)

        self.layout_menu.popup(QCursor.pos())#声明当鼠标在win控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    def cancel_canny(self):
        self.img.setImage(self.image)

   
    def save_all_annotation(self):
        """save all annotion on a image"""
        #判断self.img里的image是否是self.image
        if self.img.image is self.image:
        
            print('canny dedect first')
            return
        binary = self.create_canny()
        k = np.ones((3, 3), dtype=np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_DILATE, k)

        result = []
        # 轮廓发现
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height = binary.shape[0]
        weight = binary.shape[1]
        for c in range(len(contours)):
            rect = cv2.boundingRect(contours[c])  # 轮廓的外接矩形
            x, y, w, h = cv2.boundingRect(contours[c])
            tem = [0, (x+w/2)/weight, (y+h/2)/height, w/weight, h/height]
            result.append(tem)
            cv2.rectangle(binary, rect, (0, 255, 0), 3)  # 没有旋转的外接矩形，绿色
            cv2.drawContours(binary, contours, c, (0, 0, 255), 2, 8)

        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/" ,'txt(*.txt)')
        file=open(filepath,'w')
        print(filepath)
        t = ''
    
        for i in result:
            for e in range(len(result[0])):
                t = t+str(i[e])+' '
            file.write(t.strip(' '))
            file.write('\n')
            t = ''

    def save_all_roiAnno(self):
        #保存每个roi的信息
        if not hasattr(self, 'roiAny'):
            print('no roi')
            return
        pass
      
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
        self.img.setImage(self.image)

    def create_ROI(self):
        self.roi = pg.ROI([200, 400], [100, 50])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.p1.addItem(self.roi)
        self.roi.setZValue(10)  # make sure ROI is drawn above image
        self.roi.sigRegionChanged.connect(self.updatePlot)
        

    def cancel_ROI(self):
        if not hasattr(self, 'p2'):
            print('No ROI here')
            return
        self.p1.removeItem(self.roi)
        self.roi = None
        self.win.removeItem(self.p2)
        del self.p2
        
    # Callbacks for handling user interaction
    def updatePlot(self):
        selected = self.roi.getArrayRegion(self.image, self.img)
        d2 = selected.mean(axis=0)
        """3d data, but 1d data asked"""
        self.p2.plot(d2.mean(axis=1), clear=True)

    def create_isocurve(self):
        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=65, pen='g')
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

    #对图片进行canny边缘检测，将结果以红色的线条显示在原图上
    def canny(self, threshold1=80, threshold2=160):
        image = self.create_canny(threshold1=threshold1, threshold2=threshold2)
        self.img.setImage(image)

    def create_canny(self, threshold1=80, threshold2=160):
        return cv2.Canny(self.image, threshold1=threshold1, threshold2=threshold2)
    
    def updateRoiType(self, roiType="Line ROI"):
        # if self.roiAny is not None:
        #     self.p1.removeItem(self.roiAny)
        if roiType == "Line ROI":
            self.roiAny = MyLineROI([200, 100], [250, 150], width=5)
        elif roiType == "Rect ROI":
            self.roiAny = MyRectROI([300, 300], [100, 100])
        elif roiType == "Ellipse ROI":
            self.roiAny = MyEllipseROI([300, 300], [100, 50])
        elif roiType == "Circle ROI":
            self.roiAny = MyCircleROI([300, 300], 50)
        elif roiType == "PolyLine ROI":
            self.roiAny = MyPolyLineROI([[200,200],[300,200],[350,400],[400,400]], closed=True)
        elif roiType == "Polygon ROI":
            self.roiAny = MyPolygonROI([[200, 200], [250, 200], [275, 250]], closed=True)
        

    def create_anno(self):
        if self.roiAny is None:
            self.updateRoiType()
        self.p1.addItem(self.roiAny)
        self.roiAny.setZValue(10)  # make sure ROI is drawn above image

    

    
"""
The cw page.
It is a ImageAnalysis tool.
"""
import os
from pathlib import Path
import cv2
import xml.etree.cElementTree as ET
from PIL import Image
import numpy as np
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMenu, QAction, QFileDialog, QGraphicsRectItem
from PySide2.QtGui import QCursor,QPixmap, QImage, QPen, QColor
from PySide2.QtCore import Qt, QRectF, QPoint
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from HaiGF import HPage, HGF
from HaiGF.gui_framework.widgets.central_widgets.tab_widget import HTabWidget
from HaiGF.plugins.label_train.my_ROI import MyPolyLineROI, MyRectROI, MyCircleROI, MyEllipseROI, MyLineROI, CurvePlogan
from HaiGF.plugins.label_train.scripts.aa import ImageProcessor
from HaiGF.plugins.label_train.widgets.cw_page2 import ImageMagnificationPage
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
        self.win.keyPressEvent = self.keyPressEvent
        self.win.keyReleaseEvent = self.keyReleaseEvent
        self.win.resize(800, 800)
    
        self.layout.addWidget(self.win)
        self.p1 = self.win.addPlot(title="")
        self.p1.getViewBox().invertY(True)
        self.p1.setMenuEnabled(False)
        
        # Item for displaying image data
        self.img = pg.ImageItem()
        self.img.hoverEvent = self.imageHoverEvent
        self.img.mousePressEvent = self.mousePressEvent
        self.img.mouseMoveEvent = self.mouseMoveEvent
        self.img.mouseReleaseEvent = self.mouseReleaseEvent
    
        self.p1.addItem(self.img)

        self.win.show()
        self.roi2 = None
        self.shapes = []

        self.item = -1
        self.create_menu1()
        self.create_menu2()

        self.data = None

        self.label_type = 'xml'

        #sam request json parameter
        self.sam_enabled = False 
        self.prompt_mode = 0
        #v1, len of point 1, label 0
        self.input_points = []
        self.input_labels = []
        self.input_boxes = []
        
    def analysis_ROI(self):
        if hasattr(self, 'p2'):
            print('ROI already here')
            return
        # Another plot area for displaying ROI data
        # self.win.nextRow()
        # self.p2 = self.win.addPlot(colspan=2)
        # self.p2.setMaximumHeight(250)
        # self.p2.setMenuEnabled(False)

        self.create_ROI()
        # self.updatePlot()

    def analysis_iso(self):
        """create isocurve and hist"""
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
        """cancel isocurve and hist"""
        if not hasattr(self, 'hist'):
            print('No iso here')
            return
        self.iso.setData(None)
        self.win.removeItem(self.hist)
        del self.hist

    def fix_coordinate(self, pos):
        x, y = pos.x(), pos.y()
        if x < 0:
            x = 0
        if x > self.image.shape[1]:
            x = self.image.shape[1]
        if y < 0:
            y = 0
        if y > self.image.shape[0]:
            y = self.image.shape[0]
        return QPoint(int(x), int(y))
    
    def get_Rect(self, p1, p2):
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        if x1 < x2:
            x = x1
            width = x2 - x1
        else:
            x = x2
            width = x1 - x2
        if y1 < y2:
            y = y1
            height = y2 - y1
        else:
            y = y2
            height = y1 - y2
        return QRectF(x, y, width, height)
    
    def mousePressEvent(self, event):
        """mouse press event"""
        self.item = -1
        if self.sam_enabled:
            click_point = self.img.mapToParent(event.pos())
            if event.button() == Qt.LeftButton:
                if self.prompt_mode == 1:#point
                    #将点击的坐标加入到self.input_points中
                    self.input_points.append([int(click_point.x()), int(click_point.y())])
                    self.input_labels.append(1)
                    self.plot_point(click_point.x(), click_point.y(), 1)
                elif self.prompt_mode == 2:#box
                    self.start_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
                    self.rect_item = QGraphicsRectItem(self.get_Rect(self.start_point, self.start_point))
                    self.rect_item.setPen(QPen(QColor(0, 255, 0), 0.1))
                    self.p1.addItem(self.rect_item)
                    self.rect_item.setZValue(10)
                    
            #中键点击，背景点
            elif self.prompt_mode == 1 and event.button() == Qt.MiddleButton:
                self.input_points.append([int(click_point.x()), int(click_point.y())])
                self.input_labels.append(0)
                self.plot_point(click_point.x(), click_point.y(), 0)
        else:
            if event.button() == Qt.RightButton:
                #转为QPoint对象
                point = QPoint(event.pos().x(), event.pos().y())
                items = self.win.scene().items(point)
                for shape in self.shapes:
                    if shape in items:
                        self.item = self.shapes.index(shape)
                        return
            
        
    def plot_point(self, x, y, label):
        """plot point"""
        if label == 1:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        self.p1.plot([x], [y], pen=None, symbol='o', symbolSize=5, symbolBrush=color)
                    
    def mouseReleaseEvent(self, event):
        if self.sam_enabled:
            if self.prompt_mode == 2 and event.button() == Qt.LeftButton:
                self.end_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
                self.rect_item.setRect(self.get_Rect(self.start_point, self.end_point))
                x, y, w, h = self.rect_item.rect().x(), self.rect_item.rect().y(), self.rect_item.rect().width(), self.rect_item.rect().height()
                self.input_boxes.append([x, y, w + x, h + y])
             
    def mouseMoveEvent(self, event):
        if self.sam_enabled and self.prompt_mode == 2 and event.buttons() == Qt.LeftButton:
            self.end_point = self.img.mapToParent(self.fix_coordinate(event.pos()))
            self.rect_item.setRect(self.get_Rect(self.start_point, self.end_point))
            
    
    def create_menu1(self):
        self.menu1 = QMenu(self)
        remove_anno = QAction(u'删除框',self.menu1)
        remove_anno.triggered.connect(self.delete_roiAnno)
        self.menu1.addAction(remove_anno)

    def create_menu2(self):
        #菜单对象
        self.layout_menu = QMenu(self)
        actionA = QAction(u'保存标注 & roi',self.layout_menu)#创建菜单选项对象
        self.layout_menu.addAction(actionA)#把动作A选项对象添加到菜单self.win_menu上
        actionB = QAction(u'保存标注 & canny',self.layout_menu)
        self.layout_menu.addAction(actionB)
        actionC = QAction(u'保存蒙版',self.layout_menu)
        self.layout_menu.addAction(actionC)
        actionA.triggered.connect(self.save_all_roiAnno) #将动作A触发时连接到槽函数 button
        actionB.triggered.connect(self.save_all_annotation)
        actionC.triggered.connect(self.save_all_mask)
        self.layout_menu.actionA = actionA
        self.layout_menu.actionB = actionB
        self.layout_menu.actionC = actionC

    def create_rightmenu(self):
        """create rightmenu on layout"""
        #得到鼠标右键点击的位置的项目类型
        if self.item == -1:
            self.layout_menu.popup(QCursor.pos())
        else: 
            self.menu1.popup(QCursor.pos())#声明当鼠标在win控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    def delete_roiAnno(self):
        """delete roi and annotation"""
        item = self.shapes[self.item]
        self.p1.removeItem(item)
        self.shapes.remove(item)

    def cancel_canny(self):
        """cancel canny"""
        self.img.setImage(self.image)

    def save_all_annotation(self):
        """save all annotion on a image in canny"""
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
        print(filepath, type)
        t = ''
    
        for i in result:
            for e in range(len(result[0])):
                t = t+str(i[e])+' '
            file.write(t.strip(' '))
            file.write('\n')
            t = ''

    #将ROI区域作为蒙版标注保存
    def save_all_mask(self):
        assert len(self.shapes) > 0, 'No ROI region is selected.'
        # 获取图像的像素值矩阵
        img = self.image

        # 创建与图像大小相同的背景图像
        mask = np.zeros_like(img[:, :, 0], dtype=np.uint8)
        # 遍历所有的ROI区域，将每个ROI区域的顶点坐标保存到列表中
        pts_list = []
        for roi in self.shapes:
            #取得大小和位置，做为蒙版的大小和位置
            w = int(roi.size().x())
            h = int(roi.size().y())
            x = int(roi.pos().x())
            #y为图片的高度减去roi的y坐标
            y = int(img.shape[0] - roi.pos().y())
            print(x, y, w, h)
            mask[y - h : y, x:x+w] = 255
            


        

        # 将掩码图像转换为二值图像
        _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)

        # 将掩码图像保存到磁盘
        cv2.imwrite("D:/bubbleImage/image/mask.png", mask)
           
    
    def save_all_roiAnno(self):
        #保存每个roi的信息
        if len(self.shapes) == 0:
            print('no roi')
            return
        pass
        """使用切片操作提取出ROI区域;
        我们使用Python内置的XML模块来创建XML文件,并将ROI区域的坐标信息保存到XML文件中;
        创建一个根节点annotation,并在其中添加一个子节点size来保存图片的大小信息,以及一个子节点object来保存ROI区域的信息;
        object节点中包含一个子节点name来表示ROI区域的名称,以及一个子节点bndbox来保存ROI区域的边界框信息;
        bndbox节点中包含四个子节点xmin、ymin、xmax、ymax,分别表示ROI区域的左上角和右下角坐标最后;
        使用ElementTree将XML文件保存到磁盘中。"""
        
        for roi in self.shapes:
            # 提取ROI区域
            roi = self.img.getArrayRegion(self.image, roi)
            # 保存ROI区域的坐标信息到XML文件中
            root = ET.Element('annotation')
            size = ET.SubElement(root, 'size')
            width = ET.SubElement(size, 'width')
            height = ET.SubElement(size, 'height')
            depth = ET.SubElement(size, 'depth')
            width.text = str(self.image.shape[1])
            height.text = str(self.image.shape[0])
            depth.text = str(self.image.shape[2])
            object = ET.SubElement(root, 'object')
            name = ET.SubElement(object, 'name')
            name.text = 'ROI'
            bndbox = ET.SubElement(object, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            ymin = ET.SubElement(bndbox, 'ymin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymax = ET.SubElement(bndbox, 'ymax')
            xmin.text = str(roi.shape[0])
            ymin.text = str(roi.shape[1])
            xmax.text = str(roi.shape[2])
            ymax.text = str(roi.shape[3])
            tree = ET.ElementTree(root)
            tree.write('test.xml')
         
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
            data = Image.open(img_path)
        self.img_path = img_path
        # self.image = np.flipud(data)
        self.image = np.array(data)
        # self.scripts()
        self.img.setImage(self.image)
        self.update_manification()


    def create_ROI(self):
        """create a ROI"""
        if hasattr(self, 'roi'):
            return
        self.roi = pg.ROI([200, 400], [100, 50])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.p1.addItem(self.roi)
        self.roi.setZValue(10)  # make sure ROI is drawn above image
        # self.roi.sigRegionChanged.connect(self.updatePlot)
        self.roi.sigRegionChanged.connect(self.update_manification)
        
    def plot_box(self):
        """plot the box of ROI"""
        self.box = pg.RectROI([200, 400], [100, 50], pen=(0, 9))
        self.p1.addItem(self.box)
        self.box.setZValue(10)

    def local_magnification(self):
        """make a local magnification of the ROI area in a new tab"""
        if hasattr(self, 'page2'):
            return
        # 创建一个新的tab控件
        mw = self.p
        self.newTab = HTabWidget(mw.cw)
        self.newTab.setObjectName('newTab')
        self.newTab.tabCloseRequested.connect(self.close_tab)
        mw.cw.addTabWidget(self.newTab)
        #设置self.newTab的初始宽度为500，后续可调节
        self.newTab.setMinimumWidth(self.img.width() / 2)

        
        self.page2 = self.create_page2()
        self.newTab.addPage(self.page2)
        
        self.update_manification()

    def close_tab(self):
        """close the tab"""
        mw = self.p
        mw.cw.remove_tabw(self.newTab)
        del self.newTab
        del self.page2
        
    def update_manification(self, process=False):
        """update the image in the new tab"""
        if not hasattr(self, 'page2'):
            return
        img_manification = [self.image.shape[1], self.image.shape[0], self.roi.pos().x(), self.roi.pos().y()]
        if process:
            selected = self.roi.getArrayRegion(self.data, self.img)
        else:
            selected = self.roi.getArrayRegion(self.image, self.img)
        self.page2.show_image(selected, img_manification, self.img_path, self.label_type)

    def create_page2(self):
        """create a new page for local magnification"""
        page = ImageMagnificationPage(self.p)
        return page

    def cancel_ROI(self):
        """cancel the ROI"""
        if not hasattr(self, 'roi'):
            print('No ROI here')
            return
        self.p1.removeItem(self.roi)
        # self.roi = None
        # self.win.removeItem(self.p2)
        del self.roi
        
    # Callbacks for handling user interaction
    def updatePlot(self):
        """update the plot in the right side"""
        selected = self.roi.getArrayRegion(self.image, self.img)
        d2 = selected.mean(axis=0)
        """3d data, but 1d data asked"""
        self.p2.plot(d2.mean(axis=1), clear=True)

    def create_isocurve(self):
        """create a isocurve"""
        # Isocurve drawing
        self.iso = pg.IsocurveItem(level=65, pen='g')
        self.iso.setParentItem(self.img)
        self.iso.setZValue(5)
           
    def updateIsocurve(self):
        """update the isocurve"""
        self.iso.setLevel(self.isoLine.value())
    
    def create_isoLine(self):
        """create a isoLine"""
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
        val = self.image[i, j]
        ppos = self.img.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.p1.setTitle("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %s" % (x, y, i, j, val))
       
    def canny(self, threshold1=80, threshold2=160):
        """create a canny edge"""
        image = self.create_canny(threshold1=threshold1, threshold2=threshold2)
        self.img.setImage(image)

    def create_canny(self, threshold1=80, threshold2=160):
        """create a canny edge"""
        return cv2.Canny(self.image, threshold1=threshold1, threshold2=threshold2)
    
    def updateRoiType(self, roiType="Line ROI"):
        # if self.roiAny is not None:
        #     self.p1.removeItem(self.roiAny)
        if roiType == "Line ROI":
            roiAny = MyLineROI([200, 100], [250, 150], width=5)
        elif roiType == "Rect ROI":
            roiAny = MyRectROI([300, 300], [100, 100])
        elif roiType == "Ellipse ROI":
            roiAny = MyEllipseROI([300, 300], [100, 50])
        elif roiType == "Circle ROI":
            roiAny = MyCircleROI([300, 300], 50)
        elif roiType == "PolyLine ROI":
            roiAny = MyPolyLineROI([[200,200],[300,200],[350,400],[400,400]], closed=True)
        elif roiType == "BezierLine ROI":
            # roiAny = BezierLineROI([[200,200],[300,300],[350,400]], closed=True)
            # roiAny = BezierROI(points=[[200,200],[300,200],[350,400]])
            point1 = QPoint(200, 200)
            point2 = QPoint(300, 80)
            point3 = QPoint(500, 300)
            
            roiAny = CurvePlogan(points=[point1, point2, point3], img_shape=self.image.shape)

        return roiAny

    def create_anno(self, shape):
        """create a annotation ROI"""
        roiAny = self.updateRoiType(shape)
        self.shapes.append(roiAny)
        self.p1.addItem(roiAny)
        roiAny.setZValue(self.p1.scene().items()[::-1][0].zValue() + 1)  # make sure ROI is drawn above image
 
    def mouseDoubleClickEvent(self, event):
        """double click to transfer ROI to a new tab for local magnification"""
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'roi'):
                self.local_magnification()
            else:
                print('No ROI here')
                return
        else:
            super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        """press ctrl to show the processed image"""
        if(event.key() == Qt.Key_Control):
            self.img.setImage(self.data)
            self.update_manification(True)
        elif event.key() == Qt.Key_A:
            self.adjust_bezier()

    def adjust_bezier(self):
        for shape in self.shapes:
            if isinstance(shape, CurvePlogan):
                shape.adjustShape()

    def scripts(self):
        processor = ImageProcessor()
        image = processor(self.image)
        self.data = image
       
    def keyReleaseEvent(self, event):
        """release ctrl to show the original image"""
        if(event.key() == Qt.Key_Control):
            self.img.setImage(self.image)
            self.update_manification(False)

    def predict_sam(self):
        from ..scripts.sam_predictor import prompt_segment, auto_segment
        if self.prompt_mode == 0:
            mask = auto_segment(self.img_path)
        else:
            print(self.input_points)
            print(self.input_labels)
            print(self.input_boxes)  
            mask = prompt_segment(self.input_points, self.input_labels, self.input_boxes, self.img_path)
        
        """show the mask"""

    def draw_bbox(self, bbox):
        # rect = pg.RectROI([bbox[0], bbox[1]], [bbox[2] - bbox[0], bbox[3] - bbox[1]], pen=(0, 9))
        rect = QGraphicsRectItem(QRectF(bbox[0], bbox[1], bbox[2], bbox[3]))
        self.p1.addItem(rect)
        rect.setZValue(10)


        


    
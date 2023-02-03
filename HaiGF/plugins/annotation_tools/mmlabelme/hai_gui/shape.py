import copy
import math

# from qtpy import QtCore
# from qtpy import QtGui
from PySide2 import QtWidgets, QtGui, QtCore

import hai_gui.utils


# TODO(unknown):
# - [opt] Store paths instead of creating new ones at each paint.


DEFAULT_LINE_COLOR = QtGui.QColor(0, 255, 0, 128)  # bf hovering
DEFAULT_FILL_COLOR = QtGui.QColor(0, 255, 0, 128)  # hovering
DEFAULT_SELECT_LINE_COLOR = QtGui.QColor(255, 255, 255)  # selected
DEFAULT_SELECT_FILL_COLOR = QtGui.QColor(0, 255, 0, 155)  # selected
DEFAULT_VERTEX_FILL_COLOR = QtGui.QColor(0, 255, 0, 255)  # hovering
DEFAULT_HVERTEX_FILL_COLOR = QtGui.QColor(255, 255, 255, 255)  # hovering


class Shape(object):  # 形状对象

    # Render handles as squares
    P_SQUARE = 0

    # Render handles as circles
    P_ROUND = 1

    # Flag for the handles we would move if dragging
    MOVE_VERTEX = 0

    # Flag for all other handles on the current shape
    NEAR_VERTEX = 1

    # The following class variables influence the drawing of all shape objects.
    line_color = DEFAULT_LINE_COLOR  # 线颜色
    fill_color = DEFAULT_FILL_COLOR  # 填充颜色
    select_line_color = DEFAULT_SELECT_LINE_COLOR  # 选择线颜色
    select_fill_color = DEFAULT_SELECT_FILL_COLOR  # 选择填充颜色
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR  # 顶点填充颜色
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR  # h顶点颜色是什么？
    point_type = P_ROUND  # 顶点类型，默认的圆点
    point_size = 8  # 顶点尺寸
    scale = 1.0  # 缩放因子

    def __init__(
        self,
        modal=None,
        label=None,
        line_color=None,
        shape_type=None,  # str, rectangle, polygon et.al
        flags=None,
        group_id=None,
        tid=None,
        status=None,
        status_group_id=None
    ):
        self.modal = modal
        self.label = label
        self.group_id = group_id
        self.tid = tid
        self.status = status
        self.status_group_id = status_group_id
        self.points = []
        self.fill = False
        self.selected = False
        self.shape_type = shape_type
        self.flags = flags
        self.other_data = {}

        self._highlightIndex = None  # 高亮索引，高亮点的索引
        self._highlightMode = self.NEAR_VERTEX  # int, 1
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),  # 1: (4, 1)
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),  # 0: (1.5, 0)
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

        self.shape_type = shape_type

    @property
    def shape_type(self):
        return self._shape_type  # 私有成员

    @shape_type.setter
    def shape_type(self, value):
        if value is None:
            value = "polygon"
        if value not in [
            "polygon",
            "rectangle",
            "point",
            "line",
            "circle",
            "linestrip",
            "magic_wand",
        ]:
            raise ValueError("Unexpected shape_type: {}".format(value))
        self._shape_type = value

    def close(self):
        self._closed = True

    def addPoint(self, point):
        """添加点，如果新点和已保存的第一个点相同，保护变量_closed设置为True，即完成绘制, 否则添加该点"""
        if self.points and point == self.points[0]:
            self.close()
        else:
            self.points.append(point)

    def canAddPoint(self):
        """形状类型是多边形和linestrip时，能添加点"""
        return self.shape_type in ["polygon", "linestrip"]

    def popPoint(self):
        """删除最后一个点，并返回，如果没有点可以删除，返回None"""
        if self.points:
            return self.points.pop()
        return None

    def insertPoint(self, i, point):
        """插入点"""
        self.points.insert(i, point)

    def removePoint(self, i):
        """根据索引移除点"""
        self.points.pop(i)

    def isClosed(self):
        """返回是否关闭"""
        return self._closed

    def setOpen(self):
        """设置_closed是False"""
        self._closed = False

    def getRectFromLine(self, pt1, pt2):
        """根据线段的两个端点获取到矩形，返回4个点的矩形，是x1y1wh"""
        x1, y1 = pt1.x(), pt1.y()
        x2, y2 = pt2.x(), pt2.y()
        return QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)

    def paint(self, painter):
        """绘制。"""
        if self.points:
            color = (
                self.select_line_color if self.selected else self.line_color
            )
            pen = QtGui.QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QtGui.QPainterPath()
            vrtx_path = QtGui.QPainterPath()

            if self.shape_type == "rectangle":
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getRectFromLine(*self.points)
                    line_path.addRect(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "circle":
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getCircleRectFromLine(self.points)
                    line_path.addEllipse(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "linestrip":
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
            else:
                line_path.moveTo(self.points[0])
                # Uncommenting the following line will draw 2 paths
                # for the 1st vertex, and make it non-filled, which
                # may be desirable.
                # self.drawVertex(vrtx_path, 0)

                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
                if self.isClosed():
                    line_path.lineTo(self.points[0])

            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.fillPath(vrtx_path, self._vertex_fill_color)
            if self.fill:
                color = (
                    self.select_fill_color
                    if self.selected
                    else self.fill_color
                )
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):
        """画顶点"""
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self._vertex_fill_color = self.hvertex_fill_color
        else:
            self._vertex_fill_color = self.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        """最近顶点"""
        min_distance = float("inf")
        min_i = None
        for i, p in enumerate(self.points):
            dist = hai_gui.utils.distance(p - point)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                min_i = i
        return min_i

    def nearestEdge(self, point, epsilon):
        min_distance = float("inf")
        post_i = None
        for i in range(len(self.points)):
            line = [self.points[i - 1], self.points[i]]
            dist = hai_gui.utils.distancetoline(point, line)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                post_i = i
        return post_i

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def getCircleRectFromLine(self, line):
        """Computes parameters to draw with `QPainterPath::addEllipse`"""
        if len(line) != 2:
            return None
        (c, point) = line
        r = line[0] - line[1]
        d = math.sqrt(math.pow(r.x(), 2) + math.pow(r.y(), 2))
        rectangle = QtCore.QRectF(c.x() - d, c.y() - d, 2 * d, 2 * d)
        return rectangle

    def makePath(self):
        """返回QtGui.QPainterPath"""
        if self.shape_type == "rectangle":
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getRectFromLine(*self.points)
                path.addRect(rectangle)
        elif self.shape_type == "circle":
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getCircleRectFromLine(self.points)
                path.addEllipse(rectangle)
        else:
            path = QtGui.QPainterPath(self.points[0])
            for p in self.points[1:]:
                path.lineTo(p)
        return path

    def boundingRect(self):
        """图形形状的绑定矩形"""
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        """所有点移动"""
        self.points = [p + offset for p in self.points]

    def moveVertexBy(self, i, offset):
        """第i个点移动"""
        self.points[i] = self.points[i] + offset

    def highlightVertex(self, i, action):
        """Highlight a vertex appropriately based on the current action
        高亮一个顶点
        Args:
            i (int): The vertex index
            action (int): The action
            (see Shape.NEAR_VERTEX and Shape.MOVE_VERTEX)
        """
        self._highlightIndex = i
        self._highlightMode = action  # 0, 1

    def highlightClear(self):
        """Clear the highlighted point, 清除高亮"""
        self._highlightIndex = None

    def copy(self):  # 拷贝自己并返回
        return copy.deepcopy(self)

    def __len__(self):  # 拥有的点的长度
        return len(self.points)

    def __getitem__(self, key):  # 返回第i个点
        return self.points[key]

    def __setitem__(self, key, value):  # 设置第i个点
        self.points[key] = value

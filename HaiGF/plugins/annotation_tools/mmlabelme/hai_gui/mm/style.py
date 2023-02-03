
# from qtpy import QtWidgets
# from qtpy import QtCore
# from qtpy import QtGui

from PySide2 import QtCore, QtWidgets, QtGui

class SchemePS:
    bg_color: str = '#EE3B3B'
    tool_bg_color: str = '#C0C0C0'
    bg_colors = ['#444444', '#444444', '#555555', '#444444', '#333333',
             '#555555', '#555555', '#555555', '#555555', '#555555', '#CCCCCC']


class SchemeRainbow:
    # 顺序：主窗口，菜单栏，工具栏，状态栏，m4画布，m5 m6 m7 m8 m9
    # 红色，蓝色，黄色(橙色)，绿色， 紫色，浅黄色
    bg_colors = ["#EE3B3B", "#3366FF", "#FF9933", "#33FF00", "#CC99CC",
                 "#FFFF00", "#CCFF99", '#CCFFFF', '#FFCCCC', '#000000', '#C0C0C0']



    tool_bg_color: str = '#CCFF99'  # 浅绿
    sa_bg_color: str = '#CCFFFF'  # 浅蓝
    status_bg_color: str = '#FFCCCC'  # 浅红


class Style(object):
    def __init__(self):
        pass

    def set_scheme(self, mw, scheme):
        if scheme == 'photoshop':
            scheme = SchemePS
        elif scheme == 'rainbow':
            scheme = SchemeRainbow
        else:
            raise NotImplementedError(f'scheme not implemented: {scheme}')
        widgets = [mw, mw.menuBar(), mw.tools, mw.statusBar(), mw.scrollArea, mw.flag_dock,
                   mw.label_dock, mw.shape_dock, mw.file_dock, mw.mm_dock]
        for i, widg in enumerate(widgets):
            # print(i, len(scheme.bg_colors))
            self.qss(widg, background_color=scheme.bg_colors[i])

    def qss(self, widget, *args, **kwargs):
        # print(kwargs)
        self.set_style_sheet(widget, *args, **kwargs)

    def set_style_sheet(self, widget, *args, **kwargs):
        # print(kwargs)

        bg_color = kwargs.pop('background_color', '#CCCCCC')
        border_r = kwargs.pop('border_radius', '2px')

        # print(bg_color)

        qss = f'background-color: {bg_color}; ' \
              f'border-radius: {border_r};' \
              f'color: #FFFFFF;' \
              # f'border: 0.8px solid #111111'
        widget.setStyleSheet(qss)

    def hide_title(self, widget):
        widget.setTitleBarWidget(QtWidgets.QWidget())
        widget.titleBarWidget().hide()

    def frameless(self, mw):
        mw.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        # widget.setWindowFlags(Qt.WindowSystemMenuHint)




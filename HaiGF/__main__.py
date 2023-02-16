
import sys, os
from pathlib import Path
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTranslator
from PySide2.QtGui import QFontDatabase
here = Path(__file__).parent


from .apis import HMainWindow
# from .plugins import AppMainWindow
from .apis import __version__, __appname__




def run(name='framework'):
    translator = QTranslator()
    translator.load(f"{here}/gui_framework/translate/translate_zh_CN.qm")
    
    app = QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.installTranslator(translator)

    font_path = f'{here}/gui_framework/translate/fonts/HarmonyOS_Sans_SC_Regular.ttf'
    id = QFontDatabase.addApplicationFont(font_path)
    # QFontDatabase.systemFont(QFontDatabase.GeneralFont)
    # xx = QFontDatabase.applicationFontFamilies(id)
    # print(xx)
    # font_str = QFontDatabase.applicationFontFamilies(id)[0]

    mw = HMainWindow()

    # from .plugins.hai_tools import AIPlugin
    # mw.install_plugin(AIPlugin)

    from .plugins.load_img import LoadImagePlugin
    mw.install_plugin(LoadImagePlugin)

    from .plugins.annotation_tools import AnnoPlugin
    mw.install_plugin(AnnoPlugin)

    from .plugins.pyqtgraph import PyqtGraphPlugin
    mw.install_plugin(PyqtGraphPlugin)

    from .plugins.label_train import AntrainPlugin
    mw.install_plugin(AntrainPlugin)

    mw.show()
    mw.raise_()
    sys.exit(app.exec_())


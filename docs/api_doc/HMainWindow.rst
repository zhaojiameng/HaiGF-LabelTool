HMainWindow
==================

.. automodule:: HaiGF.HMainWindow

Usage:

.. code-block:: python
    
    import sys
    from PySide2.QtWidgets import QApplication
    from HaiGF import HMainWindow
    
    app = QApplication(sys.argv)
    mw = HMainWindow()
    mw.show()
    mw.raise_()
    sys.exit(app.exec_())


.. .. automethod:: HaiGF.HMainWindow.__init__

.. automethod:: HaiGF.apis.mw.install_plugin



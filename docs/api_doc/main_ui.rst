Main UI
========


Main Window
------------

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

Core Func Bar
-----------------

.. automodule:: HaiGF.apis.cfb

.. automethod:: HaiGF.apis.cfb.add_action
.. automethod:: HaiGF.apis.cfb.insert_action
.. automethod:: HaiGF.apis.cfb.mousePressEvent


Main Side Bar
-------------

.. automodule:: HaiGF.apis.msb

.. automethod:: HaiGF.apis.msb.add_widget


Central Widget
--------------

.. automodule:: HaiGF.apis.cw

.. .. property:: cw.tab_widgets

.. automethod:: HaiGF.apis.cw.addTabWidget

    Example:

    .. code-block:: python

        from HaiGF import HTabWidget
        from HaiGF import HPage

        tab_widget = HTabWidget(parent=cw)  # create a tab widget
        page = HPage(parent=cw, 
                    title='page_title', 
                    icon='icon_name')  # create a page
        tab_widget.addPage(page)  # add a page into tab widget
        cw.addTabWidget(tab_widget)  # add a tab widget into central widget

.. automethod:: HaiGF.apis.cw.addPage

    Example:

    .. code-block:: python

        from HaiGF import HPage

        page = HPage(parent=cw, 
                    title='page_title', 
                    icon='icon_name')  # create a page
        cw.addPage(page)  # add a page into current tab widget on central widget

.. automethod:: HaiGF.apis.cw.current_tab_widget

.. automethod:: HaiGF.apis.cw.create_tab_widget_by_source_tabw

.. automethod:: HaiGF.apis.cw.get_current_splitter_by_tab_widget

.. automethod:: HaiGF.apis.cw.judge_need_delete_source_tabw

.. automethod:: HaiGF.apis.cw.judge_need_create_new_splitter

.. automethod:: HaiGF.apis.cw.split_screen

.. automethod:: HaiGF.apis.cw.sort_new_tabw_vs_ttabw

.. automethod:: HaiGF.apis.cw.move_one_tab_to_another_tabw

.. automethod:: HaiGF.apis.cw.closeEvent

.. automethod:: HaiGF.apis.cw.mousePressEvent

.. automethod:: HaiGF.apis.cw.mouseMoveEvent

.. automethod:: HaiGF.apis.cw.moving_tab

.. automethod:: HaiGF.apis.cw.moved_tab

.. automethod:: HaiGF.apis.cw.clear_splitters


HWidgets
---------
.. toctree::
    :maxdepth: 1
    :caption: Contents:
    
    hwidgets
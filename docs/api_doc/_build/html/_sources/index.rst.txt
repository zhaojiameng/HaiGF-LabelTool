.. HAI GUI Framework documentation master file, created by
   sphinx-quickstart on Sat Jan 14 11:48:46 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HaiGF - Hep AI Gui Framework
===================================================================

**HaiGF** (High energy physics Artificial Intelligence Graphical user interface Framework) is a framework for building graphical user interfaces 
based on HAI algorithm library for high energy physics analysis. It is based on the `PyQt5` library and the `Qt5` framework.

Interface
---------------

.. image:: https://zhangzhengde0225.github.io/images/blog/hai_gui_framework_1280.gif


Feautures
---------

+ Modular design, easy to extend, easy to use.
+ The GUI front and AI algorithm backend are completely separated based on the `HAI` library so that the application will be very lightweight.

.. note: This is a work in progress.  The documentation is not complete and
   may contain errors.  Please report any errors or omissions to the
   `HAI GUI Framework`_ project.


.. toctree::
   :maxdepth: 2
   :caption: Getting started

   HaiGF_getting_started.md


.. toctree::
   :maxdepth: 2
   :caption: API
   
   HMainWindow
   mw.CoreFuncBar
   mw.MainSideBar
   mw.CentralWidget
   HPlugin
   HPage
   HGF
   


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

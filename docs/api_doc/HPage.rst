HPage
------

.. autoclass:: HaiGF.apis.HPage

    Example:

    .. code-block:: python

        from HaiGF import HPage
        
        class CustomerPage(HPage):
            def __init__(self, parent=None, **kwargs):
                super().__init__(parent, **kwargs)
                self.set_title(self.tr('Customer Page'))
                self.set_icon(<QIcon>)

                self.setup_ui()

            def setup_ui(self):
                # setup customer ui here (QWidget).
                pass
    

.. automethod:: HaiGF.apis.HPage.set_icon

.. automethod:: HaiGF.apis.HPage.set_title
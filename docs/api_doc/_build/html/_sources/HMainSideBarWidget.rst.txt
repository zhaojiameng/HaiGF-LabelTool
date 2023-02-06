HMainSideBarWidget
------------------

.. autoclass:: HaiGF.apis.HMainSideBarWidget


    Example:

    .. code-block:: python

        from HaiGF.apis import HMainSideBarWidget

        class CustomerMSBWidget(HMainSideBarWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.set_title('Customer MSB Widget Title')
                self.set_title_actions([
                    HAction(text='Cutomer action', parent=self),
                ])
                # other codes for defining the widget

        # add the widget to the main window
        msbw = CustomerMSBWidget()
        action = HAction(text='CFB action', parent=mw)
        msb.add_widget(msbw, action)  # note the msb is the main side bar object


.. automethod:: HaiGF.apis.HMainSideBarWidget.set_title

.. automethod:: HaiGF.apis.HMainSideBarWidget.set_title_actions



.. .. automethod:: HaiGF.apis.HMainSideBarWidget.HMainSideBarWidget


import param
import panel as pn

class PanelBase(param.Parameterized):
    """base class for mixin panels"""

    position = ''

    @property
    def panel(self):
        return None


class FigurePanel(PanelBase):
    """"base class for figures"""

    _controlled_by = []  # list of panel controllers

    def __init__(self, parent, controllers, **params):
        self.parent = parent  #main controller
        self.controllers = controllers  #side controllers
        super(FigurePanel, self).__init__(**params)


    def _update(self):
        """redraw the graph"""
        self.bk_pane.param.trigger('object')

    @property
    def panel(self):
        return self.bk_pane


class ControlPanel(PanelBase):
    """base class for left control pannels"""

    def __init__(self, parent, **params):
        self.parent = parent
        super(ControlPanel, self).__init__(**params)

    @property
    def panel(self):
        return pn.panel(self.param)

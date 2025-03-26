from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class PyPushButton(QPushButton):

    def __init__(
            self,
            text="",
            radius=8,
            color="#fff",
            bg_color="#323842",
            bg_color_hover="#4D78CC",
            bg_color_pressed="#E06253",
            parent=None,
            width=None,
            height=None,
            expanding=False,
            do_drops=False,
            is_compare=False
    ):
        super().__init__()
        self.url = ""
        self.is_compare = is_compare
        self.original_text = text
        self.style = '''
        QPushButton {{
        	border: 2px solid transparent;
            color: {_color};
        	border-radius: {_radius}px;
        	background-color: #323842;
        }}
        QPushButton:hover {{
        	background-color: {_bg_color_hover};
        }}
        QPushButton:pressed {{	
        	background-color: {_bg_color_pressed};
        }}
        '''
        self.setAcceptDrops(do_drops)
        # SET PARAMETRES
        self.setText(text)
        if parent != None:
            self.setParent(parent)
        if expanding:
            size_policy = self.sizePolicy()
            size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
            self.setSizePolicy(size_policy)
            self.setAutoFillBackground(True)

        self.setCursor(Qt.PointingHandCursor)

        self.custom_style = self.style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _bg_color_pressed=bg_color_pressed
        )
        self.setStyleSheet(self.custom_style)

        if width and height is not None:
            self.setFixedSize(width, height)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(PyPushButton, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(PyPushButton, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.url = str(event.mimeData().urls()[0].toLocalFile())
        else:
            super(PyPushButton, self).dropEvent(event)

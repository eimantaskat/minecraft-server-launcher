from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon, QCursor, QPalette
from PyQt5.QtCore import Qt


class ToolbarItem(QWidget):
    last_clicked = None

    def __init__(self, action, icon, text, is_last_clicked=False):
        super().__init__()
        active_icon = QIcon("assets/icon0.png")
        self.active_label = QLabel()
        self.active_label.setPixmap(active_icon.pixmap(16, 16))
        self.active_label.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0))
        self.icon_label = QLabel()
        self.icon_label.setPixmap(icon.pixmap(24, 24))
        self.text_label = QLabel(text)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.active_label)
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setContentsMargins(0, 10, 10, 10)
        self.setLayout(self.layout)
        self.setFixedWidth(150)
        self.action = action
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Dark)
        if is_last_clicked:
            self.mousePressEvent(None)


    def mousePressEvent(self, event):
        if ToolbarItem.last_clicked:
            ToolbarItem.last_clicked.text_label.setStyleSheet("")
            ToolbarItem.last_clicked.active_label.setGraphicsEffect(
                QGraphicsOpacityEffect(opacity=0))
            ToolbarItem.last_clicked.setCursor(QCursor(Qt.PointingHandCursor))
        self.text_label.setStyleSheet("font-weight: bold;")
        self.active_label.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
        ToolbarItem.last_clicked = self
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.action.trigger()


    def enterEvent(self, event):
        if ToolbarItem.last_clicked != self:
            self.setBackgroundRole(QPalette.Highlight)


    def leaveEvent(self, event):
        self.setBackgroundRole(QPalette.Dark)

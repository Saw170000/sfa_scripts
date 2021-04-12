import logging

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("ScatterTool")
        self.setMinimumWidth(425)
        self.setMinimumHeight(500)
        self.create_ui()

    def create_ui(self):
        title_lbl = QtWidgets.QLabel("Scatter Tool")
        title_lbl.setStyleSheet("font: bold 20px")
        scatter_lay = self._scatter_ui()
        destination_lay = self._destination_ui()
        displacement_lay = self._displacement_rotation_ui()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_lbl)
        main_lay.addLayout(scatter_lay)
        main_lay.addLayout(destination_lay)
        main_lay.addLayout(displacement_lay)
        main_lay.addStretch()
        self.setLayout(main_lay)

    def slider_setup(self):
        # self.layout = QtWidgets.QHBoxLayout()
        slider = QtWidgets.QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.valueChanged.connect(self.changed_value)
        return slider

    def changed_value(self):
        size_x = self.x_slide.value()
        size_y = self.y_slide.value()
        size_z = self.z_slide.value()
        self.x_value_le.setText(str(size_x))
        self.y_value_le.setText(str(size_y))
        self.z_value_le.setText(str(size_z))

    def _displacement_rotation_ui(self):
        self.rotation_lbl = QtWidgets.QLabel("Random Rotation Offset")
        self.x_lbl = QtWidgets.QLabel("X:")
        self.x_value_le = QtWidgets.QLineEdit()
        self.x_value_le.setFixedWidth(25)
        self.x_slide = self.slider_setup()
        self.y_lbl = QtWidgets.QLabel("Y:")
        self.y_value_le = QtWidgets.QLineEdit()
        self.y_value_le.setFixedWidth(25)
        self.y_slide = self.slider_setup()
        self.z_lbl = QtWidgets.QLabel("Z:")
        self.z_value_le = QtWidgets.QLineEdit()
        self.z_value_le.setFixedWidth(25)
        self.z_slide = self.slider_setup()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rotation_lbl)
        self.widgetLayout = self._displacement_rotation_widgets()
        layout.addLayout(self.widgetLayout)
        return layout

    def _displacement_rotation_widgets(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.x_lbl, 0, 0)
        layout.addWidget(self.x_value_le, 0, 1)
        layout.addWidget(self.x_slide, 0, 2)
        layout.addWidget(self.y_lbl, 1, 0)
        layout.addWidget(self.y_value_le, 1, 1)
        layout.addWidget(self.y_slide, 1, 2)
        layout.addWidget(self.z_lbl, 2, 0)
        layout.addWidget(self.z_value_le, 2, 1)
        layout.addWidget(self.z_slide, 2, 2)
        return layout

    def _scatter_ui(self):
        self.scatterObj_lbl = QtWidgets.QLabel("Object to scatter:")
        self.scatterObj_lbl.setFixedWidth(125)
        self.scatterObj_le = QtWidgets.QLineEdit()
        self.scatterObj_le.setFixedWidth(200)
        self.scatterObj_select_btn = QtWidgets.QPushButton("Selected")
        self.scatterObj_select_btn.setFixedWidth(50)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatterObj_lbl, 0, 0)
        layout.addWidget(self.scatterObj_le, 0, 1)
        layout.addWidget(self.scatterObj_select_btn, 0, 2)
        return layout

    def _destination_ui(self):
        self.destObj_lbl = QtWidgets.QLabel("Object to scatter onto:")
        self.destObj_lbl.setFixedWidth(125)
        self.destObj_le = QtWidgets.QLineEdit()
        self.destObj_le.setFixedWidth(200)
        self.destObj_select_btn = QtWidgets.QPushButton("Selected")
        self.destObj_select_btn.setFixedWidth(50)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.destObj_lbl, 0, 0)
        layout.addWidget(self.destObj_le, 0, 1)
        layout.addWidget(self.destObj_select_btn, 0, 2)
        return layout


ui = ScatterToolUI()
ui.show()

import logging
import random

random.seed(1)

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
        self.setMinimumHeight(350)
        self.create_ui()
        self.connection()

    def create_ui(self):
        title_lbl = QtWidgets.QLabel("Scatter Tool")
        title_lbl.setStyleSheet("font: bold 20px")
        scatter_lay = self._scatter_ui()
        destination_lay = self._destination_ui()
        displace_rotate_lay = self._displacement_rotation_ui()
        displace_scale_lay = self._displacement_scale_ui()
        apply_cancel_lay = self.button_setup()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_lbl)
        main_lay.addSpacing(20)
        main_lay.addLayout(scatter_lay)
        main_lay.addLayout(destination_lay)
        main_lay.addSpacing(20)
        main_lay.addLayout(displace_rotate_lay)
        main_lay.addSpacing(20)
        main_lay.addLayout(displace_scale_lay)
        main_lay.addLayout(apply_cancel_lay)
        main_lay.addStretch()
        self.setLayout(main_lay)

    def button_setup(self):
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def slider_setup(self):
        slider = QtWidgets.QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(360)
        slider.valueChanged.connect(self.changed_value)
        return slider

    def changed_value(self):
        # rotation sliders
        size_rotate_x = self.x_rotate_slide.value()
        size_rotate_y = self.y_rotate_slide.value()
        size_rotate_z = self.z_rotate_slide.value()
        self.x_rotate_value_le.setText(str(size_rotate_x))
        self.y_rotate_value_le.setText(str(size_rotate_y))
        self.z_rotate_value_le.setText(str(size_rotate_z))
        # scale sliders
        size_scale_x = self.x_scale_slide.value()
        size_scale_y = self.y_scale_slide.value()
        size_scale_z = self.z_scale_slide.value()
        self.x_scale_value_le.setText(str(size_scale_x))
        self.y_scale_value_le.setText(str(size_scale_y))
        self.z_scale_value_le.setText(str(size_scale_z))

    def _displacement_rotation_ui(self):
        self.rotation_lbl = QtWidgets.QLabel("Random Rotate Offset")
        self.rotation_lbl.setFixedWidth(125)
        self.x_lbl = QtWidgets.QLabel("X:")
        self.x_rotate_value_le = QtWidgets.QLineEdit("0")
        self.x_rotate_value_le.setFixedWidth(25)
        self.x_rotate_slide = self.slider_setup()
        self.y_lbl = QtWidgets.QLabel("Y:")
        self.y_rotate_value_le = QtWidgets.QLineEdit("0")
        self.y_rotate_value_le.setFixedWidth(25)
        self.y_rotate_slide = self.slider_setup()
        self.z_lbl = QtWidgets.QLabel("Z:")
        self.z_rotate_value_le = QtWidgets.QLineEdit("0")
        self.z_rotate_value_le.setFixedWidth(25)
        self.z_rotate_slide = self.slider_setup()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rotation_lbl)
        self.widgetLayout = self._displacement_rotation_widgets()
        layout.addLayout(self.widgetLayout)
        return layout

    def _displacement_rotation_widgets(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.x_lbl, 0, 0)
        layout.addWidget(self.x_rotate_value_le, 0, 1)
        layout.addWidget(self.x_rotate_slide, 0, 2)
        layout.addWidget(self.y_lbl, 1, 0)
        layout.addWidget(self.y_rotate_value_le, 1, 1)
        layout.addWidget(self.y_rotate_slide, 1, 2)
        layout.addWidget(self.z_lbl, 2, 0)
        layout.addWidget(self.z_rotate_value_le, 2, 1)
        layout.addWidget(self.z_rotate_slide, 2, 2)
        return layout

    def _displacement_scale_ui(self):
        self.scale_lbl = QtWidgets.QLabel("Random Scale Offset")
        self.scale_lbl.setFixedWidth(125)
        self.x_lbl = QtWidgets.QLabel("X:")
        self.x_scale_value_le = QtWidgets.QLineEdit("0")
        self.x_scale_value_le.setFixedWidth(25)
        self.x_scale_slide = self.slider_setup()
        self.y_lbl = QtWidgets.QLabel("Y:")
        self.y_scale_value_le = QtWidgets.QLineEdit("0")
        self.y_scale_value_le.setFixedWidth(25)
        self.y_scale_slide = self.slider_setup()
        self.z_lbl = QtWidgets.QLabel("Z:")
        self.z_scale_value_le = QtWidgets.QLineEdit("0")
        self.z_scale_value_le.setFixedWidth(25)
        self.z_scale_slide = self.slider_setup()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scale_lbl)
        self.widgetLayout = self._displacement_scale_widgets()
        layout.addLayout(self.widgetLayout)
        return layout

    def _displacement_scale_widgets(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.x_lbl, 0, 0)
        layout.addWidget(self.x_scale_value_le, 0, 1)
        layout.addWidget(self.x_scale_slide, 0, 2)
        layout.addWidget(self.y_lbl, 1, 0)
        layout.addWidget(self.y_scale_value_le, 1, 1)
        layout.addWidget(self.y_scale_slide, 1, 2)
        layout.addWidget(self.z_lbl, 2, 0)
        layout.addWidget(self.z_scale_value_le, 2, 1)
        layout.addWidget(self.z_scale_slide, 2, 2)
        return layout

    def selected_button_setup(self):
        select_btn = QtWidgets.QPushButton("Selected")
        select_btn.setFixedWidth(50)
        return select_btn

    def selected_label_setup(self):
        select_le = QtWidgets.QLineEdit()
        select_le.setFixedWidth(200)
        return select_le

    def selected_name(self):
        first_object = cmds.ls(orderedSelection=True)
        first_object = first_object[0]
        cmds.select(first_object)
        return first_object

    def _scatter_ui(self):
        self.scatterObj_lbl = QtWidgets.QLabel("Object to scatter:")
        self.scatterObj_lbl.setFixedWidth(125)
        self.scatter_btn = self.selected_button_setup()
        self.scatter_le = self.selected_label_setup()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatterObj_lbl, 0, 0)
        layout.addWidget(self.scatter_le, 0, 1)
        layout.addWidget(self.scatter_btn, 0, 2)
        return layout

    def _destination_ui(self):
        self.destObj_lbl = QtWidgets.QLabel("Object to scatter onto:")
        self.destObj_lbl.setFixedWidth(125)
        self.dest_btn = self.selected_button_setup()
        self.dest_le = self.selected_label_setup()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.destObj_lbl, 0, 0)
        layout.addWidget(self.dest_le, 0, 1)
        layout.addWidget(self.dest_btn, 0, 2)
        return layout

    def connection(self):
        self.scatter_btn.clicked.connect(self.selected_scat_value)
        self.dest_btn.clicked.connect(self.selected_dest_value)
        self.apply_btn.clicked.connect(self.scatter_objects)
        self.cancel_btn.clicked.connect(self.cancel_window)

    @QtCore.Slot()
    def selected_scat_value(self):
        scat_temp = self.selected_name()
        self.scatter_le.setText(str(scat_temp))

    @QtCore.Slot()
    def selected_dest_value(self):
        dest_temp = self.selected_name()
        self.dest_le.setText(str(dest_temp))

    def return_scatter_name(self):
        return self.scatter_le.text()

    def return_destination_name(self):
        return self.dest_le.text()

    def scatter_objects(self):
        scatter_name = self.scatter_le.text()
        dest_name = self.dest_le.text()
        vertex_names = cmds.polyListComponentConversion(str(dest_name), toVertex=True)
        vertex_names = cmds.filterExpand(vertex_names, selectionMask=31)
        cmds.select(vertex_names)

        if cmds.objectType(scatter_name) == "transform":

            for vertex in vertex_names:
                new_instance = cmds.instance(scatter_name)
                position = cmds.pointPosition(vertex, world=True)
                cmds.move(position[0], position[1], position[2],
                          new_instance, absolute=True, worldSpace=True)

        else:
            cmds.error("That didn't work")

    def cancel_window(self):
        ui.close()


ui = ScatterToolUI()
ui.show()

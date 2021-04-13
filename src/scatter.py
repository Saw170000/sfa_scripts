import logging
import random
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

random.seed(1)
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
        """Creates main ui"""
        title_lbl = QtWidgets.QLabel("Scatter Tool")
        title_lbl.setStyleSheet("font: bold 20px")
        scatter_lay = self._scatter_ui()
        destination_lay = self._destination_ui()
        displace_rotate_lay = self._displacement_rotation_ui()
        displace_scale_lay = self._displacement_scale_ui()
        apply_cancel_lay = self.button_setup()
        main_lay = self.main_lay_layout(apply_cancel_lay, destination_lay,
                                        displace_rotate_lay, displace_scale_lay,
                                        scatter_lay, title_lbl)
        self.setLayout(main_lay)

    def main_lay_layout(self, apply_cancel_lay, destination_lay,
                        displace_rotate_lay, displace_scale_lay, scatter_lay,
                        title_lbl):
        """Organizes main ui widget layouts"""
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
        return main_lay

    def button_setup(self):
        """Creates Apply and Cancel buttons"""
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def slider_setup(self):
        """Setup for creating sliders"""
        slider = QtWidgets.QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(360)
        slider.valueChanged.connect(self.changed_value)
        return slider

    def changed_value(self):
        """Keeps track of slider value and records it"""
        size_rotate_x = self.x_rotate_slide.value()
        size_rotate_y = self.y_rotate_slide.value()
        size_rotate_z = self.z_rotate_slide.value()
        self.x_rotate_value_le.setText(str(size_rotate_x))
        self.y_rotate_value_le.setText(str(size_rotate_y))
        self.z_rotate_value_le.setText(str(size_rotate_z))

    def _displacement_rotation_ui(self):
        """The ui for rotation"""
        self.rotation_lbl = QtWidgets.QLabel("Random Rotate Offset")
        self.rotation_lbl.setFixedWidth(125)
        self._displacement_rotation_xyz_widgets()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rotation_lbl)
        self.widgetLayout = self._displacement_rotation_layout()
        layout.addLayout(self.widgetLayout)
        return layout

    def _displacement_rotation_xyz_widgets(self):
        """Creates widgets for x, y, and z rotation variables"""
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

    def _displacement_rotation_layout(self):
        """Organizes rotation ui layout"""
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
        """The UI for scale"""
        self.scale_lbl = QtWidgets.QLabel("Random Scale Offset")
        self.scale_lbl.setFixedWidth(125)
        self.min_lbl = QtWidgets.QLabel("Min:")
        self.max_lbl = QtWidgets.QLabel("Max:")

        self._displacement_scale_xyz_widgets()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scale_lbl)
        self.widgetLayout = self._displacement_scale_layout()
        layout.addLayout(self.widgetLayout)
        return layout

    def _displacement_scale_xyz_widgets(self):
        """Creates widgets for x, y, and z scale variables"""
        self.x_lbl = QtWidgets.QLabel("X:")
        self.x_min_value_le = QtWidgets.QLineEdit("1")
        self.x_max_value_le = QtWidgets.QLineEdit("1")
        self.y_lbl = QtWidgets.QLabel("Y:")
        self.y_min_value_le = QtWidgets.QLineEdit("1")
        self.y_max_value_le = QtWidgets.QLineEdit("1")
        self.z_lbl = QtWidgets.QLabel("Z:")
        self.z_min_value_le = QtWidgets.QLineEdit("1")
        self.z_max_value_le = QtWidgets.QLineEdit("1")

    def _displacement_scale_layout(self):
        """Organizes scale ui layout"""
        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 25)
        layout.setColumnStretch(3, 10)
        layout.addWidget(self.min_lbl, 0, 1)
        layout.addWidget(self.max_lbl, 0, 2)
        layout.addWidget(self.x_lbl, 1, 0)
        layout.addWidget(self.x_min_value_le, 1, 1)
        layout.addWidget(self.x_max_value_le, 1, 2)
        layout.addWidget(self.y_lbl, 2, 0)
        layout.addWidget(self.y_min_value_le, 2, 1)
        layout.addWidget(self.y_max_value_le, 2, 2)
        layout.addWidget(self.z_lbl, 3, 0)
        layout.addWidget(self.z_min_value_le, 3, 1)
        layout.addWidget(self.z_max_value_le, 3, 2)
        return layout

    def selected_button_setup(self):
        """Setup for creating Selected buttons"""
        select_btn = QtWidgets.QPushButton("Selected")
        select_btn.setFixedWidth(50)
        return select_btn

    def selected_le_setup(self):
        """Setup for creating Selected line edits"""
        select_le = QtWidgets.QLineEdit()
        select_le.setFixedWidth(200)
        return select_le

    def selected_name(self):
        """Stores name of first object selected"""
        first_object = cmds.ls(orderedSelection=True)
        first_object = first_object[0]
        cmds.select(first_object)
        return first_object

    def _scatter_ui(self):
        """The ui for object to scatter"""
        self.scatterObj_lbl = QtWidgets.QLabel("Object to scatter:")
        self.scatterObj_lbl.setFixedWidth(125)
        self.scatter_btn = self.selected_button_setup()
        self.scatter_le = self.selected_le_setup()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatterObj_lbl, 0, 0)
        layout.addWidget(self.scatter_le, 0, 1)
        layout.addWidget(self.scatter_btn, 0, 2)
        return layout

    def _destination_ui(self):
        """The ui for the object that'll be scattered onto"""
        self.destObj_lbl = QtWidgets.QLabel("Object to scatter onto:")
        self.destObj_lbl.setFixedWidth(125)
        self.dest_btn = self.selected_button_setup()
        self.dest_le = self.selected_le_setup()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.destObj_lbl, 0, 0)
        layout.addWidget(self.dest_le, 0, 1)
        layout.addWidget(self.dest_btn, 0, 2)
        return layout

    def connection(self):
        """Connects buttons"""
        self.scatter_btn.clicked.connect(self.selected_scat_value)
        self.dest_btn.clicked.connect(self.selected_dest_value)
        self.apply_btn.clicked.connect(self.scatter_objects)
        self.cancel_btn.clicked.connect(self.cancel_window)

    @QtCore.Slot()
    def selected_scat_value(self):
        """Stores the selected object name as scatter name"""
        scat_temp = self.selected_name()
        self.scatter_le.setText(str(scat_temp))

    @QtCore.Slot()
    def selected_dest_value(self):
        """Stores the selected object name as destination object name"""
        dest_temp = self.selected_name()
        self.dest_le.setText(str(dest_temp))

    def return_scatter_name(self):
        """Returns scatter name"""
        return self.scatter_le.text()

    def return_destination_name(self):
        """Returns destination object name"""
        return self.dest_le.text()

    def scatter_objects(self):
        """Scatters the scatter object onto the destination object"""
        scatter_name = self.scatter_le.text()
        dest_name = self.dest_le.text()

        if cmds.objExists(scatter_name) & cmds.objExists(dest_name):
            if cmds.objectType(scatter_name) == "transform":

                vertex_names = cmds.polyListComponentConversion(str(dest_name), toVertex=True)
                vertex_names = cmds.filterExpand(vertex_names, selectionMask=31)

                cmds.select(vertex_names)

                instance_group = cmds.group(empty=True,
                                            name=scatter_name + '_instance_grp#', )
                self.scatter_loop(instance_group, scatter_name, vertex_names)

            else:
                cmds.error(scatter_name + " is not a Transform object")
        else:
            cmds.error("Couldn't find '" + scatter_name + "' or '"
                       + dest_name + "' object.")
    
    def scatter_loop(self, instance_group, scatter_name, vertex_names):
        """The loop for scattering the scatter object onto each vertex"""
        for vertex in vertex_names:
            new_instance = cmds.instance(scatter_name,
                                         name=scatter_name +
                                         '_instance#', smartTransform=True)
            cmds.parent(new_instance, instance_group)
            position = cmds.pointPosition(vertex, world=True)
            cmds.move(position[0], position[1], position[2],
                      new_instance)

            self.scatter_rotate_scale(new_instance)

    def scatter_rotate_scale(self, new_instance):
        """Generates random variables for rotate and scale"""
        x_rotate = random.uniform(0, int(self.x_rotate_value_le.text()))
        y_rotate = random.uniform(0, int(self.y_rotate_value_le.text()))
        z_rotate = random.uniform(0, int(self.z_rotate_value_le.text()))
        cmds.rotate(x_rotate, y_rotate, z_rotate, new_instance)
        x_scale = random.uniform(int(self.x_min_value_le.text()),
                                 int(self.x_max_value_le.text()))
        y_scale = random.uniform(int(self.y_min_value_le.text()),
                                 int(self.y_max_value_le.text()))
        z_scale = random.uniform(int(self.z_max_value_le.text()),
                                 int(self.z_max_value_le.text()))
        cmds.scale(x_scale, y_scale, z_scale, new_instance)

    def cancel_window(self):
        """Closes UI"""
        ui.close()


ui = ScatterToolUI()
ui.show()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ivanbusthomi/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/EqDistant/eq_distant_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EqDistantDockWidgetBase(object):
    def setupUi(self, EqDistantDockWidgetBase):
        EqDistantDockWidgetBase.setObjectName("EqDistantDockWidgetBase")
        EqDistantDockWidgetBase.resize(524, 766)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.interpolate_value_a = QtWidgets.QLineEdit(self.groupBox)
        self.interpolate_value_a.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolate_value_a.sizePolicy().hasHeightForWidth())
        self.interpolate_value_a.setSizePolicy(sizePolicy)
        self.interpolate_value_a.setMaximumSize(QtCore.QSize(50, 16777215))
        self.interpolate_value_a.setObjectName("interpolate_value_a")
        self.gridLayout_4.addWidget(self.interpolate_value_a, 1, 2, 1, 1)
        self.interpolate_input_a = QtWidgets.QCheckBox(self.groupBox)
        self.interpolate_input_a.setEnabled(False)
        self.interpolate_input_a.setObjectName("interpolate_input_a")
        self.gridLayout_4.addWidget(self.interpolate_input_a, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.interpolate_unit_a = QtWidgets.QComboBox(self.groupBox)
        self.interpolate_unit_a.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolate_unit_a.sizePolicy().hasHeightForWidth())
        self.interpolate_unit_a.setSizePolicy(sizePolicy)
        self.interpolate_unit_a.setMaximumSize(QtCore.QSize(80, 16777215))
        self.interpolate_unit_a.setObjectName("interpolate_unit_a")
        self.interpolate_unit_a.addItem("")
        self.interpolate_unit_a.addItem("")
        self.interpolate_unit_a.addItem("")
        self.gridLayout_4.addWidget(self.interpolate_unit_a, 1, 3, 1, 1)
        self.selected_input_a = QtWidgets.QCheckBox(self.groupBox)
        self.selected_input_a.setEnabled(False)
        self.selected_input_a.setObjectName("selected_input_a")
        self.gridLayout_4.addWidget(self.selected_input_a, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.mcb_input_a = gui.QgsMapLayerComboBox(self.groupBox)
        self.mcb_input_a.setObjectName("mcb_input_a")
        self.horizontalLayout.addWidget(self.mcb_input_a)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_preprocess = QtWidgets.QPushButton(self.groupBox)
        self.btn_preprocess.setMinimumSize(QtCore.QSize(75, 0))
        self.btn_preprocess.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btn_preprocess.setObjectName("btn_preprocess")
        self.horizontalLayout_4.addWidget(self.btn_preprocess)
        self.gridLayout.addLayout(self.horizontalLayout_4, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.mcb_input_b = gui.QgsMapLayerComboBox(self.groupBox)
        self.mcb_input_b.setObjectName("mcb_input_b")
        self.horizontalLayout_2.addWidget(self.mcb_input_b)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.interpolate_unit_b = QtWidgets.QComboBox(self.groupBox)
        self.interpolate_unit_b.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolate_unit_b.sizePolicy().hasHeightForWidth())
        self.interpolate_unit_b.setSizePolicy(sizePolicy)
        self.interpolate_unit_b.setMaximumSize(QtCore.QSize(80, 16777215))
        self.interpolate_unit_b.setObjectName("interpolate_unit_b")
        self.interpolate_unit_b.addItem("")
        self.interpolate_unit_b.addItem("")
        self.interpolate_unit_b.addItem("")
        self.gridLayout_5.addWidget(self.interpolate_unit_b, 0, 4, 1, 1)
        self.selected_input_b = QtWidgets.QCheckBox(self.groupBox)
        self.selected_input_b.setEnabled(False)
        self.selected_input_b.setObjectName("selected_input_b")
        self.gridLayout_5.addWidget(self.selected_input_b, 1, 2, 1, 1)
        self.interpolate_value_b = QtWidgets.QLineEdit(self.groupBox)
        self.interpolate_value_b.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolate_value_b.sizePolicy().hasHeightForWidth())
        self.interpolate_value_b.setSizePolicy(sizePolicy)
        self.interpolate_value_b.setMaximumSize(QtCore.QSize(50, 16777215))
        self.interpolate_value_b.setObjectName("interpolate_value_b")
        self.gridLayout_5.addWidget(self.interpolate_value_b, 0, 3, 1, 1)
        self.interpolate_input_b = QtWidgets.QCheckBox(self.groupBox)
        self.interpolate_input_b.setEnabled(False)
        self.interpolate_input_b.setObjectName("interpolate_input_b")
        self.gridLayout_5.addWidget(self.interpolate_input_b, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 5, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.outputGroup = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.outputGroup.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputGroup.sizePolicy().hasHeightForWidth())
        self.outputGroup.setSizePolicy(sizePolicy)
        self.outputGroup.setObjectName("outputGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.outputGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.outputGroup)
        self.label_10.setMinimumSize(QtCore.QSize(100, 0))
        self.label_10.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.folder_path = QtWidgets.QLineEdit(self.outputGroup)
        self.folder_path.setEnabled(False)
        self.folder_path.setReadOnly(True)
        self.folder_path.setObjectName("folder_path")
        self.horizontalLayout_10.addWidget(self.folder_path)
        self.btn_browse_dir = QtWidgets.QPushButton(self.outputGroup)
        self.btn_browse_dir.setEnabled(False)
        self.btn_browse_dir.setMinimumSize(QtCore.QSize(75, 0))
        self.btn_browse_dir.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_browse_dir.setObjectName("btn_browse_dir")
        self.horizontalLayout_10.addWidget(self.btn_browse_dir)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 2, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.outputGroup)
        self.label_11.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        self.check_median_line = QtWidgets.QCheckBox(self.outputGroup)
        self.check_median_line.setChecked(True)
        self.check_median_line.setObjectName("check_median_line")
        self.horizontalLayout_11.addWidget(self.check_median_line)
        self.check_construction_line = QtWidgets.QCheckBox(self.outputGroup)
        self.check_construction_line.setObjectName("check_construction_line")
        self.horizontalLayout_11.addWidget(self.check_construction_line)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.outputGroup)
        self.label_14.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_14.addWidget(self.label_14)
        self.check_equidistant_point = QtWidgets.QCheckBox(self.outputGroup)
        self.check_equidistant_point.setObjectName("check_equidistant_point")
        self.horizontalLayout_14.addWidget(self.check_equidistant_point)
        self.gridLayout_2.addLayout(self.horizontalLayout_14, 6, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_15 = QtWidgets.QLabel(self.outputGroup)
        self.label_15.setMinimumSize(QtCore.QSize(100, 0))
        self.label_15.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_12.addWidget(self.label_15)
        self.check_load_result = QtWidgets.QCheckBox(self.outputGroup)
        self.check_load_result.setEnabled(False)
        self.check_load_result.setChecked(True)
        self.check_load_result.setObjectName("check_load_result")
        self.horizontalLayout_12.addWidget(self.check_load_result)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.outputGroup)
        self.label_13.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        self.rb_saveToFolder = QtWidgets.QRadioButton(self.outputGroup)
        self.rb_saveToFolder.setObjectName("rb_saveToFolder")
        self.horizontalLayout_13.addWidget(self.rb_saveToFolder)
        self.rb_saveAsTemporary = QtWidgets.QRadioButton(self.outputGroup)
        self.rb_saveAsTemporary.setChecked(True)
        self.rb_saveAsTemporary.setObjectName("rb_saveAsTemporary")
        self.horizontalLayout_13.addWidget(self.rb_saveAsTemporary)
        self.gridLayout_2.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_16 = QtWidgets.QLabel(self.outputGroup)
        self.label_16.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_15.addWidget(self.label_16)
        self.check_final_boundary = QtWidgets.QCheckBox(self.outputGroup)
        self.check_final_boundary.setObjectName("check_final_boundary")
        self.horizontalLayout_15.addWidget(self.check_final_boundary)
        self.buffer_value = QtWidgets.QLineEdit(self.outputGroup)
        self.buffer_value.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buffer_value.sizePolicy().hasHeightForWidth())
        self.buffer_value.setSizePolicy(sizePolicy)
        self.buffer_value.setMaximumSize(QtCore.QSize(50, 16777215))
        self.buffer_value.setObjectName("buffer_value")
        self.horizontalLayout_15.addWidget(self.buffer_value)
        self.buffer_unit = QtWidgets.QComboBox(self.outputGroup)
        self.buffer_unit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buffer_unit.sizePolicy().hasHeightForWidth())
        self.buffer_unit.setSizePolicy(sizePolicy)
        self.buffer_unit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.buffer_unit.setObjectName("buffer_unit")
        self.buffer_unit.addItem("")
        self.buffer_unit.addItem("")
        self.buffer_unit.addItem("")
        self.horizontalLayout_15.addWidget(self.buffer_unit)
        self.gridLayout_2.addLayout(self.horizontalLayout_15, 7, 0, 1, 1)
        self.gridLayout_3.addWidget(self.outputGroup, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.check_debug_mode = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.check_debug_mode.setObjectName("check_debug_mode")
        self.horizontalLayout_3.addWidget(self.check_debug_mode)
        self.btn_help = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_help.setObjectName("btn_help")
        self.horizontalLayout_3.addWidget(self.btn_help)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btn_clear = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_clear.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_clear.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btn_clear.setObjectName("btn_clear")
        self.horizontalLayout_3.addWidget(self.btn_clear)
        self.btn_process = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_process.setMinimumSize(QtCore.QSize(75, 0))
        self.btn_process.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btn_process.setObjectName("btn_process")
        self.horizontalLayout_3.addWidget(self.btn_process)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 3, 0, 1, 1)
        EqDistantDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(EqDistantDockWidgetBase)
        self.rb_saveToFolder.toggled['bool'].connect(self.folder_path.setEnabled)
        self.rb_saveToFolder.toggled['bool'].connect(self.btn_browse_dir.setEnabled)
        self.interpolate_input_a.toggled['bool'].connect(self.interpolate_value_a.setEnabled)
        self.interpolate_input_a.toggled['bool'].connect(self.interpolate_unit_a.setEnabled)
        self.interpolate_input_b.toggled['bool'].connect(self.interpolate_value_b.setEnabled)
        self.interpolate_input_b.toggled['bool'].connect(self.interpolate_unit_b.setEnabled)
        self.rb_saveToFolder.toggled['bool'].connect(self.check_load_result.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(EqDistantDockWidgetBase)

    def retranslateUi(self, EqDistantDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        EqDistantDockWidgetBase.setWindowTitle(_translate("EqDistantDockWidgetBase", "EqDistant"))
        self.groupBox.setTitle(_translate("EqDistantDockWidgetBase", "Input"))
        self.interpolate_value_a.setToolTip(_translate("EqDistantDockWidgetBase", "Interval distance. Line segment shorter than this value will be interpolated."))
        self.interpolate_input_a.setToolTip(_translate("EqDistantDockWidgetBase", "Interpolate point at a given interval. Enabled on input layer in Projected CRS."))
        self.interpolate_input_a.setText(_translate("EqDistantDockWidgetBase", "Interpolate point"))
        self.interpolate_unit_a.setItemText(0, _translate("EqDistantDockWidgetBase", "Meter"))
        self.interpolate_unit_a.setItemText(1, _translate("EqDistantDockWidgetBase", "Kilometer"))
        self.interpolate_unit_a.setItemText(2, _translate("EqDistantDockWidgetBase", "Nautical Miles"))
        self.selected_input_a.setToolTip(_translate("EqDistantDockWidgetBase", "Only use selected features in this layer as input for line creation."))
        self.selected_input_a.setText(_translate("EqDistantDockWidgetBase", "Selected features only"))
        self.label.setText(_translate("EqDistantDockWidgetBase", "Input Layer A"))
        self.btn_preprocess.setToolTip(_translate("EqDistantDockWidgetBase", "Preprocess input data to get initial overview on the area."))
        self.btn_preprocess.setText(_translate("EqDistantDockWidgetBase", "Preprocess"))
        self.label_2.setText(_translate("EqDistantDockWidgetBase", "Input Layer B"))
        self.interpolate_unit_b.setItemText(0, _translate("EqDistantDockWidgetBase", "Meter"))
        self.interpolate_unit_b.setItemText(1, _translate("EqDistantDockWidgetBase", "Kilometer"))
        self.interpolate_unit_b.setItemText(2, _translate("EqDistantDockWidgetBase", "Nautical Miles"))
        self.selected_input_b.setToolTip(_translate("EqDistantDockWidgetBase", "Only use selected features in this layer as input for line creation."))
        self.selected_input_b.setText(_translate("EqDistantDockWidgetBase", "Selected features only"))
        self.interpolate_value_b.setToolTip(_translate("EqDistantDockWidgetBase", "Interval distance. Line segment shorter than this value will be interpolated."))
        self.interpolate_input_b.setToolTip(_translate("EqDistantDockWidgetBase", "Interpolate point at a given interval. Enabled on input layer in Projected CRS."))
        self.interpolate_input_b.setText(_translate("EqDistantDockWidgetBase", "Interpolate point"))
        self.outputGroup.setTitle(_translate("EqDistantDockWidgetBase", "Output"))
        self.label_10.setText(_translate("EqDistantDockWidgetBase", "Directory"))
        self.btn_browse_dir.setToolTip(_translate("EqDistantDockWidgetBase", "Browse for folder to save the results layer."))
        self.btn_browse_dir.setText(_translate("EqDistantDockWidgetBase", "..."))
        self.label_11.setText(_translate("EqDistantDockWidgetBase", "Output Option"))
        self.check_median_line.setToolTip(_translate("EqDistantDockWidgetBase", "Median / Equidistant line"))
        self.check_median_line.setText(_translate("EqDistantDockWidgetBase", "Median Line"))
        self.check_construction_line.setToolTip(_translate("EqDistantDockWidgetBase", "Construction line indicates which point in the input layer that is used in creating the median line."))
        self.check_construction_line.setText(_translate("EqDistantDockWidgetBase", "Construction Line"))
        self.check_equidistant_point.setToolTip(_translate("EqDistantDockWidgetBase", "Equidistant point"))
        self.check_equidistant_point.setText(_translate("EqDistantDockWidgetBase", "Equidistant Point"))
        self.check_load_result.setToolTip(_translate("EqDistantDockWidgetBase", "Construction line indicates which point in the input layer that is used in creating the median line."))
        self.check_load_result.setText(_translate("EqDistantDockWidgetBase", "Load results"))
        self.label_13.setText(_translate("EqDistantDockWidgetBase", "Output Location"))
        self.rb_saveToFolder.setToolTip(_translate("EqDistantDockWidgetBase", "Save the final results in local folder."))
        self.rb_saveToFolder.setText(_translate("EqDistantDockWidgetBase", "Save to local folder"))
        self.rb_saveAsTemporary.setToolTip(_translate("EqDistantDockWidgetBase", "Save the final results as memory layer."))
        self.rb_saveAsTemporary.setText(_translate("EqDistantDockWidgetBase", "as temporary file"))
        self.check_final_boundary.setToolTip(_translate("EqDistantDockWidgetBase", "Equidistant point"))
        self.check_final_boundary.setText(_translate("EqDistantDockWidgetBase", "Generate Boundary"))
        self.buffer_value.setToolTip(_translate("EqDistantDockWidgetBase", "Interval distance. Line segment shorter than this value will be interpolated."))
        self.buffer_unit.setItemText(0, _translate("EqDistantDockWidgetBase", "Meter"))
        self.buffer_unit.setItemText(1, _translate("EqDistantDockWidgetBase", "Kilometer"))
        self.buffer_unit.setItemText(2, _translate("EqDistantDockWidgetBase", "Nautical Miles"))
        self.check_debug_mode.setToolTip(_translate("EqDistantDockWidgetBase", "Export all intermediate results to the layer list as memory layers."))
        self.check_debug_mode.setText(_translate("EqDistantDockWidgetBase", "Debug Mode"))
        self.btn_help.setText(_translate("EqDistantDockWidgetBase", "Help"))
        self.btn_clear.setToolTip(_translate("EqDistantDockWidgetBase", "Clear all input."))
        self.btn_clear.setText(_translate("EqDistantDockWidgetBase", "Clear"))
        self.btn_process.setText(_translate("EqDistantDockWidgetBase", "Process"))
        self.pushButton.setText(_translate("EqDistantDockWidgetBase", "Custom Button"))
from qgis import gui

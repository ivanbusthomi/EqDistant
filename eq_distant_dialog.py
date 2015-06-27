# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EqDistantDialog
                                 A QGIS plugin
 This plugin creates equidistant line
                             -------------------
        begin                : 2014-12-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Ivan Busthomi
        email                : ivanbusthomi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from qgis.gui import QgsMapToolEmitPoint, QgsMessageBar, QgsVertexMarker
from qgis.core import *
from qgis.utils import reloadPlugin

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'eq_distant_dialog_base.ui'))

HELP_CLASS, _ = uic.loadUiType(os.path.join(                                # <---- load ui files for help dialog class
    os.path.dirname(__file__), 'eq_distant_dialog_help.ui'))

class EqDistantDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):            # <---- pass iface
        """Constructor."""
        super(EqDistantDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.hdlg = EqDistantDialogHelp()
        self.iface = iface                      # <---- pass iface
        self.canvas = iface.mapCanvas()
        self.closeEvnt = QtGui.QCloseEvent

    def on_btnHelp_pressed(self):
        self.hdlg.show()

    def on_btnClose_pressed(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        try:
            self.canvas.scene().removeItem(self.vm_sa)
            self.canvas.scene().removeItem(self.vm_sb)
            self.canvas.scene().removeItem(self.vm_ea)
            self.canvas.scene().removeItem(self.vm_eb)
        except AttributeError:
            pass
        self.close()
        reloadPlugin('EqDistant')

    # --- Daerah berhadapan
    # fungsi titik awal A
    def on_opp_btnStartA_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_sa)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify start point for Layer A',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clicked_start_a)
        self.hide()

    def clicked_start_a(self, point):
        self.start_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.vm_sa = QgsVertexMarker(self.canvas)
        self.vm_sa.setCenter(point)
        self.lineEdit_sa.setText("%s, %s" % (str(round(self.start_a.x(), 3)),
                                             str(round(self.start_a.y(), 3))))
        self.clickTool.deactivate()
        self.show()

    # fungsi titik akhir A
    def on_opp_btnEndA_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_ea)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify end point for Layer A',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clicked_end_a)
        self.hide()

    def clicked_end_a(self, point):
        self.end_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.vm_ea = QgsVertexMarker(self.canvas)
        self.vm_ea.setCenter(point)
        self.lineEdit_ea.setText("%s, %s" % (str(round(self.end_a.x(), 3)),
                                             str(round(self.end_a.y(), 3))))
        self.clickTool.deactivate()
        self.show()

    # fungsi titik awal B
    def on_opp_btnStartB_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_sb)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify start point for Layer B',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clicked_start_b)
        self.hide()

    def clicked_start_b(self, point):
        self.start_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.vm_sb = QgsVertexMarker(self.canvas)
        self.vm_sb.setCenter(point)
        self.lineEdit_sb.setText("%s, %s" % (str(round(self.start_b.x(), 3)),
                                             str(round(self.start_b.y(), 3))))
        self.clickTool.deactivate()
        self.show()

    # fungsi titik akhir B
    def on_opp_btnEndB_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_eb)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify end point for Layer B',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clicked_end_b)
        self.hide()

    def clicked_end_b(self, point):
        self.end_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.vm_eb = QgsVertexMarker(self.canvas)
        self.vm_eb.setCenter(point)
        self.lineEdit_eb.setText("%s, %s" % (str(round(self.end_b.x(), 3)),
                                             str(round(self.end_b.y(), 3))))
        self.clickTool.deactivate()
        self.show()

    # --- Daerah bersebelahan
    # fungsi titik awal A
    def on_adj_btnStartA_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_sa)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify start point for Layer A',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.adj_clicked_start_a)
        self.hide()

    def adj_clicked_start_a(self, point):
        self.adj_start_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.adj_lineEditA.setText("%s, %s" % (str(round(self.adj_start_a.x(), 3)),
                                               str(round(self.adj_start_a.y(), 3))))
        self.vm_sa = QgsVertexMarker(self.canvas)
        self.vm_sa.setCenter(point)
        self.clickTool.deactivate()
        self.show()
    # fungsi titik awal B
    def on_adj_btnStartB_pressed(self):
        try:
            self.canvas.scene().removeItem(self.vm_sb)
        except AttributeError:
            pass
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info',
                                            'Specify start point for Layer B',
                                            level=QgsMessageBar.INFO,
                                            duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.adj_clicked_start_b)
        self.hide()

    def adj_clicked_start_b(self, point):
        self.adj_start_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.adj_lineEditB.setText("%s, %s" % (str(round(self.adj_start_b.x(), 3)),
                                               str(round(self.adj_start_b.y(), 3))))
        self.vm_sb = QgsVertexMarker(self.canvas)
        self.vm_sb.setCenter(point)
        self.clickTool.deactivate()
        self.show()


class EqDistantDialogHelp(QtGui.QDialog, HELP_CLASS):                   # <---- add Help dialog class
    def __init__(self, parent=None):
        super(EqDistantDialogHelp, self).__init__(parent)
        self.setupUi(self)

    def on_btnClose_pressed(self):
        self.hide()
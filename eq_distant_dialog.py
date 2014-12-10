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
from qgis.gui import QgsMapToolEmitPoint, QgsMessageBar
from qgis.core import *

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
        self.iface = iface                      # <---- pass iface
        #self.adj_claim_dist.setText('100')
        #self.opp_claim_dist.setText('100')


    '''
    def accept(self):
        self.iface.messageBar().clearWidgets()
        self.close()
    '''
    def on_btnHelp_pressed(self):
        self.hdlg = EqDistantDialogHelp()
        self.hdlg.show()

    def on_btnCancel_pressed(self):
        self.reject()

class EqDistantDialogHelp(QtGui.QDialog, HELP_CLASS):                   # <---- add Help dialog class
    def __init__(self, parent=None):
        super(EqDistantDialogHelp, self).__init__(parent)
        self.setupUi(self)

    def on_btnClose_pressed(self):
        self.hdlg = EqDistantDialogHelp()
        self.hdlg.hide()



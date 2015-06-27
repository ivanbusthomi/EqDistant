# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EqDistant
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from qgis.core import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from eq_distant_dialog import EqDistantDialog
import os.path
# import library
from library import Library


class EqDistant:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        # Create the dialog (after translation) and keep reference
        self.iface = iface
        self.dlg = EqDistantDialog(self.iface)
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EqDistant_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&EqDistant Plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EqDistant')
        self.toolbar.setObjectName(u'EqDistant')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EqDistant', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/EqDistant/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'EqDistant Line Plugin'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&EqDistant Plugin'),
                action)
            self.iface.removeToolBarIcon(action)

    # --- fungsi dialog tambahan
    def cek_proses(self):
        if self.dlg.lineEdit_sa.text() and self.dlg.lineEdit_ea.text() and self.dlg.lineEdit_sb.text() and self.dlg.lineEdit_eb.text() != "":
            self.dlg.opp_btnRun.setEnabled(True)
        else:
            self.dlg.opp_btnRun.setEnabled(False)
        if self.dlg.adj_lineEditA.text() and self.dlg.adj_lineEditB.text() and self.dlg.adj_claim_dist.text() != "":
            self.dlg.adj_btnRun.setEnabled(True)
        else:
            self.dlg.adj_btnRun.setEnabled(False)

    def cek_layer_input(self):
        # pendefinisian layer input
        self.layer_a = self.dlg.layerInputA.itemData(self.dlg.layerInputA.currentIndex())
        self.layer_b = self.dlg.layerInputB.itemData(self.dlg.layerInputB.currentIndex())
        self.lib = Library(self.layer_a, self.layer_b, 10)
        if self.layer_a == self.layer_b:
            self.dlg.opp_btnRun.setEnabled(False)
            self.dlg.adj_btnRun.setEnabled(False)
            self.dlg.tabMenu.setEnabled(False)
            self.dlg.labelTitikA.setText("Layer A and Layer B must not same")
            self.dlg.labelTitikB.setText("Layer A and Layer B must not same")
        else:
            self.dlg.opp_btnRun.setEnabled(True)
            self.dlg.adj_btnRun.setEnabled(True)
            self.dlg.tabMenu.setEnabled(True)
            self.cek_terpilih_a()
            self.cek_terpilih_b()
            if len(self.layer_a.selectedFeatures()) != 0:
                self.dlg.checkBox_pilihA.setEnabled(True)
            else:
                self.dlg.checkBox_pilihA.setEnabled(False)
            if len(self.layer_b.selectedFeatures()) != 0:
                self.dlg.checkBox_pilihB.setEnabled(True)
            else:
                self.dlg.checkBox_pilihB.setEnabled(False)
            self.dlg.checkBox_pilihA.stateChanged.connect(self.cek_terpilih_a)
            self.dlg.checkBox_pilihB.stateChanged.connect(self.cek_terpilih_b)

    def cek_terpilih_a(self):
        if self.dlg.checkBox_pilihA.isChecked():
            self.list_feat_garis_a = [feat for feat in self.layer_a.selectedFeatures()]
        else:
            self.list_feat_garis_a = [feat for feat in self.layer_a.getFeatures()]
        self.update_poi_info_a()

    def update_poi_info_a(self):
        self.layer_ttk_a = self.lib.konversi_garis_ke_titik(self.list_feat_garis_a, "A")
        self.list_feat_ttk_a = [feat for feat in self.layer_ttk_a.getFeatures()]
        jml_ttk_a = len(self.list_feat_ttk_a)
        self.dlg.labelTitikA.setText(str(jml_ttk_a) + " points")

    def cek_terpilih_b(self):
        if self.dlg.checkBox_pilihB.isChecked():
            self.list_feat_garis_b = [feat for feat in self.layer_b.selectedFeatures()]
        else:
            self.list_feat_garis_b = [feat for feat in self.layer_b.getFeatures()]
        self.update_poi_info_b()

    def update_poi_info_b(self):
        self.layer_ttk_b = self.lib.konversi_garis_ke_titik(self.list_feat_garis_b, "B")
        self.list_feat_ttk_b = [feat for feat in self.layer_ttk_b.getFeatures()]
        jml_ttk_b = len(self.list_feat_ttk_b)
        self.dlg.labelTitikB.setText(str(jml_ttk_b) + " points")

    # --- eksekusi algoritma
    def hdp_deploy(self):
        list_geom_a = [feat.geometry() for feat in self.list_feat_garis_a]
        list_geom_b = [feat.geometry() for feat in self.list_feat_garis_b]
        list_ft = self.list_feat_ttk_a + self.list_feat_ttk_b
        # pendefinisian titik awal
        t_awal_a = self.lib.titik_pada_garis(self.dlg.start_a, list_geom_a)
        t_akhr_a = self.lib.titik_pada_garis(self.dlg.end_a, list_geom_a)
        t_awal_b = self.lib.titik_pada_garis(self.dlg.start_b, list_geom_b)
        t_akhr_b = self.lib.titik_pada_garis(self.dlg.end_b, list_geom_b)
        # iterasi
        list_g_eq, list_g_cc, list_g_grs_k = self.lib.proses_hdp(t_awal_a,
                                                                 t_awal_b,
                                                                 t_akhr_a,
                                                                 t_akhr_b,
                                                                 list_ft)
        self.lib.konversi_titik_ke_garis(list_g_cc)
        if self.dlg.checkBox_cLine.isChecked():
            self.lib.buat_layer_garis_k(list_g_grs_k)
        if self.dlg.checkBox_titikEq.isChecked():
            self.lib.buat_layer_titik(list_g_cc)

    def sblh_deploy(self):
        list_geom_a = [feat.geometry() for feat in self.list_feat_garis_a]
        list_geom_b = [feat.geometry() for feat in self.list_feat_garis_b]
        list_feat = self.list_feat_ttk_a + self.list_feat_ttk_b
        t_awal_a = self.lib.titik_pada_garis(self.dlg.adj_start_a, list_geom_a)
        t_awal_b = self.lib.titik_pada_garis(self.dlg.adj_start_b, list_geom_b)
        list_t_akhir = []
        for a in list_geom_a:
            for b in list_geom_b:
                if a.intersects(b):
                    t_akhir = a.intersection(b)
                    list_t_akhir.append(t_akhir)
                else:
                    pass
        if len(list_t_akhir) == 0:
            raise ValueError("No end point detected")
        elif len(list_t_akhir) > 1:
            raise ValueError("More than one end point detected")
        else:
            g_akhir = list_t_akhir[0]
            ttk_akhir = g_akhir.asPoint()
        jarak_klaim = int(self.dlg.adj_claim_dist.text())*1852
        self.adj_lib = Library(self.layer_a, self.layer_b, 10, jarak_klaim)
        list_g_eq, list_g_cc, list_g_gk = self.adj_lib.proses_sb(t_awal_a,
                                                                 t_awal_b,
                                                                 ttk_akhir,
                                                                 list_feat)
        self.adj_lib.konversi_titik_ke_garis(list_g_cc)
        if self.dlg.checkBox_cLine.isChecked():
            self.lib.buat_layer_garis_k(list_g_gk)
        if self.dlg.checkBox_titikEq.isChecked():
            self.lib.buat_layer_titik(list_g_cc)

    def run(self):
        # Kosongkan input pada combo box
        self.dlg.layerInputA.clear()
        self.dlg.layerInputB.clear()
        # baca informasi layer yang termuat pada TOC QGIS
        toc_layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_polyline = []
        for lay in toc_layers:
            if lay.type() == QgsMapLayer.VectorLayer and lay.geometryType() == 1:
                layer_polyline.append(lay)
        # cek nilai input
        self.dlg.lineEdit_sa.textChanged.connect(self.cek_proses)
        self.dlg.lineEdit_ea.textChanged.connect(self.cek_proses)
        self.dlg.lineEdit_sb.textChanged.connect(self.cek_proses)
        self.dlg.lineEdit_eb.textChanged.connect(self.cek_proses)
        # -
        self.dlg.adj_lineEditA.textChanged.connect(self.cek_proses)
        self.dlg.adj_lineEditB.textChanged.connect(self.cek_proses)
        self.dlg.adj_claim_dist.textChanged.connect(self.cek_proses)
        # connect function
        self.dlg.opp_btnRun.pressed.connect(self.hdp_deploy)
        self.dlg.adj_btnRun.pressed.connect(self.sblh_deploy)
        # tampilkan dialog jika dua layer polyline telah termuat dalam TOC
        if len(layer_polyline) < 2:
            self.iface.messageBar().pushMessage('Oops!!',
                                                'Please add at least two line layers',
                                                level=QgsMessageBar.CRITICAL,
                                                duration=2)
        else:
            # tampilkan dialog
            self.dlg.show()
            # tambahkan line layer pada TOC
            for layer in layer_polyline:
                self.dlg.layerInputA.addItem(layer.name(), layer)
                self.dlg.layerInputB.addItem(layer.name(), layer)
            self.cek_layer_input()
            self.dlg.layerInputA.currentIndexChanged.connect(self.cek_layer_input)
            self.dlg.layerInputB.currentIndexChanged.connect(self.cek_layer_input)
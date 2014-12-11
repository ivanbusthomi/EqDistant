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
from qgis.gui import QgsMessageBar, QgsMapToolEmitPoint, QgsMapToolPan
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from eq_distant_dialog import EqDistantDialog, EqDistantDialogHelp
from libs.adj_lib_new import AdjacentLibrary
from libs.lay_lib import LayerOperation
from libs.opp_lib import OppositeLibrary
from libs.opp_lib_new import OppositeLibrary as OppositeLibraryNew
import os.path

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
        self.iface = iface
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

        # Create the dialog (after translation) and keep reference
        self.dlg = EqDistantDialog(self.iface)              #<----- pass iface
        self.layOpt = LayerOperation()                      # <---- call LayerOperation from libs.lay_lib
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

    #---------------- Opposite State Tools  #
    def pressedStartA(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik awal untuk layer A',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clickedStartA)
        self.dlg.hide()
    def clickedStartA(self, point, button):
        self.start_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.lineEdit_sa.setText("%s,%s"%(str(round(self.start_a.x(),3)),str(round(self.start_a.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def pressedStartB(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik awal untuk layer B',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clickedStartB)
        self.dlg.hide()
    def clickedStartB(self, point, button):
        self.start_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.lineEdit_sb.setText("%s,%s"%(str(round(self.start_b.x(),3)),str(round(self.start_b.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def pressedEndA(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik akhir untuk layer A',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clickedEndA)
        self.dlg.hide()
    def clickedEndA(self, point, button):
        self.end_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.lineEdit_ea.setText("%s,%s"%(str(round(self.end_a.x(),3)),str(round(self.end_a.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def pressedEndB(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik akhir untuk layer B',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.clickedEndB)
        self.dlg.hide()
    def clickedEndB(self, point, button):
        self.end_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.lineEdit_eb.setText("%s,%s"%(str(round(self.end_b.x(),3)),str(round(self.end_b.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def opp_deploy(self):
        # define layer from comboBox item #
        layer_a = self.dlg.inputLayerA.itemData(self.dlg.inputLayerA.currentIndex())
        layer_b = self.dlg.inputLayerB.itemData(self.dlg.inputLayerB.currentIndex())
        crs = layer_a.crs().authid()
        intv = self.dlg.opp_intv.value()
        # convert line layer to point layer
        point_layer_a = self.layOpt.lineToPoint(layer_a, "A",crs)
        point_layer_b = self.layOpt.lineToPoint(layer_b, "B",crs)
        # create list of features from point layer
        feat_list_a = []
        feat_list_b = []
        for feat in point_layer_a.getFeatures():feat_list_a.append(feat)
        for feat in point_layer_b.getFeatures():feat_list_b.append(feat)
        lib = OppositeLibrary(point_layer_a,point_layer_b,intv)
        #define start and end point in point_layer_a and point_layer_b
        start_point_a = lib.nearestFeat(self.start_a,feat_list_a).geometry().asPoint()
        start_point_b = lib.nearestFeat(self.start_b,feat_list_b).geometry().asPoint()
        end_point_a = lib.nearestFeat(self.end_a,feat_list_a).geometry().asPoint()
        end_point_b = lib.nearestFeat(self.end_b,feat_list_b).geometry().asPoint()
        #mid_start = lib.findMid(start_point_a,start_point_b)
        #mid_end = lib.findMid(end_point_a,end_point_b)
        final_result, construction_line = lib.deploy(feat_list_a,feat_list_b,start_point_a,start_point_b,end_point_a,end_point_b)
        self.layOpt.addPointF(final_result,crs)
        if self.dlg.checkBox_eLine.isChecked():
            self.layOpt.pointsToLine(final_result,crs)
        #if self.dlg.checkBox_eLine.isChecked():
        #    self.layOpt.addLine_FList(construction_line)
        self.dlg.close()

    def opp_deploy_new(self):
        layer_a = self.dlg.inputLayerA.itemData(self.dlg.inputLayerA.currentIndex())
        layer_b = self.dlg.inputLayerB.itemData(self.dlg.inputLayerB.currentIndex())
        crs = layer_a.crs().authid()
        intv = self.dlg.opp_intv.value()
        claim_dist = 1500 #int(self.dlg.opp_claim_dist.text())
        # list initiation
        list_feat_a=[]
        for feat_a in layer_a.getFeatures():list_feat_a.append(feat_a)
        list_feat_b=[]
        for feat_b in layer_b.getFeatures():list_feat_b.append(feat_b)
        list_geom_a=[]
        for feat_a in list_feat_a:list_geom_a.append(feat_a.geometry())
        list_geom_b=[]
        for feat_b in list_feat_b:list_geom_b.append(feat_b.geometry())
        # input point inititation
        start_point_a = self.layOpt.pointinline(self.start_a,list_geom_a)
        start_point_b = self.layOpt.pointinline(self.start_b,list_geom_b)
        end_point_a = self.layOpt.pointinline(self.end_a,list_geom_a)
        end_point_b = self.layOpt.pointinline(self.end_b,list_geom_b)
        # main function
        lib = OppositeLibraryNew(list_geom_a,list_geom_b,claim_dist,intv)
        mid_s = lib.find_mid(start_point_a,start_point_b)
        mid_e = lib.find_mid(end_point_a,end_point_b)
        result = lib.run(start_point_a,start_point_b,end_point_a,end_point_b)
        #self.layOpt.addPointL([start_point_a,mid_s,start_point_b,end_point_a,mid_e,end_point_b],crs)
        #self.layOpt.addPointL(result,crs)
        self.dlg.textBrowser.append(str(start_point_a))
        self.dlg.textBrowser.append(str(start_point_b))
        self.dlg.textBrowser.append(str(end_point_a))
        self.dlg.textBrowser.append(str(end_point_b))

    #---------------- Opposite State Tools  #
    def adj_pressedStartA(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik awal untuk layer A',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.adj_clickedStartA)
        self.dlg.hide()
    def adj_clickedStartA(self, point, button):
        self.adj_start_a = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.adj_lineEditA.setText("%s,%s"%(str(round(self.adj_start_a.x(),3)),str(round(self.adj_start_a.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def adj_pressedStartB(self):
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.messageBar().pushMessage('Info','Input titik awal untuk layer B',level=QgsMessageBar.INFO,duration=1)
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.adj_clickedStartB)
        self.dlg.hide()
    def adj_clickedStartB(self, point, button):
        self.adj_start_b = self.clickTool.toMapCoordinates(self.clickTool.toCanvasCoordinates(point))
        self.dlg.adj_lineEditB.setText("%s,%s"%(str(round(self.adj_start_b.x(),3)),str(round(self.adj_start_b.y(),3))))
        self.clickTool.deactivate()
        self.dlg.show()

    def adj_deploy_new(self):
        layer_a = self.dlg.inputLayerA.itemData(self.dlg.inputLayerA.currentIndex())
        layer_b = self.dlg.inputLayerB.itemData(self.dlg.inputLayerB.currentIndex())
        intv = self.dlg.adj_intv.value()
        claim_dist = int(self.dlg.adj_claim_dist.text())
        list_feat_a = []
        list_feat_b = []
        for feat in layer_a.getFeatures():list_feat_a.append(feat)
        for feat in layer_b.getFeatures():list_feat_b.append(feat)
        list_geom_a = []
        list_geom_b = []
        for feat in list_feat_a:list_geom_a.append(feat.geometry())
        for feat in list_feat_b:list_geom_b.append(feat.geometry())
        lib = AdjacentLibrary(list_geom_a,list_geom_b,claim_dist,intv)
        p_start_a = self.layOpt.pointinline(self.adj_start_a,list_geom_a)
        p_start_b = self.layOpt.pointinline(self.adj_start_b,list_geom_b)
        ends = []
        for line_a in list_geom_a:
            for line_b in list_geom_b:
                if line_a.intersects(line_b):
                    self.dlg.textBrowser.append("intersect")
                    e = line_a.intersection(line_b)
                    ends.append(e)
                else:
                    self.dlg.textBrowser.append("no intersection")
        if len(ends)==0:
            raise ValueError("Tidak bisa mendefinisikan titik akhir")
        elif len(ends)>1:
            raise ValueError("Kandidat titik akhir lebih dari 1")
        else:
            g_end = ends[0]
            p_end = g_end.asPoint()
        result = lib.something(p_start_a,p_start_b,p_end)
        result_feat = []
        for i in result:
            f = QgsFeature()
            f.setGeometry(i)
            result_feat.append(f)
        crs = layer_a.crs().authid()
        #self.layOpt.addPointL(result,crs)
        self.layOpt.pointsToLine(result_feat,crs)
        #self.dlg.textBrowser.append(str(len(list_geom_a)))
        #self.dlg.textBrowser.append(str(len(list_geom_b)))
        #self.dlg.textBrowser.append(str(len(result)))

    def adj_deploy(self):
        layer_a = self.dlg.inputLayerA.itemData(self.dlg.inputLayerA.currentIndex())
        layer_b = self.dlg.inputLayerB.itemData(self.dlg.inputLayerB.currentIndex())
        intv = self.dlg.adj_intv.value()
        claim_dist = int(self.dlg.adj_claim_dist.text())
        lib = AdjacentLibrary(layer_a,layer_b,claim_dist,intv)
        list_feat_a = []
        list_feat_b = []
        for a in layer_a.getFeatures():list_feat_a.append(a)
        for b in layer_b.getFeatures():list_feat_b.append(b)
        list_geom_a=[]
        list_geom_b=[]
        for a in list_feat_a:list_geom_a.append(a.geometry())
        for b in list_feat_b:list_geom_b.append(b.geometry())
        start_point_a = self.layOpt.pointinline(self.adj_start_a,list_geom_a)
        start_point_b = self.layOpt.pointinline(self.adj_start_b,list_geom_b)
        ends = []
        for geom_a in list_geom_a:
            for geom_b in list_geom_b:
                if geom_a.intersects(geom_b):
                    e = geom_a.intersection(geom_b)
                    ends.append(e)
        if len(ends)>1:
            raise ValueError("more than 1 intersection between layer a and layer b")
        else:
            p_end = ends[0].asPoint()
        #list_eq_geom = lib.something(start_point_a,start_point_b,p_end)
        self.dlg.textBrowser.append(p_end.toString())
        #self.layOpt.addPointL(list_eq_geom)

    #------------- main implementation
    def checkInputLayer(self):
        if self.dlg.inputLayerA.currentIndex()==self.dlg.inputLayerB.currentIndex():
            self.dlg.textBrowser.clear()
            self.dlg.textBrowser.append('Ups! Layer Input Gak Boleh Sama')
        else:
            self.dlg.textBrowser.clear()
            self.dlg.textBrowser.append('Layer input siap')

    def checkPoint(self):
        self.dlg.textBrowser.append(str(self.adj_start_a)+' | '+self.adj_start_a.toString())
        self.dlg.textBrowser.append(str(self.adj_start_b)+' | '+self.adj_start_a.toString())
        self.dlg.textBrowser.append(str(self.adj_start_a)+' | '+self.adj_start_a.toString())
    def run(self):
        """Run method that performs all the real work"""
        # clear everytime the dialog loaded #
        self.dlg.inputLayerA.clear()
        self.dlg.inputLayerB.clear()
        self.dlg.inputLayerA.currentIndexChanged.connect(self.checkInputLayer)
        self.dlg.inputLayerB.currentIndexChanged.connect(self.checkInputLayer)
        # connect opposite state map tools
        self.dlg.opp_btnStartA.pressed.connect(self.pressedStartA)
        self.dlg.opp_btnStartB.pressed.connect(self.pressedStartB)
        self.dlg.opp_btnEndA.pressed.connect(self.pressedEndA)
        self.dlg.opp_btnEndB.pressed.connect(self.pressedEndB)
        #self.dlg.btnCancel.pressed.connect(self.dlg.reject)
        # connect adjacent state map tools
        self.dlg.adj_btnStartA.pressed.connect(self.adj_pressedStartA)
        self.dlg.adj_btnStartB.pressed.connect(self.adj_pressedStartB)
        self.dlg.opp_btnRun.pressed.connect(self.opp_deploy_new)
        self.dlg.adj_btnRun.pressed.connect(self.adj_deploy_new)
        # layer checking from map canvas    #
        layers_ = QgsMapLayerRegistry.instance().mapLayers().values()
        line_layers = []
        for i in layers_:
            if i.type() == QgsMapLayer.VectorLayer and i.geometryType() == 1:
                line_layers.append(i)
        if len(line_layers)<2:
            self.iface.messageBar().pushMessage('Tips','Tambahkan minimal dua layer bertipe polyline ke Map Canvas',level=QgsMessageBar.INFO,duration=3)
            self.iface.messageBar().pushMessage('Ups!!','Anda belum menambahkan cukup layer ke Map Canvas',level=QgsMessageBar.CRITICAL,duration=3)
        else:
            # show the dialog
            self.dlg.show()

            # read line layers from mapCanvas, and add it to comboBox #
            for layer in line_layers:
                self.dlg.inputLayerA.addItem(layer.name(),layer)
                self.dlg.inputLayerB.addItem(layer.name(),layer)
            # Run the dialog event loop
            result = self.dlg.exec_()
            # See if OK was pressed
            if result:
                # Do something useful here - delete the line containing pass and
                # substitute with your code.
                pass
                #--------------------------------------------------

    def showHelp(self):
        self.hdlg = EqDistantDialogHelp()
        self.hdlg.show()
from qgis.core import *
from PyQt4.QtCore import QVariant

class LayerOperation(object):
    def __init__(self):
        #self.line_layer = line_layer
        #self.point_layer = point_layer
        #self.attr = attr
        pass

    def lineToPoint(self, line_layer, attr):
        point_layer=QgsVectorLayer("Point", "Point Result", "memory")
        point_layer_prov = point_layer.dataProvider()
        point_layer_prov.addAttributes([QgsField("fid", QVariant.Int),QgsField("ket",QVariant.String)])
        features_list = []
        list_coord = []
        id = 0
        for line in line_layer.getFeatures():
            list_line_coord = line.geometry().asPolyline()
            for coord in list_line_coord:
                list_coord.append(coord)
        for coord in list_coord:
            point_ = QgsPoint(coord[0],coord[1])
            point_geom = QgsGeometry.fromPoint(point_)
            point_feat = QgsFeature()
            point_feat.setGeometry(point_geom)
            point_feat.setAttributes([id,attr])
            id +=1
            features_list.append(point_feat)
        point_layer_prov.addFeatures(features_list)
        point_layer.startEditing()
        point_layer.commitChanges()
        # ______________________comment this so that point_layer will not be added to table of content
        #QgsMapLayerRegistry.instance().addMapLayer(point_layer)
        return point_layer
    def nearestFeat(self,point,feat_list):
        currentDistance = 99999999
        nearest = QgsPoint()
        for p in feat_list:
            p_point = p.geometry().asPoint()
            distance = math.sqrt(point.sqrDist(p_point))
            if distance<currentDistance:
                currentDistance = distance
                nearest = p
        return nearest
    def pointlayerToLine(self,ft_list):
        #ft_list=[]
        #for f in point_layer.getFeatures():
        #    ft_list.append(f)
        res_list = []                                                               #container for result
        s = ft_list[0]                                                            #start point
        s_point = s.geometry().asPoint()
        res_list.append(s_point)                                                #add start to result list
        ft_list.remove(s)
        while len(ft_list)>0:
            n_feat = self.nearestFeat(s_point, ft_list)
            n_point = n_feat.geometry().asPoint()
            res_list.append(n_point)
            ft_list.remove(n_feat)
            s_point = n_point
            #print len(ft_list)
        #convert list of point to line layer
        line_layer = QgsVectorLayer("LineString", "Line Result", "memory")
        line_layer_prov = line_layer.dataProvider()
        feat = QgsFeature()
        line_geom = QgsGeometry.fromPolyline(res_list)
        feat.setGeometry(line_geom)
        line_layer_prov.addFeatures([feat])
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)
    def addPointL(self,list_point_geom):
        point_layer = QgsVectorLayer("Point","Point","memory")
        point_layer_prov = point_layer.dataProvider()
        list_feat = []
        for geom in list_point_geom:
            point_feat = QgsFeature()
            point_feat.setGeometry(geom)
            list_feat.append(point_feat)
        point_layer_prov.addFeatures(list_feat)
        QgsMapLayerRegistry.instance().addMapLayer(point_layer)
    def addPointG(self, point_geom):
        point_layer = QgsVectorLayer("Point","Point","memory")
        point_layer_prov = point_layer.dataProvider()
        point_feat = QgsFeature()
        point_feat.setGeometry(point_geom)
        point_layer_prov.addFeatures([point_feat])
        QgsMapLayerRegistry.instance().addMapLayer(point_layer)
    def addPointF(self, list_point_feat):
        point_layer = QgsVectorLayer("Point","Point", "memory")
        point_layer_prov = point_layer.dataProvider()
        point_layer_prov.addFeatures(list_point_feat)
        QgsMapLayerRegistry.instance().addMapLayer(point_layer)
    def addLine(self,line_geom):
        line_layer = QgsVectorLayer("LineString", "Line Result", "memory")
        line_layer_prov = line_layer.dataProvider()
        line_feat = QgsFeature()
        line_feat.setGeometry(line_geom)
        line_layer_prov.addFeatures([line_feat])
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)
    def addLine_FList(self,line_list):
        line_layer = QgsVectorLayer("LineString", "Construction Line", "memory")
        prov_ = line_layer.dataProvider()
        prov_.addFeatures(line_list)
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)
    def addPolygon(self, poly_geom):
        poly_layer = QgsVectorLayer("Polygon", "Polygon Result", "memory")
        poly_layer_prov =poly_layer.dataProvider()
        poly_feat = QgsFeature()
        poly_feat.setGeometry(poly_geom)
        poly_layer_prov.addFeatures([poly_feat])
        QgsMapLayerRegistry.instance().addMapLayer(poly_layer)

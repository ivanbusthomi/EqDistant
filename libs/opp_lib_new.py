from qgis.core import *
from qgis.gui import QgsLegendInterface
from PyQt4.QtCore import QVariant
import math


class OppositeLibrary(object):
    def __init__(self,iface, list_line_geom_a, list_line_geom_b, intv,crs):
        self.iface = iface
        self.list_line_geom_a = list_line_geom_a
        self.list_line_geom_b = list_line_geom_b
        self.intv = intv
        self.crs = crs

    def find_mid(self, pt_a, pt_b):
        xa = pt_a.x()
        ya = pt_a.y()
        xb = pt_b.x()
        yb = pt_b.y()
        xm = xa - (xa-xb)/2
        ym = ya - (ya-yb)/2
        m = QgsPoint(xm, ym)
        return m

    def point_in_line(self,point,list_line_geom):
        result = {}
        for line_geom in list_line_geom:
            dist,p,int = line_geom.closestSegmentWithContext(point)
            result[p]=dist
        nearest = min(result, key=result.get)
        return nearest

    def find_side(self, pa, pb, p_test):
        xa = pa.x()
        ya = pa.y()
        xb = pb.x()
        yb = pb.y()
        x_test = p_test.x()
        y_test = p_test.y()
        side = (x_test-xa)*(yb-ya)-(y_test-ya)*(xb-xa)
        return side

    def azm(self, pa, pb):
        az = pa.azimuth(pb)
        return az

    def perpendicular_line(self, dist, pa, pb, pc):
        p_mid = self.find_mid(pa,pb)
        az = self.azm(pa,pb)
        side = self.find_side(pa,pb,pc)
        xm = p_mid.x()
        ym = p_mid.y()
        px = xm
        py = ym
        if az>0 and az<90:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                #print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                #print az, side
            else:
                print "side value 1 error"
        elif az>90 and az<180:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                #print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                #print az, side
            else:
                print "side value 2 error"
        elif az<0 and az>-90:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                #print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                #print az, side
            else:
                print "side value 3 error"
        elif az<-90 and az>-180:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                #print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                #print az, side
            else:
                print "side value 4 error"
        else:
            print "azimuth error"
        pp = QgsPoint(px,py)
        pp_line = QgsGeometry.fromPolyline([p_mid,pp])
        return pp_line

    def distanceFromPoint(self,point_a,point_b):
        return math.sqrt(point_a.sqrDist(point_b))

    def iter_point(self, p_a, p_b, mid_e, list_line_geom_a, list_line_geom_b, geom_pp_line):
        current_distance = 0
        geom_eq = QgsGeometry()
        feat = QgsFeature()
        stop_ = False
        buffer_ = QgsGeometry()
        while current_distance<=geom_pp_line.length():
            geom_eq = geom_pp_line.interpolate(current_distance)
            dist_a = math.sqrt(geom_eq.asPoint().sqrDist(p_a))
            buffer_ = geom_eq.buffer(dist_a,50)
            feat = self.intersect_func(buffer_,geom_eq,list_line_geom_a,list_line_geom_b)
            current_distance = current_distance + self.intv
            dist_mid_a = self.distanceFromPoint(mid_e,p_a)
            dist_mid_b = self.distanceFromPoint(mid_e,p_b)
            if feat!=0 and feat.geometry().asPoint()!=p_a and feat.geometry().asPoint()!=p_b:
                dist_mid_f = self.distanceFromPoint(mid_e,feat.geometry().asPoint())
                if (feat['ket']=="A") and (dist_mid_f < dist_mid_a):
                    break
                elif (feat['ket']=="B") and (dist_mid_f < dist_mid_b):
                    break
                else:
                    continue
            else:
                continue
        else:
            stop_ = True
        return geom_eq,feat,stop_,buffer_

    def intersect_func(self, buff_, geom_eq, list_line_geom_a,list_line_geom_b):
        list_intrs_feat = []
        flds = QgsFields()
        ket = QgsField("ket",QVariant.String)
        flds.append(ket)
        for geom_line in list_line_geom_a:
            list_intrs_a = geom_line.intersection(buff_).asGeometryCollection()
            for line in list_intrs_a:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.point_in_line(geom_eq.asPoint(),[line])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["A"])
                list_intrs_feat.append(feat)
        for geom_line in list_line_geom_b:
            list_intrs_b = geom_line.intersection(buff_).asGeometryCollection()
            for line in list_intrs_b:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.point_in_line(geom_eq.asPoint(),[line])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["B"])
                list_intrs_feat.append(feat)
        if len(list_intrs_feat)!=0:
            f = self.nearestFeat(geom_eq.asPoint(),list_intrs_feat)
        else:
            f=0
        return f

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

    def run(self,p_start_a,p_start_b,p_end_a,p_end_b):
        #self.iface.legendInterface().addGroup("creation line")
        p_mid_s = self.find_mid(p_start_a,p_start_b)
        p_mid_e = self.find_mid(p_end_a,p_end_b)
        #-------------------------------------
        p_iter_a = p_start_a
        p_iter_b = p_start_b
        dist = self.distanceFromPoint(p_mid_s,p_mid_e)
        geom_pp_line = self.perpendicular_line(dist,p_start_a,p_start_b,p_mid_e)
        list_eq_geom = []
        list_c_line = []
        eq_geom, r_feat, stop_ ,buffs= self.iter_point(p_start_a,p_start_b,p_mid_e,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
        while stop_ == False:
            #self.addLine(buffs.convertToType(1),self.crs)
            if r_feat['ket']=="A":
                p_iter_a = r_feat.geometry().asPoint()
                #print "next point is A"
            elif r_feat['ket']=="B":
                p_iter_b = r_feat.geometry().asPoint()
                #print "next point is B"
            eq_point = eq_geom.asPoint()
            r_point = r_feat.geometry().asPoint()
            c_line = QgsGeometry().fromMultiPolyline([[eq_point,p_iter_a],[eq_point,p_iter_b],[eq_point,r_point]])
            list_c_line.append(c_line)
            list_eq_geom.append(eq_geom)
            dist = self.distanceFromPoint(eq_geom.asPoint(),p_mid_e)
            geom_pp_line = self.perpendicular_line(dist,p_iter_a,p_iter_b,p_mid_e)
            eq_geom, r_feat, stop_,buffs = self.iter_point(p_iter_a,p_iter_b,p_mid_e,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
            #self.addLine(geom_pp_line,self.crs)
        else:
            print "stop is true"
        return list_eq_geom,list_c_line
    #--------------------------------------------------------------
    def addLine(self,line_geom,crs):
        line_layer = QgsVectorLayer("LineString?crs="+crs, "Line Result", "memory")
        line_layer_prov = line_layer.dataProvider()
        line_feat = QgsFeature()
        line_feat.setGeometry(line_geom)
        line_layer_prov.addFeatures([line_feat])
        #return line_layer
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)
        self.iface.legendInterface().moveLayer(line_layer,0)

    def addLine_GList(self,geom_list,crs):
        line_list = []
        for i in geom_list:
            feat = QgsFeature()
            feat.setGeometry(i)
            line_list.append(feat)
        line_layer = QgsVectorLayer("LineString?crs="+crs, "Construction Line", "memory")
        prov_ = line_layer.dataProvider()
        prov_.addFeatures(line_list)
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)

    def addPointL(self,list_point_geom,crs):
        point_layer = QgsVectorLayer("Point?crs="+crs,"Point","memory")
        point_layer_prov = point_layer.dataProvider()
        list_feat = []
        for geom in list_point_geom:
            point_feat = QgsFeature()
            point_feat.setGeometry(geom)
            list_feat.append(point_feat)
        point_layer_prov.addFeatures(list_feat)
        #QgsMapLayerRegistry.instance().addMapLayer(point_layer)
        return point_layer

    def pointsToLine(self,p_layer,crs):
        #ft_list=[]
        #for f in point_layer.getFeatures():
        #    ft_list.append(f)
        ft_list=[]
        for p in p_layer.getFeatures():
            ft_list.append(p)
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
        line_layer = QgsVectorLayer("LineString?crs="+crs, "Line Result", "memory")
        line_layer_prov = line_layer.dataProvider()
        feat = QgsFeature()
        line_geom = QgsGeometry.fromPolyline(res_list)
        feat.setGeometry(line_geom)
        line_layer_prov.addFeatures([feat])
        QgsMapLayerRegistry.instance().addMapLayer(line_layer)
"""
claim_dist = 1500
intv = 10
p_start_a = QgsPoint(377.103,1270.09)
p_start_b= QgsPoint(2694.81,907.607)
p_end = QgsPoint(1321.42,274.379)
"""
from qgis.core import *
from PyQt4.QtCore import QVariant
import math

class AdjacentLibrary(object):
    def __init__(self,list_line_geom_a,list_line_geom_b,claim_dist,intv):
        self.claim_dist = claim_dist
        self.intv = intv
        self.list_line_geom_a = list_line_geom_a
        self.list_line_geom_b = list_line_geom_b

    def pointinline(self, point, list_line_geom):
        result = {}
        for line_geom in list_line_geom:
            dist,p,int = line_geom.closestSegmentWithContext(point)
            result[p]=dist
        nearest = min(result, key=result.get)
        return nearest

    def nearestFeat(self,point,feat_list):
        currentDistance = 9999999
        nearest = QgsPoint()
        for p in feat_list:
            p_point = p.geometry().asPoint()
            distance = math.sqrt(point.sqrDist(p_point))
            if distance<currentDistance:
                currentDistance = distance
                nearest = p
        return nearest

    def findMid(self, pt_a, pt_b):
        xa = pt_a.x()
        ya = pt_a.y()
        xb = pt_b.x()
        yb = pt_b.y()
        xm = xa - (xa-xb)/2
        ym = ya - (ya-yb)/2
        m = QgsPoint(xm,ym)
        return m

    def intersectFunction(self, buff_,eq_geom,list_lineGeom_a,list_lineGeom_b):
        #buff_line = buff_.convertToType(1)
        list_intrsFeat=[]
        flds = QgsFields()
        ket = QgsField("ket",QVariant.String)
        flds.append(ket)
        for lineGeom in list_lineGeom_a:
            intrs_a = lineGeom.intersection(buff_).asMultiPolyline()
            for line_a in intrs_a:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.pointinline(eq_geom.asPoint(),[QgsGeometry().fromPolyline(line_a)])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["A"])
                list_intrsFeat.append(feat)
        for lineGeom in list_lineGeom_b:
            intrs_b = lineGeom.intersection(buff_).asGeometryCollection()
            for i in intrs_b:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.pointinline(eq_geom.asPoint(),[i])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["B"])
                list_intrsFeat.append(feat)
        if len(list_intrsFeat)!=0:
            f = self.nearestFeat(eq_geom.asPoint(),list_intrsFeat)
        else:
            f=0
        return f

    def iterPoint(self,p_iter_a,p_iter_b,list_lineGeom_a,list_lineGeom_b, pp_line_geom):
        current_dist = 0
        eq_geom = QgsGeometry()
        feat = QgsFeature()
        stop_ = False
        while current_dist<=pp_line_geom.length():
            eq_geom = pp_line_geom.interpolate(current_dist)
            dist_a = math.sqrt(eq_geom.asPoint().sqrDist(p_iter_a))
            buff_ = eq_geom.buffer(dist_a,25)
            feat = self.intersectFunction(buff_,eq_geom,list_lineGeom_a,list_lineGeom_b)
            current_dist= current_dist + self.intv
            if feat != 0 and feat.geometry().asPoint()!=p_iter_a and feat.geometry().asPoint()!=p_iter_b:
                break
            else:
                continue
        else:
            stop_ = True
        return eq_geom,feat,stop_

    def ppPoint(self, grad_, reverse, mid, dist, az):
        #reverse == 0 if false/not reversed
        #reverse == 1 if true/reversed
        xP = mid.x()
        yP = mid.y()
        if grad_>0:
            if reverse==1:
                xP = mid.x()+dist*math.cos(math.radians(az))
                yP = mid.y()+dist*math.sin(math.radians(az))
            elif reverse==0:
                xP = mid.x()-dist*math.cos(math.radians(az))
                yP = mid.y()-dist*math.sin(math.radians(az))
        elif grad_<0:
            if reverse==1:
                xP = mid.x()+dist*math.cos(math.radians(az))
                yP = mid.y()-dist*math.sin(math.radians(az))
            elif reverse==0:
                xP = mid.x()-dist*math.cos(math.radians(az))
                yP = mid.y()+dist*math.sin(math.radians(az))
        elif grad == 0:
            if reverse==1:
                xP = mid.x()
                yP = mid.y()-dist
            elif reverse==0:
                xP = mid.x()
                yP = mid.y()+dist
        else:
            if reverse==1:
                xP = mid.x()+dist
                yP = mid.y()
            elif reverse==0:
                xP = mid.x()-dist
                yP = mid.y()
        p = QgsPoint(xP,yP)
        return p

    def something(self,p_start_a,p_start_b,p_end):
        p_iter_a = p_start_a
        p_iter_b = p_start_b
        p_mid = self.findMid(p_start_a,p_start_b)
        az = p_start_a.azimuth(p_start_b)
        g_line_base = QgsGeometry.fromPolyline([p_start_a,p_start_b])
        grad_ = (p_start_b.y()-p_start_a.y())/(p_start_b.x()-p_start_a.x())
        g_end = QgsGeometry().fromPoint(p_end)
        buff_base = g_end.buffer(self.claim_dist,50)
        if g_line_base.intersects(buff_base):
            reverse = 0
            p_base = self.ppPoint(grad_,reverse,p_mid,self.claim_dist,az)
            g_ppline_base = QgsGeometry().fromPolyline([p_base,p_mid])
            buff_line = buff_base.convertToType(1)
            pp = g_ppline_base.intersection(buff_line).asPoint()
            geom_ppline = QgsGeometry.fromPolyline([pp,p_mid])
        else:
            reverse = 1
            p_base = self.ppPoint(grad_,reverse,p_mid,self.claim_dist,az)
            g_ppline_base = QgsGeometry().fromPolyline([p_mid,p_base])
            buff_line = buff_base.convertToType(1)
            pp = g_ppline_base.intersection(buff_line).asPoint()
            geom_ppline = QgsGeometry.fromPolyline([p_mid,pp])
        list_eq_geom = []
        eq_geom, r_feat, stop_ = self.iterPoint(p_start_a,p_start_b,self.list_line_geom_a,self.list_line_geom_b, geom_ppline)
        while stop_==False:
            #addLine(geom_ppline,crs)
            #addPolygon(buffer_,crs)
            if r_feat['ket']=="A":
                p_iter_a = r_feat.geometry().asPoint()
                print "next point is A"
            elif r_feat['ket']=="B":
                p_iter_b = r_feat.geometry().asPoint()
                print "next point is B"
            list_eq_geom.append(eq_geom)
            m = self.findMid(p_iter_a,p_iter_b)
            if reverse == 0:
                geom_ppline = QgsGeometry().fromPolyline([eq_geom.asPoint(),m])
            else:
                geom_ppline = QgsGeometry().fromPolyline([m,eq_geom.asPoint()])
            eq_geom, r_feat, stop_ = self.iterPoint(p_iter_a,p_iter_b,self.list_line_geom_a,self.list_line_geom_b, geom_ppline)
        else:
            print "stop is true"
        return list_eq_geom
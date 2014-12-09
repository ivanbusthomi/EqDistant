from qgis.core import *
from PyQt4.QtCore import QVariant
import math

class AdjacentLibrary(object):
    def __init__(self,line_layer_a,line_layer_b,claim_dist,intv):
        self.claim_dist = claim_dist
        self.intv = intv
        self.line_layer_a = line_layer_a
        self.line_layer_b = line_layer_b
        self.list_eq_geom = []

    def findMid(self,pt_a,pt_b):
        xa = pt_a.x()
        ya = pt_a.y()
        xb = pt_b.x()
        yb = pt_b.y()
        xm = xa - (xa-xb)/2
        ym = ya - (ya-yb)/2
        m = QgsPoint(xm,ym)
        return m

    def ppPoint(self,grad_, reverse, mid, dist, az):
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

    def intersectFunction(self,buff_,eq_geom,list_lineGeom_a,list_lineGeom_b):
        #buff_line = buff_.convertToType(1)
        list_intrsFeat=[]
        flds = QgsFields()
        ket = QgsField("ket",QVariant.String)
        flds.append(ket)
        for lineGeom in list_lineGeom_a:
            intrs_a = lineGeom.intersection(buff_).asGeometryCollection()
            for i  in intrs_a:
                feat = QgsFeature()
                feat.setFields(flds)
                n = pointinline(eq_geom.asPoint(),i)
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["A"])
                list_intrsFeat.append(feat)
        for lineGeom in list_lineGeom_b:
            intrs_b = lineGeom.intersection(buff_).asGeometryCollection()
            for i in intrs_b:
                feat = QgsFeature()
                feat.setFields(flds)
                n = pointinline(eq_geom.asPoint(),i)
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["B"])
                list_intrsFeat.append(feat)
        if len(list_intrsFeat)!=0:
            f = nearestFeat(eq_geom.asPoint(),list_intrsFeat)
        else:
            f=0
        return f

    def iterPoint(self, p_iter_a,p_iter_b,list_lineGeom_a,list_lineGeom_b, pp_line_geom):
        current_dist = 0
        eq_geom = QgsGeometry()
        feat = QgsFeature()
        stop_ = False
        while current_dist<=pp_line_geom.length():
            eq_geom = pp_line_geom.interpolate(current_dist)
            dist_a = math.sqrt(eq_geom.asPoint().sqrDist(p_iter_a))
            buff_ = eq_geom.buffer(dist_a,25)
            feat = self.intersectFunction(buff_,eq_geom,list_lineGeom_a,list_lineGeom_b)
            current_dist+=self.intv
            if feat != 0 and feat.geometry().asPoint()!=p_iter_a and feat.geometry().asPoint()!=p_iter_b:
                break
            else:
                continue
        else:
            stop_ = True
        return eq_geom,feat,stop_

    def deploy(self,p_start_a,p_start_b,p_end):
        p_iter_a = p_start_a
        p_iter_b = p_start_b
        list_lineGeom_a = []
        list_lineGeom_b = []
        for i in self.line_layer_a.getFeatures():list_lineGeom_a.append(i.geometry())
        for i in self.line_layer_b.getFeatures():list_lineGeom_b.append(i.geometry())
        # -----------------------------------
        # garis tegak lurus utama
        # -----------------------------------
        p_mid = self.findMid(p_start_a,p_start_b)       # titik tengah titik awal
        az = p_start_a.azimuth(p_start_b)               # azimut titik awal (azimuth AB)
        g_line_base = QgsGeometry().fromPolyline([p_start_a,p_start_b])       # garis hubung titik awal
        grad_ = (p_start_b.y()-p_start_a.y())/(p_start_b.x()-p_start_a.x()) # gradien garis g_line_base
        # titik awal garis batas ditentukan dari nilai klaim garis batas yang diinput pengguna.
        # nilai klaim tersebut digunakan untuk menarik buffer dari titik p_end
        g_end = QgsGeometry().fromPoint(p_end)
        buff_base = g_end.buffer(self.claim_dist,50)
        buff_line = buff_base.convertToType(1)
        if g_line_base.intersects(buff_base):
            reverse = 0
            p_base = self.ppPoint(grad_,reverse,p_mid,self.claim_dist,az)
            g_ppline_base = QgsGeometry().fromPolyline([p_base,p_mid])
            pp = g_ppline_base.intersection(buff_line).asPoint()
            geom_ppline = QgsGeometry().fromPolyline([pp,p_mid])
        else:
            reverse = 1
            p_base = self.ppPoint(grad_,reverse,p_mid,self.claim_dist,az)
            p_base_rev = self.ppPoint(grad_,reverse,p_mid,-(self.claim_dist),az)
            g_ppline_base = QgsGeometry().fromPolyline([p_mid,p_base])
            pp = g_ppline_base.intersection(buff_line).asPoint()
            geom_ppline = QgsGeometry().fromPolyline([pp, p_base_rev])
        list_eq_geom = []
        eq_geom, r_feat, stop_ = self.iterPoint(p_iter_a,p_iter_b,list_lineGeom_a,list_lineGeom_b, geom_ppline)
        while stop_ == False:
            if r_feat['ket']=="A":
                p_iter_a = r_feat.geometry().asPoint()
            elif r_feat['ket']=="B":
                p_iter_b = r_feat.geometry().asPoint()
            else:
                break
            list_eq_geom.append(eq_geom)
            m = self.findMid(p_iter_a,p_iter_b)
            if reverse == 0:
                geom_ppline = QgsGeometry().fromPolyline([eq_geom.asPoint(),m])
            else:
                geom_ppline = QgsGeometry().fromPolyline([m,eq_geom.asPoint()])
            eq_geom, r_feat, stop_ = iterPoint(p_iter_a,p_iter_b,list_lineGeom_a,list_lineGeom_b, geom_ppline,intv)
        return list_eq_geom
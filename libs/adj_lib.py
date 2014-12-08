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

    def deploy(self,p_start_a,p_start_b,p_end):
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
        print reverse
        return geom_ppline
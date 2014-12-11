from qgis.core import *
from PyQt4.QtCore import QVariant
import math


class OppositeLibrary(object):
    def __init__(self, list_line_geom_a, list_line_geom_b, claim_dist, intv):
        self.list_line_geom_a = list_line_geom_a
        self.list_line_geom_b = list_line_geom_b
        self.claim_dist = claim_dist
        self.intv = intv

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
                #kanan
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                print az, side
            elif side < 0:
                #kiri
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                print az, side
            else:
                print "side value 1 error"
        elif az>90 and az<180:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                print az, side
            else:
                print "side value 2 error"
        elif az<0 and az>-90:
            if side > 0:
                #kanan
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                print az, side
            elif side < 0:
                #kiri
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                print az, side
            else:
                print "side value 3 error"
        elif az<-90 and az>-180:
            if side > 0:
                px = xm+dist*math.cos(math.radians(az))
                py = ym-dist*math.sin(math.radians(az))
                print az, side
            elif side < 0:
                px = xm-dist*math.cos(math.radians(az))
                py = ym+dist*math.sin(math.radians(az))
                print az, side
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
        return geom_eq,feat,stop_

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
        p_mid_s = self.find_mid(p_start_a,p_start_b)
        p_mid_e = self.find_mid(p_end_a,p_end_b)
        #-------------------------------------
        p_iter_a = p_start_a
        p_iter_b = p_start_b
        dist = self.distanceFromPoint(p_mid_s,p_mid_e)
        geom_pp_line = self.perpendicular_line(dist,p_start_a,p_start_b,p_mid_e)
        list_eq_geom = []
        eq_geom, r_feat, stop_ = self.iter_point(p_start_a,p_start_b,mid_e,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
        while stop_ == False:
            if r_feat['ket']=="A":
                p_iter_a = r_feat.geometry().asPoint()
                print "next point is A"
            elif r_feat['ket']=="B":
                p_iter_b = r_feat.geometry().asPoint()
                print "next point is B"
            list_eq_geom.append(eq_geom)
            dist = self.distanceFromPoint(eq_geom.asPoint(),p_mid_e)
            geom_pp_line = self.perpendicular_line(dist,p_iter_a,p_iter_b,p_mid_e)
            eq_geom, r_feat, stop_ = self.iter_point(p_iter_a,p_iter_b,mid_e,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
        else:
            print "stop is true"
        return list_eq_geom
    #--------------------------------------------------------------

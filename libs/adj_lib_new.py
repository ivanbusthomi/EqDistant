from qgis.core import *
from qgis.gui import QgsLegendInterface
from PyQt4.QtCore import QVariant
#from lay_lib import LayerOperation
import math

class AdjacentLibrary(object):
    def __init__(self,iface,list_line_geom_a,list_line_geom_b,claim_dist,intv,crs):
        self.iface=iface
        self.claim_dist = claim_dist
        self.intv = intv
        self.list_line_geom_a = list_line_geom_a
        self.list_line_geom_b = list_line_geom_b
        self.crs = crs
        #self.lay_op = LayerOperation()

    def findMid(self, pt_a, pt_b):
        xa = pt_a.x()
        ya = pt_a.y()
        xb = pt_b.x()
        yb = pt_b.y()
        xm = xa - (xa-xb)/2
        ym = ya - (ya-yb)/2
        m = QgsPoint(xm,ym)
        return m

    def pointinline(self, point, list_line_geom):
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
        az_ = pa.azimuth(pb)
        if az_>0:
            az = az_
        else:
            az = 360+az_
        return az

    def perpendicular_line(self, pa, pb, pp, p_end):
        p_mid = self.findMid(pa,pb)
        side_pp = self.find_side(pa,pb,pp)
        side_end = self.find_side(pa,pb,p_end)
        d_a = math.sqrt(pp.sqrDist(p_mid))
        d_b = math.sqrt(pp.sqrDist(p_end))
        c =(side_pp/side_end)
        if c<0:
            dx_a = p_mid.x()-pp.x()
            dy_a = p_mid.y()-pp.y()
        else:# (side_pp/side_end)>0:
            dx_a = pp.x()- p_mid.x()
            dy_a = pp.y()- p_mid.y()
        dx_b = dx_a*d_b/d_a
        dy_b = dy_a*d_b/d_a
        if c<0:
            x_pp_b = pp.x()+dx_b
            y_pp_b = pp.y()+dy_b
        else:
            x_pp_b = p_mid.x()+dx_b
            y_pp_b = p_mid.y()+dy_b
        pp_b = QgsPoint(x_pp_b,y_pp_b)
        geom_pp_line = QgsGeometry().fromPolyline([pp,pp_b])
        return geom_pp_line

    def iterPoint(self,p_iter_a,p_iter_b,p_end,list_lineGeom_a,list_lineGeom_b, pp_line_geom):
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
            #print current_dist, pp_line_geom.length()
            dist_mid_a = math.sqrt(p_iter_a.sqrDist(p_end))
            dist_mid_b = math.sqrt(p_iter_b.sqrDist(p_end))
            if feat != 0 and feat.geometry().asPoint()!=p_iter_a and feat.geometry().asPoint()!=p_iter_b:
                f_point = feat.geometry().asPoint()
                dist_mid_f = math.sqrt(f_point.sqrDist(p_end))
                if feat['ket']=="A" and dist_mid_f<dist_mid_a:
                    break
                elif feat['ket']=="B" and dist_mid_f<dist_mid_b:
                    break
                else:
                    continue
            else:
                continue
        else:
            stop_ = True
        return eq_geom,feat,stop_

    def intersectFunction(self, buff_,eq_geom,list_lineGeom_a,list_lineGeom_b):
        #buff_line = buff_.convertToType(1)
        list_intrsFeat=[]
        flds = QgsFields()
        ket = QgsField("ket",QVariant.String)
        flds.append(ket)
        for lineGeom in list_lineGeom_a:
            intrs_a = lineGeom.intersection(buff_).asGeometryCollection()
            for line_a in intrs_a:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.pointinline(eq_geom.asPoint(),[line_a])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["A"])
                list_intrsFeat.append(feat)
        for lineGeom in list_lineGeom_b:
            intrs_b = lineGeom.intersection(buff_).asGeometryCollection()
            for line_b in intrs_b:
                feat = QgsFeature()
                feat.setFields(flds)
                n = self.pointinline(eq_geom.asPoint(),[line_b])
                feat.setGeometry(QgsGeometry().fromPoint(n))
                feat.setAttributes(["B"])
                list_intrsFeat.append(feat)
        if len(list_intrsFeat)!=0:
            f = self.nearestFeat(eq_geom.asPoint(),list_intrsFeat)
        else:
            f=0
        return f

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

    def delta_(self,az,side):
        if az>0 and az<=90:         # 1st Quadrant
            if side<0:
                dx = -self.claim_dist*math.cos(math.radians(az))
                dy = self.claim_dist*math.sin(math.radians(az))
            else:
                dx = self.claim_dist*math.cos(math.radians(az))
                dy = -self.claim_dist*math.sin(math.radians(az))
        elif az>90 and az<=180:     # 2nd Quadrant
            if side<0:
                dx = -self.claim_dist*math.cos(math.radians(az))
                dy = self.claim_dist*math.sin(math.radians(az))
            else:
                dx = self.claim_dist*math.cos(math.radians(az))
                dy = -self.claim_dist*math.sin(math.radians(az))
        elif az>180 and az<=270:    # 3rd Quadrant
            if side > 0:
                dx = self.claim_dist*math.cos(math.radians(az))
                dy = -self.claim_dist*math.sin(math.radians(az))
            else:
                dx = -self.claim_dist*math.cos(math.radians(az))
                dy = self.claim_dist*math.sin(math.radians(az))
        elif az>270 and az<=360:    # 4th Quadrant
            if side > 0:
                dx = self.claim_dist*math.cos(math.radians(az))
                dy = -self.claim_dist*math.sin(math.radians(az))
            else:
                dx = -self.claim_dist*math.cos(math.radians(az))
                dy = self.claim_dist*math.sin(math.radians(az))
        else:
            raise ValueError("azimuth error")
        return dx,dy

    def run(self,p_start_a,p_start_b,p_end):
        self.iface.legendInterface().addGroup("creation_line")
        p_mid = self.findMid(p_start_a,p_start_b)
        az = self.azm(p_start_a,p_start_b)
        side_end =self.find_side(p_start_a,p_start_b,p_end)
        side = -side_end                # reverse
        dx,dy = self.delta_(az,side)
        xp = p_mid.x()+ dx
        yp = p_mid.y()+ dy
        pp = QgsPoint(xp,yp)    # perpendicular point
        geom_pp_line = self.perpendicular_line(p_start_a,p_start_b,pp,p_end) #perpendicular line to end_point

        #------------------------ iteration
        p_iter_a = p_start_a
        p_iter_b = p_start_b
        list_eq_geom = []
        list_c_line_geom = []
        eq_geom, r_feat, stop_ = self.iterPoint(p_iter_a,p_iter_b,p_end,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
        while stop_ == False:
            #create control line
            eq_point = eq_geom.asPoint()
            r_point = r_feat.geometry().asPoint()
            cline_geom = QgsGeometry.fromMultiPolyline([[eq_point,p_iter_a],[eq_point,p_iter_b],[eq_point,r_point]])
            list_c_line_geom.append(cline_geom)
            if r_feat['ket']=="A":
                p_iter_a = r_point
                #print "next point is A : "+str(p_i
            elif r_feat['ket']=="B":
                p_iter_b = r_point
                #print "next point is B : "+str(p_iter_b)
            list_eq_geom.append(eq_geom)
            geom_pp_line = self.perpendicular_line(p_iter_a,p_iter_b,eq_point,p_end)
            eq_geom, r_feat, stop_= self.iterPoint(p_iter_a,p_iter_b,p_end,self.list_line_geom_a,self.list_line_geom_b,geom_pp_line)
            self.addLine(geom_pp_line,self.crs)
        else:
            pass
        #print len(list_eq_geom)
        self.iface.legendInterface().removeGroup(0)
        return list_eq_geom,list_c_line_geom

    #--------new run

    def addPointG(self,point_geom,crs):
        point_layer = QgsVectorLayer("Point?crs="+crs,"Point","memory")
        point_layer_prov = point_layer.dataProvider()
        point_feat = QgsFeature()
        point_feat.setGeometry(point_geom)
        point_layer_prov.addFeatures([point_feat])
        QgsMapLayerRegistry.instance().addMapLayer(point_layer)
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

    # the methods below might be unimportant
    def addPolygon(self, poly_geom,crs):
        poly_layer = QgsVectorLayer("Polygon?crs="+crs, "Polygon Result", "memory")
        poly_layer_prov =poly_layer.dataProvider()
        poly_feat = QgsFeature()
        poly_feat.setGeometry(poly_geom)
        poly_layer_prov.addFeatures([poly_feat])
        QgsMapLayerRegistry.instance().addMapLayer(poly_layer)

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

    def slope(self, pa, pb):
        xa,ya = pa.x(),pa.y()
        xb,yb = pb.x(),pb.y()
        m = (yb-ya)/(xb-xa)
        return m


    def test(self,p_start_a,p_start_b,p_end):
        p_mid = self.findMid(p_start_a,p_start_b)
        az = self.azm(p_start_a,p_start_b)
        side_end =self.find_side(p_start_a,p_start_b,p_end)
        side = -side_end                # reverse
        dx,dy = self.delta_(az,side)
        xp = p_mid.x()+ dx
        yp = p_mid.y()+ dy
        pp = QgsPoint(xp,yp)    # perpendicular point
        geom_pp_line = self.perpendicular_line(p_start_a,p_start_b,pp,p_end)
        self.addLine(geom_pp_line,self.crs)
from qgis.core import *
from PyQt4.QtCore import QVariant
import math

class OppositeLibrary(object):
    def __init__(self,point_layer_a,point_layer_b,intv):
        self.point_layer_a = point_layer_a
        self.point_layer_b = point_layer_b
        #____________________________________________________
        self.intv = intv
        self.list_equi_geom = []
        self.list_third_feat = []
    def findMid(self,pt_a,pt_b):
        xa = pt_a.x()
        ya = pt_a.y()
        xb = pt_b.x()
        yb = pt_b.y()
        xm = xa - (xa-xb)/2
        ym = ya - (ya-yb)/2
        m = QgsPoint(xm,ym)
        return m
    def circumCenter(self,point_a,point_b,point_c):
        xA=point_a.x()
        yA=point_a.y()
        xB=point_b.x()
        yB=point_b.y()
        xC=point_c.x()
        yC=point_c.y()
        a2 = pow(xA,2)+pow(yA,2)
        b2 = pow(xB,2)+pow(yB,2)
        c2 = pow(xC,2)+pow(yC,2)
        #------------------
        const = 2*(xA*(yB-yC)+xB*(yC-yA)+xC*(yA-yB))
        xO = (a2*(yB-yC)+b2*(yC-yA)+c2*(yA-yB))/const
        yO = (a2*(xC-xB)+b2*(xA-xC)+c2*(xB-xA))/const
        point_o = QgsPoint(xO,yO)
        #line construction
        geom_line_a = QgsGeometry.fromPolyline([point_a,point_o])
        geom_line_b = QgsGeometry.fromPolyline([point_b,point_o])
        geom_line_c = QgsGeometry.fromPolyline([point_c,point_o])
        list_geom = [geom_line_a,geom_line_b,geom_line_c]
        con_line = []
        for geom in list_geom:
            feat = QgsFeature()
            feat.setGeometry(geom)
            con_line.append(feat)
        return point_o,con_line
    def direction(self, point_a,point_b,end_point_a,end_point_b):
        mid_start = self.findMid(point_a,point_b)
        mid_end = self.findMid(end_point_a,end_point_b)
        midpoint_start = QgsPoint(mid_start[0],mid_start[1])
        midpoint_end = QgsPoint(mid_end[0],mid_end[1])
        #dir_=0
        if midpoint_start.x()<midpoint_end.x():
            if midpoint_start.y()<midpoint_end.y():
                dir_=1
            else:
            #elif midpoint_start.y()>midpoint_end.y():
                dir_=2
        else:
        #elif midpoint_start.x()>midpoint_end.x():
            if midpoint_start.y()<midpoint_end.y():
                dir_=3
            else:
            #elif midpoint_start.y()>midpoint_end.y():
                dir_=4
        dy = midpoint_end.y()-midpoint_start.y()
        dx = midpoint_end.x()-midpoint_start.x()
        if dx == 0:
            grad_ = 5
        else:
            grad_ = dy/dx
        return dir_, grad_
    #takes point layers from __init__
    def perpendicularLine(self,point_a,point_b,dir_):
        xA = point_a.x()
        yA = point_a.y()
        xB = point_b.x()
        yB = point_b.y()
        midpoint = self.findMid(point_a,point_b)
        xM = midpoint.x()
        yM = midpoint.y()
        extent_a = self.point_layer_a.extent()
        extent_b = self.point_layer_b.extent()
        # find xmax and xmin values
        if extent_a.xMaximum() > extent_b.xMaximum():
            xmax = extent_a.xMaximum()
        else:
            xmax = extent_b.xMaximum()
        if extent_a.xMinimum() < extent_b.xMinimum():
            xmin = extent_a.xMinimum()
        else:
            xmin = extent_b.xMinimum()
        # find ymax and ymin values
        if extent_a.yMaximum() > extent_b.yMaximum():
            ymax = extent_a.yMaximum()
        else:
            ymax = extent_b.yMaximum()
        if extent_a.yMinimum() < extent_b.yMinimum():
            ymin = extent_a.yMinimum()
        else:
            ymin = extent_b.yMinimum()
        # main equation
        p = xB - xA
        q = yB - yA
        r = xM - xA
        s = yM - yA
        d2 = point_a.sqrDist(point_b)
        # line gradient is used to determine the length of the line that will be created
        if p == 0:
            # gradient line 1 = undefined. line 1 is vertical, line 2 is horizontal
            gradient2 = 0
            u = 0
        elif q == 0:
            # line 1 is horizontal, line 2 is vertical
            gradient2 = 2
            u = r/p
        else:
            gradient1 = q/p
            gradient2 = -1/gradient1
            u = r/p
        # ---------------------------------
        if dir_ == 1:                  # line direction is up-right
            if math.pow(gradient2,2)>1:
                y3 = ymax
                x3 = ((-q)*y3 + p*xA + q*yA + u*d2) / p
            else:# math.pow(gradient2,2)<1:
                x3 = xmax
                y3 = ((-p)*x3 + p*xA + q*yA + u*d2) / q
        elif dir_ == 2:                  # line direction is down-right
            if math.pow(gradient2,2)>1:
                y3 = ymin
                x3 = ((-q)*y3 + p*xA + q*yA + u*d2) / p
            else:# math.pow(gradient2,2)<1:
                x3 = xmax
                y3 = ((-p)*x3 + p*xA + q*yA + u*d2) / q
        elif dir_ == 3:                  # line direction is up-left
            if math.pow(gradient2,2)>1:
                y3 = ymax
                x3 = ((-q)*y3 + p*xA + q*yA + u*d2) / p
            else:# math.pow(gradient2,2)<1:
                x3 = xmin
                y3 = ((-p)*x3 + p*xA + q*yA + u*d2) / q
        else:# dir_ == 4:                  # line direction is down-left
            if math.pow(gradient2,2)>1:
                y3 = ymin
                x3 = ((-q)*y3 + p*xA + q*yA + u*d2) / p
            else:# math.pow(gradient2,2)<1:
                x3 = xmin
                y3 = ((-p)*x3 + p*xA + q*yA + u*d2) / q
        # -----------------------------------------
        ppd_point = QgsPoint(x3,y3)
        ppd_line = QgsGeometry.fromPolyline([midpoint,ppd_point])
        #print dir_
        return ppd_line
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
    def distanceFromPoint(self,point_a,point_b):
        return math.sqrt(point_a.sqrDist(point_b))
    def intersectionCheck(self,buffer_,sp_idx_a,sp_idx_b,f_dict_a,f_dict_b,point_a,point_b,dir_,grad_):
        list_of_result = []
        #___________________________________________________
        ids_a =sp_idx_a.intersects(buffer_.boundingBox())
        for id in ids_a:
            f = f_dict_a[id]
            if f.geometry().intersects(buffer_):
                if dir_ == 1:
                    if grad_ >=1 and f.geometry().asPoint().y()>point_a.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()>point_a.x():
                        list_of_result.append(f)
                elif dir_ == 2 :
                    if grad_ >=1 and f.geometry().asPoint().y()<point_a.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()>point_a.x():
                        list_of_result.append(f)
                elif dir_ == 3 :
                    if grad_ >=1 and f.geometry().asPoint().y()>point_a.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()<point_a.x():
                        list_of_result.append(f)
                elif dir_ == 4 :
                    if grad_ >=1 and f.geometry().asPoint().y()<point_a.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()<point_a.x():
                        list_of_result.append(f)
        #___________________________________________________
        ids_b =sp_idx_b.intersects(buffer_.boundingBox())
        for id in ids_b:
            f = f_dict_b[id]
            if f.geometry().intersects(buffer_):
                if dir_ == 1:
                    if grad_ >=1 and f.geometry().asPoint().y()>point_b.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()>point_b.x():
                        list_of_result.append(f)
                elif dir_ == 2 :
                    if grad_ >=1 and f.geometry().asPoint().y()<point_b.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()>point_b.x():
                        list_of_result.append(f)
                elif dir_ == 3 :
                    if grad_ >=1 and f.geometry().asPoint().y()>point_b.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()<point_b.x():
                        list_of_result.append(f)
                elif dir_ == 4 :
                    if grad_ >=1 and f.geometry().asPoint().y()<point_b.y():
                        list_of_result.append(f)
                    elif grad_ <1 and f.geometry().asPoint().x()<point_b.x():
                        list_of_result.append(f)
        return list_of_result
    def iteratePoint(self, point_a,point_b, sp_idx_a,sp_idx_b,f_dict_a,f_dict_b, pp_line_geom, dir_,grad_,itv):
        current_distance=0
        r = QgsFeature()
        buff = QgsGeometry()
        equi_geom = QgsGeometry()
        while current_distance<=pp_line_geom.length():
            stop = 0
            equi_geom = pp_line_geom.interpolate(current_distance)
            dist_a = self.distanceFromPoint(point_a, equi_geom.asPoint())
            buff = equi_geom.buffer(dist_a,15)
            res = self.intersectionCheck(buff,sp_idx_a,sp_idx_b,f_dict_a,f_dict_b,point_a,point_b,dir_,grad_)
            current_distance+=itv
            if len(res)==1:
                r = res[0]
                break
            elif len(res)>1:
                r=self.nearestFeat(equi_geom.asPoint(),res)
                break
            else:
                continue
        else:
            stop=1
        return equi_geom, r, stop, buff
    def deploy(self, f_list_a,f_list_b,start_point_a,start_point_b,end_point_a,end_point_b):
        p_iter_a = start_point_a
        p_iter_b = start_point_b
        stop = 0
        #dir_ = 0
        # Spatial index creation
        sp_idx_a = QgsSpatialIndex()
        sp_idx_b = QgsSpatialIndex()
        f_dict_a = {f.id():f for f in f_list_a}
        f_dict_b = {f.id():f for f in f_list_b}
        for feat_a in f_list_a:sp_idx_a.insertFeature(feat_a)
        for feat_b in f_list_b:sp_idx_b.insertFeature(feat_b)
        #iterate ____________________________________________________
        while stop==0 and p_iter_a!= end_point_a and p_iter_b!= end_point_b:
            dir_,grad_ = self.direction(p_iter_a,p_iter_b,end_point_a,end_point_b)
            #if dir_==0:
            #    break
            pp_line_geom = self.perpendicularLine(p_iter_a,p_iter_b,dir_)
            equi_geom, third_feat, stop,buff = self.iteratePoint(p_iter_a,p_iter_b,sp_idx_a,sp_idx_b,f_dict_a,f_dict_b,pp_line_geom,dir_,grad_,self.intv)
            #print stop,third_feat,equi_geom.asPoint()
            if stop == 0:
                third_point = third_feat.geometry().asPoint()
                if third_point!=p_iter_a and third_point!=p_iter_b:
                    self.list_equi_geom.append(equi_geom)
                    self.list_third_feat.append([p_iter_a,p_iter_b,third_point])
                    if third_feat['ket']=='A':
                        p_iter_a=third_point
                        #print "a changed"
                    elif third_feat['ket']=='B':
                        p_iter_b=third_point
                        #print "b changed"
        else:
            pass
            #print "Process completed"
        final_res = []
        construction_line = []
        for coords in self.list_third_feat:
            o,con_line = self.circumCenter(coords[0],coords[1],coords[2])
            for feat in con_line:construction_line.append(feat)
            f = QgsFeature()
            f.setGeometry(QgsGeometry.fromPoint(o))
            final_res.append(f)
        #layopt = LayerOperation()
        #layopt.addPointF(final_res)
        return final_res,construction_line

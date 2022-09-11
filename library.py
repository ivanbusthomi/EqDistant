from qgis.PyQt.QtCore import QVariant
from qgis.gui import QgsRubberBand
from qgis.core import *
from qgis.utils import iface


def interpolate_line_segment(line_segment, interpolate_interval):
    list_interpolate_point_feature = []
    interpolate_dist = 0
    while interpolate_dist < line_segment.length():
        interpolate_point = line_segment.interpolate(interpolate_dist)
        feat = QgsFeature()
        feat.setGeometry(interpolate_point)
        list_interpolate_point_feature.append(feat)
        interpolate_dist += interpolate_interval
    return list_interpolate_point_feature


def interpolate_line(list_of_line_feature, interpolate_interval):
    list_of_segment_geom = []
    list_interpolate_point_feature = []
    # print(f"Processing {len(list_of_line_feature)} feature(s)")
    # print("Breaking into line segment")
    for line_feat in list_of_line_feature:
        # print("Processing line feature")
        line_geom = line_feat.geometry()
        # check whether the line feature is multipart or not.
        if line_geom.isMultipart():
            # print("Multipart feature detected")
            line_coord = line_geom.asMultiPolyline()
            for line in line_coord:
                for index in range(len(line) - 1):
                    first_point = line[index]
                    second_point = line[index + 1]
                    segment_geom = QgsGeometry.fromPolylineXY(
                        [first_point, second_point]
                    )
                    points = interpolate_line_segment(
                        segment_geom, interpolate_interval
                    )
                    list_interpolate_point_feature += points
                last_point = QgsGeometry.fromPointXY(line[-1])
                last_point_feat = QgsFeature()
                last_point_feat.setGeometry(last_point)
                list_interpolate_point_feature.append(last_point_feat)
        else:
            # print("Singlepart feature detected")
            line_coord = line_geom.asPolyline()
            for index in range(len(line_coord) - 1):
                first_point = line_coord[index]
                second_point = line_coord[index + 1]
                segment_geom = QgsGeometry.fromPolylineXY([first_point, second_point])
                points = interpolate_line_segment(segment_geom, interpolate_interval)
                list_interpolate_point_feature += points
            last_point = QgsGeometry.fromPointXY(line_coord[-1])
            last_point_feat = QgsFeature()
            last_point_feat.setGeometry(last_point)
            list_interpolate_point_feature.append(last_point_feat)

        print("Processing line feature finished")
    print("Line segment created")

    return list_interpolate_point_feature


def line_to_point_layer_new(
    list_feat,
    crs,
    layer_name="point_layer",
    id_name="point_id",
    id_prefix="",
    filepath="memory",
    interpolate_interval=0,
):
    """Convert list of line feature into a point layer.

    Args:
        list_feat (list): List of line feature
        crs (epsg crs): crs information
        layer_name (str, optional): [description]. Defaults to "point_layer".
        id_name (str, optional): [description]. Defaults to "point_id".
        id_prefix (str, optional): [description]. Defaults to "".
        filepath (str, optional): [description]. Defaults to "memory".
        interpolate_interval (int, optional): [description]. Defaults to 0.

    Returns:
        QgsVectorLayer: Point Layer
    """
    point_layer = QgsVectorLayer("Point?crs=" + crs, layer_name, filepath)
    point_layer_pr = point_layer.dataProvider()
    point_layer_pr.addAttributes([QgsField("point_id", QVariant.String)])
    point_layer.updateFields()

    # create line segment and interpolate
    list_of_segment_geom = []
    list_point_feature = []
    point_id = 0

    list_geom = combine_geometries([feat.geometry() for feat in list_feat])

    for line_geom in list_geom:
        # line_geom = line_feat.geometry()
        # check whether geomery is multipart or not
        if line_geom.isMultipart():
            multi_line = line_geom.asMultiPolyline()
            for line_coord in multi_line:
                for index in range(len(line_coord) - 1):
                    first_point = line_coord[index]
                    if interpolate_interval > 0:
                        next_point = line_coord[index + 1]
                        segment_geom = QgsGeometry.fromPolylineXY(
                            [first_point, next_point]
                        )
                        point_feats = interpolate_line_segment(
                            segment_geom, interpolate_interval
                        )
                        for point_feat in point_feats:
                            point_feat.setAttributes([id_prefix + str(point_id)])
                            point_id += 1
                            point_layer_pr.addFeature(point_feat)
                    else:
                        point_geom = QgsGeometry.fromPointXY(first_point)
                        point_feat = QgsFeature()
                        point_feat.setGeometry(point_geom)
                        point_feat.setAttributes([id_prefix + str(point_id)])
                        point_id += 1
                        point_layer_pr.addFeature(point_feat)
                last_point = QgsGeometry.fromPointXY(line_coord[-1])
                last_point_feat = QgsFeature()
                last_point_feat.setGeometry(last_point)
                last_point_feat.setAttributes([id_prefix + str(point_id)])
                point_layer_pr.addFeature(last_point_feat)

        else:
            line_coord = line_geom.asPolyline()
            for index in range(len(line_coord) - 1):
                first_point = line_coord[index]
                if interpolate_interval > 0:
                    next_point = line_coord[index + 1]
                    segment_geom = QgsGeometry.fromPolylineXY([first_point, next_point])
                    point_feats = interpolate_line_segment(
                        segment_geom, interpolate_interval
                    )
                    for point_feat in point_feats:
                        point_feat.setAttributes([id_prefix + str(point_id)])
                        point_id += 1
                        point_layer_pr.addFeature(point_feat)
                else:
                    point_geom = QgsGeometry.fromPointXY(first_point)
                    point_feat = QgsFeature()
                    point_feat.setGeometry(point_geom)
                    point_feat.setAttributes([id_prefix + str(point_id)])
                    point_id += 1
                    point_layer_pr.addFeature(point_feat)
            last_point = QgsGeometry.fromPointXY(line_coord[-1])
            last_point_feat = QgsFeature()
            last_point_feat.setGeometry(last_point)
            last_point_feat.setAttributes([id_prefix + str(point_id)])
            point_layer_pr.addFeature(last_point_feat)

    point_layer.startEditing()
    point_layer.commitChanges()
    point_layer.updateExtents()
    return point_layer


def line_to_point_layer(
    list_feat,
    crs,
    layer_name="Point Layer",
    id_name="point_id",
    id_prefix="",
    filepath="memory",
):

    point_layer = QgsVectorLayer("Point?crs=" + crs, layer_name, filepath)
    point_layer_pr = point_layer.dataProvider()
    point_layer_pr.addAttributes([QgsField("point_id", QVariant.String)])
    point_layer.updateFields()
    # list_feat = [feat for feat in line_layer.getFeatures()]
    list_geom = [feat.geometry() for feat in list_feat]
    # create point geometry
    list_point_feat = []
    point_id = 0
    for geom in list_geom:
        if geom.isMultipart():
            for poly in geom.asMultiPolyline():
                for pt in poly:
                    point_feat = QgsFeature()
                    point_feat.setGeometry(QgsGeometry.fromPointXY(pt))
                    point_feat.setAttributes([id_prefix + str(point_id)])
                    point_id += 1
                    point_layer_pr.addFeature(point_feat)
        else:
            for point in geom.asPolyline():
                point_feat = QgsFeature()
                point_feat.setGeometry(QgsGeometry.fromPointXY(point))
                point_feat.setAttributes([id_prefix + str(point_id)])
                point_id += 1
                point_layer_pr.addFeature(point_feat)
    point_layer.startEditing()
    point_layer.commitChanges()
    point_layer.updateExtents()
    return point_layer


def combine_geometries(list_of_geometry):
    g = list_of_geometry[0]
    for geom in list_of_geometry:
        g = g.combine(geom)
    if g.isMultipart():
        list_result_geometry = [
            QgsGeometry().fromPolylineXY(geom) for geom in g.asMultiPolyline()
        ]
        # print('Geometry is multipart. there are ' + str(len(list_result_geometry)) + ' features')
    else:
        list_result_geometry = [g]
        # print('Geometry is singlepart')
    return list_result_geometry


def line_feature_list_to_layer(
    list_feat, crs, layer_name="Line Layer", id_name="line_id", filepath="memory"
):

    line_layer = QgsVectorLayer("Linestring?crs=" + crs, layer_name, filepath)
    line_layer_pr = line_layer.dataProvider()

    for feat in list_feat:
        line_layer_pr.addFeature(feat)
    line_layer.startEditing()
    line_layer.commitChanges()
    return line_layer


def merge_point_layers(point_layer_a, point_layer_b):
    crs = point_layer_a.crs().authid()
    point_layer = QgsVectorLayer("Point?crs=" + crs, "merge point_layer", "memory")
    point_layer_pr = point_layer.dataProvider()
    point_layer_pr.addAttributes(point_layer_a.fields())
    point_layer.updateFields()

    list_a = [f for f in point_layer_a.getFeatures()]
    list_b = [f for f in point_layer_b.getFeatures()]
    list_f = list_a + list_b
    point_layer_pr.addFeatures(list_f)
    point_layer.startEditing()
    point_layer.commitChanges()
    return point_layer


def create_voronoi(merged_pt_layer):
    spatial_index = QgsSpatialIndex(merged_pt_layer.getFeatures())
    list_feat = [feat for feat in merged_pt_layer.getFeatures()]
    list_point = [feat.geometry().asPoint() for feat in list_feat]

    geom_multipoint = QgsGeometry.fromMultiPointXY(list_point)
    voronoi_diagram = geom_multipoint.voronoiDiagram()
    # create voronoi layer in memory
    vd_layer = QgsVectorLayer(
        "MultiPolygon?crs=" + merged_pt_layer.crs().authid(), "Voronoi", "memory"
    )
    vd_layer_pr = vd_layer.dataProvider()
    vd_layer_pr.addAttributes(
        [QgsField("voroID", QVariant.Int), QgsField("point_id", QVariant.String)]
    )
    vd_layer.updateFields()
    vd_id = 0
    for geom in voronoi_diagram.asGeometryCollection():
        voronoi_feat = QgsFeature()
        voronoi_feat.setGeometry(geom)

        # get point ID
        intersect_idx = spatial_index.intersects(geom.boundingBox())
        req = QgsFeatureRequest().setFilterFids(intersect_idx)
        req_feat = [feat for feat in merged_pt_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().intersects(geom):
                pid = feat["point_id"]

        voronoi_feat.setAttributes([vd_id, pid])
        vd_layer_pr.addFeature(voronoi_feat)
        vd_id += 1
    vd_layer.startEditing()
    vd_layer.commitChanges()
    vd_layer.updateExtents()
    return vd_layer


def create_delaunay_triangulation(merged_pt_layer):
    spatial_index = QgsSpatialIndex(merged_pt_layer.getFeatures())
    list_feat = [feat for feat in merged_pt_layer.getFeatures()]
    list_point = [feat.geometry().asPoint() for feat in list_feat]

    geom_multipoint = QgsGeometry.fromMultiPointXY(list_point)
    delaunay_triangulation = geom_multipoint.delaunayTriangulation()

    # create delaunay triangulation layer in memory
    dt_layer = QgsVectorLayer(
        "MultiPolygon?crs=" + merged_pt_layer.crs().authid(),
        "Delaunay Triangulation",
        "memory",
    )
    dt_layer_pr = dt_layer.dataProvider()
    dt_layer_pr.addAttributes(
        [
            QgsField("delaunayID", QVariant.Int),
            QgsField("first_point", QVariant.String),
            QgsField("second_point", QVariant.String),
            QgsField("third_point", QVariant.String),
            QgsField("valid_triangle", QVariant.String),
        ]
    )
    dt_layer.updateFields()
    dt_id = 0
    for geom in delaunay_triangulation.asGeometryCollection():
        # create DT feature
        delaunay_feat = QgsFeature()
        delaunay_feat.setGeometry(geom)

        # get point ID
        point_list = []
        intersect_idx = spatial_index.intersects(geom.boundingBox())
        req = QgsFeatureRequest().setFilterFids(intersect_idx)
        req_feat = [feat for feat in merged_pt_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().touches(geom):
                point_list.append(feat)

        list_attr = []
        for point in point_list:
            list_attr.append(point["point_id"][0])
        unique_attr = list(set(list_attr))
        if len(unique_attr) > 1:
            valid_triangle = "valid"
        else:
            valid_triangle = "invalid"
        delaunay_feat.setAttributes(
            [
                dt_id,
                point_list[0]["point_id"],
                point_list[1]["point_id"],
                point_list[2]["point_id"],
                valid_triangle,
            ]
        )
        dt_layer_pr.addFeature(delaunay_feat)
        dt_id += 1
    dt_layer.startEditing()
    dt_layer.commitChanges()
    dt_layer.updateExtents()
    return dt_layer


def valid_delaunay_triangulation(dt_layer, list_feature_a, list_feature_b):
    # Valid Delaunay
    valid_delaunay_request = QgsFeatureRequest(
        QgsExpression(f"\"valid_triangle\" = 'valid'")
    )
    valid_delaunay_list = [
        feat.geometry() for feat in dt_layer.getFeatures(valid_delaunay_request)
    ]
    # create multipart
    valid_delaunay = valid_delaunay_list[0]
    for geom in valid_delaunay_list[1:]:
        valid_delaunay = valid_delaunay.combine(geom)

    valid_dt_layer = QgsVectorLayer(
        "Polygon?crs=" + dt_layer.crs().authid(), "Valid Area", "memory"
    )
    valid_dt_layer_pr = valid_dt_layer.dataProvider()
    # split geometry based on input layer
    geom_a = [feat.geometry() for feat in list_feature_a]
    geom_b = [feat.geometry() for feat in list_feature_b]

    geom_list = []
    for ga in geom_a:
        for gb in geom_b:
            if ga.intersects(gb):
                geom_list.append(ga)
                geom_list.append(gb)
    if len(geom_list) > 0:
        geom_combine = geom_list[0]
        for geom in geom_list[1:]:
            geom_combine = geom_combine.combine(geom)
        result, new_geometries, point_xy = valid_delaunay.splitGeometry(
            geom_combine.asPolyline(), True
        )
        for geom in [valid_delaunay] + new_geometries:
            feat = QgsFeature()
            feat.setGeometry(geom)
            valid_dt_layer_pr.addFeature(feat)
    else:
        feat = QgsFeature()
        feat.setGeometry(valid_delaunay)
        valid_dt_layer_pr.addFeature(feat)
    valid_dt_layer.startEditing()
    valid_dt_layer.commitChanges()
    valid_dt_layer.updateExtents()
    return valid_dt_layer


def create_median_line_opposite(vd_layer, list_feature_a, list_feature_b, crs):
    sp_index = QgsSpatialIndex(vd_layer)
    voronoi_a = []
    # voronoi_id_a = []
    for line in list_feature_a:
        idx = sp_index.intersects(line.geometry().boundingBox())
        req = QgsFeatureRequest().setFilterFids(idx)
        req_feat = [feat for feat in vd_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().intersects(line.geometry()):
                voronoi_a.append(feat.geometry())
                # voronoi_id_a.append(feat.id())
    # vd_layer.select(voronoi_id_a)
    voronoi_b = []
    for line in list_feature_b:
        idx = sp_index.intersects(line.geometry().boundingBox())
        req = QgsFeatureRequest().setFilterFids(idx)
        req_feat = [feat for feat in vd_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().intersects(line.geometry()):
                voronoi_b.append(feat.geometry())

    voronoi_mp_a = voronoi_a[0]
    voronoi_mp_b = voronoi_b[0]
    # create multipart geometry to enable dissolving
    for geom in voronoi_a[1:]:
        voronoi_mp_a.addPartGeometry(geom)
    for geom in voronoi_b[1:]:
        voronoi_mp_b.addPartGeometry(geom)
    # dissolve voronoi for each input using buffer 0 distance
    dissolve_voronoi_a = voronoi_mp_a.buffer(0, 5)
    dissolve_voronoi_b = voronoi_mp_b.buffer(0, 5)
    # convert to line
    dissolve_voronoi_a_line = QgsGeometry.fromPolylineXY(
        dissolve_voronoi_a.asPolygon()[0]
    )
    dissolve_voronoi_b_line = QgsGeometry.fromPolylineXY(
        dissolve_voronoi_b.asPolygon()[0]
    )
    # create intersection between dissolved voronoi line as final median line
    median_line = dissolve_voronoi_a_line.intersection(dissolve_voronoi_b_line)

    # convert multipart geometry to singlepart
    median_line_gc = median_line.asGeometryCollection()
    median_line_combine = median_line_gc[0]
    for geom in median_line_gc[1:]:
        median_line_combine = median_line_combine.combine(geom)
    list_median_line = median_line_combine.asGeometryCollection()

    # create layer
    median_layer = QgsVectorLayer("LineString?crs=" + crs, "Median Line", "memory")
    median_layer_pr = median_layer.dataProvider()
    median_layer_pr.addAttributes([QgsField("name", QVariant.String)])
    median_layer.updateFields()
    for median_line in list_median_line:
        # add feature to layer
        median_feat = QgsFeature()
        median_feat.setGeometry(median_line)
        median_feat.setAttributes(["Median Line"])
        median_layer_pr.addFeature(median_feat)
        median_layer.startEditing()
        median_layer.commitChanges()
        median_layer.updateExtents()
    return median_layer


def create_median_line_adjacent(vd_layer, list_feature_a, list_feature_b, crs):
    sp_index = QgsSpatialIndex(vd_layer)

    # find intersection point
    list_pt_of_intersection = []
    # get point of intersection
    for fa in list_feature_a:
        for fb in list_feature_b:
            if fa.geometry().intersects(fb.geometry()):
                poi = fa.geometry().intersection(fb.geometry())
                list_pt_of_intersection.append(poi)
    list_pt_of_intersection = list(set(list_pt_of_intersection))
    if len(list_pt_of_intersection) == 1:
        meeting_point = list_pt_of_intersection[0]
    else:
        wkt_list_pt_of_intersection = [pt.asWkt() for pt in list_pt_of_intersection]
        unique_list_pt_of_intersection = [
            QgsGeometry().fromWkt(wkt_pt)
            for wkt_pt in list(set(wkt_list_pt_of_intersection))
        ]
        if len(unique_list_pt_of_intersection) == 1:
            meeting_point = unique_list_pt_of_intersection[0]
        else:
            print(len(list_pt_of_intersection), list_pt_of_intersection)

    # find intersection voronoi
    intersection_voronoi = []
    idx = sp_index.intersects(meeting_point.boundingBox())
    req = QgsFeatureRequest().setFilterFids(idx)
    req_feat = [feat for feat in vd_layer.getFeatures(req)]
    for feat in req_feat:
        if feat.geometry().intersects(meeting_point):
            intersection_voronoi.append(feat.geometry())
    if len(intersection_voronoi) == 1:
        voro_polygon = intersection_voronoi[0]

    # create initial median line
    voronoi_a = []
    for line in list_feature_a:
        idx = sp_index.intersects(line.geometry().boundingBox())
        req = QgsFeatureRequest().setFilterFids(idx)
        req_feat = [feat for feat in vd_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().intersects(line.geometry()):
                voronoi_a.append(feat.geometry())
    voronoi_b = []
    for line in list_feature_b:
        idx = sp_index.intersects(line.geometry().boundingBox())
        req = QgsFeatureRequest().setFilterFids(idx)
        req_feat = [feat for feat in vd_layer.getFeatures(req)]
        for feat in req_feat:
            if feat.geometry().intersects(line.geometry()):
                voronoi_b.append(feat.geometry())
    voronoi_mp_a = voronoi_a[0]
    voronoi_mp_b = voronoi_b[0]
    # create multipart geometry to enable dissolving
    for geom in voronoi_a[1:]:
        voronoi_mp_a.addPartGeometry(geom)
    for geom in voronoi_b[1:]:
        voronoi_mp_b.addPartGeometry(geom)
    # dissolve voronoi for each input using buffer 0 distance
    dissolve_voronoi_a = voronoi_mp_a.buffer(0, 5)
    dissolve_voronoi_b = voronoi_mp_b.buffer(0, 5)
    # convert to line
    dissolve_voronoi_a_line = QgsGeometry.fromPolylineXY(
        dissolve_voronoi_a.asPolygon()[0]
    )
    dissolve_voronoi_b_line = QgsGeometry.fromPolylineXY(
        dissolve_voronoi_b.asPolygon()[0]
    )
    # create intersection between dissolved voronoi line as final median line
    median_line = dissolve_voronoi_a_line.intersection(dissolve_voronoi_b_line)
    # convert multipart geometry to singlepart
    median_line_gc = median_line.asGeometryCollection()
    median_line_combine = median_line_gc[0]
    for geom in median_line_gc[1:]:
        median_line_combine = median_line_combine.combine(geom)
    list_median_line_single = median_line_combine.asGeometryCollection()

    # find the nearest point and create line segment from it
    list_median_line = []
    for line in list_median_line_single:
        closest_vertex = line.closestVertex(meeting_point.asPoint())
        geom_line = QgsGeometry().fromPolylineXY(
            [closest_vertex[0], meeting_point.asPoint()]
        )
        line = line.combine(geom_line)
        list_median_line.append(line)
    # create layer
    median_layer = QgsVectorLayer("LineString?crs=" + crs, "Median Line", "memory")
    median_layer_pr = median_layer.dataProvider()
    median_layer_pr.addAttributes([QgsField("name", QVariant.String)])
    median_layer.updateFields()
    for median_line in list_median_line:
        # add feature to layer
        median_feat = QgsFeature()
        median_feat.setGeometry(median_line)
        median_feat.setAttributes(["Median Line"])
        median_layer_pr.addFeature(median_feat)
        median_layer.startEditing()
        median_layer.commitChanges()
        median_layer.updateExtents()
    return median_layer


def create_equidistant_point(median_layer):
    equidistant_pt_layer = QgsVectorLayer(
        "Point?crs=" + median_layer.crs().authid(), "Equidistant Point", "memory"
    )
    equidistant_pt_layer_pr = equidistant_pt_layer.dataProvider()
    equidistant_pt_layer_pr.addAttributes([QgsField("id", QVariant.Int)])
    equidistant_pt_layer.updateFields()
    if len(median_layer.selectedFeatures()) > 0:
        list_geom = [feat.geometry() for feat in median_layer.selectedFeatures()]
    else:
        list_geom = [feat.geometry() for feat in median_layer.getFeatures()]

    point_id = 0
    list_point_feat = []
    for median_line_geom in list_geom:
        for point in median_line_geom.asPolyline():
            point_feat = QgsFeature()
            point_feat.setGeometry(QgsGeometry.fromPointXY(point))
            point_feat.setAttributes([point_id])
            equidistant_pt_layer_pr.addFeature(point_feat)
            point_id += 1
    equidistant_pt_layer.startEditing()
    equidistant_pt_layer.commitChanges()
    equidistant_pt_layer.updateExtents()
    return equidistant_pt_layer


def create_construction_line(vd_layer, equidistant_pt_layer, merged_pt_layer):
    cl_layer = QgsVectorLayer(
        "Linestring?crs=" + vd_layer.crs().authid(), "Construction Line", "memory"
    )
    cl_layer_pr = cl_layer.dataProvider()
    cl_layer_pr.addAttributes([QgsField("line_id", QVariant.Int)])
    cl_layer.updateFields()
    vd_index = QgsSpatialIndex(vd_layer)
    for feat in equidistant_pt_layer.getFeatures():
        intersect_idx = vd_index.intersects(feat.geometry().boundingBox())
        req = QgsFeatureRequest().setFilterFids(intersect_idx)
        req_feat = [feat for feat in vd_layer.getFeatures(req)]
        list_pid = []
        list_pt = []
        for f in req_feat:
            if f.geometry().intersects(feat.geometry()):
                pid = f["point_id"]
                list_pid.append(pid)
                pt_feat = [
                    feat
                    for feat in merged_pt_layer.getFeatures(
                        QgsFeatureRequest(QgsExpression(f"\"point_id\" = '{pid}'"))
                    )
                ]
                if len(pt_feat) == 1:
                    list_pt.append(pt_feat[0].geometry().asPoint())
        if len(list_pt) == 3:
            eq_pt = feat.geometry().asPoint()
            # create multilinestring feature
            cl_geom = QgsGeometry().fromMultiPolylineXY(
                [
                    [QgsPointXY(eq_pt), QgsPointXY(list_pt[0])],
                    [QgsPointXY(eq_pt), QgsPointXY(list_pt[1])],
                    [QgsPointXY(eq_pt), QgsPointXY(list_pt[2])],
                ]
            )
            cl_feat = QgsFeature()
            cl_feat.setGeometry(cl_geom)
            cl_feat.setAttributes([feat["id"]])
            cl_layer_pr.addFeature(cl_feat)
    cl_layer.startEditing()
    cl_layer.commitChanges()
    cl_layer.updateExtents()
    return cl_layer

def generate_final_boundary(list_feature_a, list_feature_b, boundary_distance_m, median_layer, crs, buffer_segment = 25):
    # create buffer_a
    geom_a = list_feature_a[0].geometry()
    if len(list_feature_a) >= 1:
        for feat in list_feature_a[1:]:
            geom_a.addPartGeometry(feat.geometry())
    buffer_a = geom_a.buffer(boundary_distance_m, buffer_segment)
    # create buffer_b
    geom_b = list_feature_b[0].geometry()
    if len(list_feature_b) >= 1:
        for feat in list_feature_b[1:]:
            geom_b.addPartGeometry(feat.geometry())
    buffer_b = geom_b.buffer(boundary_distance_m, buffer_segment)
    # common area intersection
    common_area = buffer_a.intersection(buffer_b)
    # boundary polyline
    boundary_a = QgsGeometry.fromPolylineXY(buffer_a.asPolygon()[0])
    boundary_b = QgsGeometry.fromPolylineXY(buffer_b.asPolygon()[0])
    # common line boundary
    median_line = [feat.geometry() for feat in median_layer.getFeatures()]
    line = median_line[0]
    if len(median_line) > 1:
        for geom in median_line[1:]:
            line.addPartGeometry(geom)
    common_line = line.intersection(common_area)
    # final boundary
    final_boundary_a = boundary_a.difference(buffer_b).combine(common_line)
    feat_a = QgsFeature()
    feat_a.setGeometry(final_boundary_a)
    final_boundary_b = boundary_b.difference(buffer_a).combine(common_line)
    feat_b = QgsFeature()
    feat_b.setGeometry(final_boundary_b)
    
    line_layer = QgsVectorLayer("Linestring?crs=" + crs, 'Boundary Layer', "memory")
    line_layer_pr = line_layer.dataProvider()

    line_layer_pr.addFeature(feat_a)
    line_layer_pr.addFeature(feat_b)
    line_layer.startEditing()
    line_layer.commitChanges()
    return line_layer
    
    

# def side_buffer_rubberbands(line_rubberband, buffer_distance, buffer_segment, buffer_side):
#     geom = QgsGeometry()
#     buffer_geom = geom.singleSidedBuffer(buffer_distance, buffer_segment, buffer_side)
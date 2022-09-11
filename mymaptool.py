from PyQt5.QtGui import QColor
from qgis.gui import QgsMapTool, QgsVertexMarker
from qgis.utils import iface

class PointTool(QgsMapTool):   
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        
        self.vm = QgsVertexMarker(canvas)
        self.vm.setColor(QColor(255,0, 0)) #(R,G,B)
        self.vm.setIconSize(10)
        self.vm.setIconType(QgsVertexMarker.ICON_CIRCLE)
        self.vm.setPenWidth(3)

        self.vm2 = QgsVertexMarker(canvas)
        self.vm2.setColor(QColor(230,0, 0)) #(R,G,B)
        self.vm2.setIconSize(10)
        self.vm2.setIconType(QgsVertexMarker.ICON_X)
        self.vm2.setPenWidth(3)

        self.isEmitting = True

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):      
        if self.isEmitting:
            self.point_snap = self.snapping(event.pos())
            self.vm2.setCenter(self.point_snap)

    def canvasReleaseEvent(self, event):
        self.vm.setCenter(self.point_snap)
        
        self.isEmitting = False
        self.canvas.scene().removeItem(self.vm2)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def snapping(self, point):
        utils = self.canvas.snappingUtils()
        match = utils.snapToMap(point)
        if match.isValid():
            return match.point()
        else:
            return self.canvas.getCoordinateTransform().toMapCoordinates(point)

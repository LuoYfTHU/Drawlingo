"""
Drawing Canvas Widget - Supports mouse, touch, and tablet input
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap, QPaintEvent, QResizeEvent, QMouseEvent, QTabletEvent, QColor
from PyQt6.QtCore import QEvent

class DrawingCanvas(QWidget):
    """Custom widget for drawing sketches with mouse, touch, or tablet support."""
    
    # Tool types
    TOOL_PEN = 0
    TOOL_ERASER = 1
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_drawing = False
        self.m_hasDrawing = False
        self.m_lastPoint = QPoint()
        
        # Tool and color settings
        self.m_currentTool = self.TOOL_PEN
        self.m_currentColor = QColor(Qt.GlobalColor.black)
        self.m_penWidth = 3
        
        # Enable touch and tablet events
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TabletTracking, True)
        
        self.setupPen()
        
        # Initialize pixmap with default size
        self.m_pixmap = QPixmap(800, 600)
        self.m_pixmap.fill(Qt.GlobalColor.white)
    
    def setupPen(self):
        """Initialize the pen for drawing."""
        if self.m_currentTool == self.TOOL_ERASER:
            # Eraser uses white color
            self.m_pen = QPen(Qt.GlobalColor.white, self.m_penWidth * 2)  # Eraser is wider
        else:
            # Pen uses current color
            self.m_pen = QPen(self.m_currentColor, self.m_penWidth)
        
        self.m_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.m_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    
    def setTool(self, tool):
        """Set the current drawing tool (TOOL_PEN or TOOL_ERASER)."""
        self.m_currentTool = tool
      
        self.setupPen()
    
    def setColor(self, color):
        """Set the drawing color. Can be QColor or Qt.GlobalColor."""
        if isinstance(color, QColor):
            self.m_currentColor = color
        else:
            self.m_currentColor = QColor(color)
        if self.m_currentTool == self.TOOL_PEN:
            self.setupPen()
    
    def setPenWidth(self, width):
        """Set the pen width."""
        self.m_penWidth = width
        self.setupPen()
    
    def getCurrentTool(self):
        """Get the current tool."""
        return self.m_currentTool
    
    def getCurrentColor(self):
        """Get the current color."""
        return self.m_currentColor
    
    def clearCanvas(self):
        """Clear the canvas."""
        self.m_pixmap.fill(Qt.GlobalColor.white)
        self.m_hasDrawing = False
        self.update()
    
    def hasDrawing(self):
        """Check if there's a drawing on the canvas."""
        return self.m_hasDrawing
    
    def getSketch(self):
        """Get the current sketch as a QPixmap."""
        return self.m_pixmap
    
    def paintEvent(self, event: QPaintEvent):
        """Paint the canvas."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.m_pixmap)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_lastPoint = event.position().toPoint()
            self.m_drawing = True
            self.m_hasDrawing = True
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events."""
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.m_drawing:
            self.drawLineTo(event.position().toPoint())
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton and self.m_drawing:
            self.drawLineTo(event.position().toPoint())
            self.m_drawing = False
    
    def tabletEvent(self, event: QTabletEvent):
        """Handle tablet/stylus events."""
        event_type = event.type()
        
        if event_type == QEvent.Type.TabletPress:
            if not self.m_drawing:
                self.m_lastPoint = event.position().toPoint()
                self.m_drawing = True
                self.m_hasDrawing = True
                
                # Adjust pen pressure
                if event.pressure() > 0.0:
                    base_width = self.m_penWidth * 2 if self.m_currentTool == self.TOOL_ERASER else self.m_penWidth
                    self.m_pen.setWidthF(base_width * event.pressure())
        elif event_type == QEvent.Type.TabletMove:
            if self.m_drawing:
                self.drawLineTo(event.position().toPoint())
                
                # Adjust pen pressure
                if event.pressure() > 0.0:
                    base_width = self.m_penWidth * 2 if self.m_currentTool == self.TOOL_ERASER else self.m_penWidth
                    self.m_pen.setWidthF(base_width * event.pressure())
        elif event_type == QEvent.Type.TabletRelease:
            if self.m_drawing:
                self.drawLineTo(event.position().toPoint())
                self.m_drawing = False
                self.setupPen()  # Reset pen
        
        event.accept()
    
    def event(self, event: QEvent):
        """Handle touch events."""
        event_type = event.type()
        
        if event_type in (QEvent.Type.TouchBegin, QEvent.Type.TouchUpdate, QEvent.Type.TouchEnd):
            touch_event = event
            touch_points = touch_event.points()
            
            if touch_points:
                touch_point = touch_points[0]
                pos = touch_point.position().toPoint()
                
                if event_type == QEvent.Type.TouchBegin:
                    self.m_lastPoint = pos
                    self.m_drawing = True
                    self.m_hasDrawing = True
                elif event_type == QEvent.Type.TouchUpdate:
                    if self.m_drawing:
                        self.drawLineTo(pos)
                elif event_type == QEvent.Type.TouchEnd:
                    if self.m_drawing:
                        self.drawLineTo(pos)
                        self.m_drawing = False
                
                event.accept()
                return True
        
        return super().event(event)
    
    def drawLineTo(self, endPoint: QPoint):
        """Draw a line from the last point to the end point."""
        painter = QPainter(self.m_pixmap)
        painter.setPen(self.m_pen)
        painter.drawLine(self.m_lastPoint, endPoint)
        
        # Update the widget
        rad = (self.m_pen.width() // 2) + 2
        update_rect = self.m_lastPoint.x(), self.m_lastPoint.y(), endPoint.x(), endPoint.y()
        from PyQt6.QtCore import QRect
        update_rect = QRect(self.m_lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad)
        self.update(update_rect)
        
        self.m_lastPoint = endPoint
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle resize events."""
        # Resize pixmap if widget is larger
        if self.width() > self.m_pixmap.width() or self.height() > self.m_pixmap.height():
            newWidth = max(self.width() + 128, self.m_pixmap.width())
            newHeight = max(self.height() + 128, self.m_pixmap.height())
            
            newPixmap = QPixmap(newWidth, newHeight)
            newPixmap.fill(Qt.GlobalColor.white)
            
            painter = QPainter(newPixmap)
            painter.drawPixmap(0, 0, self.m_pixmap)
            self.m_pixmap = newPixmap
        
        super().resizeEvent(event)


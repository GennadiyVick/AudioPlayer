import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from OpenGL.GL import *
from PyQt5.QtOpenGL import *



class GLWidget(QGLWidget):
    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)
        self.w = 100
        self.h = 30
        self.initializeGL()

    def initializeGL(self):
        pass
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #glOrtho(0.0, 600, 0.0, 600, -1.0, 1.0)
        #glMatrixMode (GL_MODELVIEW)
        #glLoadIdentity()

    def resizeGL(self, w, h):
        self.w = w
        self.h = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, w, 0.0, h, -1.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def drawquad(self, pos, size, color1, color2):
        glBegin(GL_QUADS)
        glColor3f(*color1)
        glVertex2f(pos[0], self.h-(pos[1]+size[1]))
        glColor3f(*color2)
        glVertex2f(pos[0], self.h-pos[1])
        glVertex2f(pos[0]+size[1], self.h-pos[1])
        glColor3f(*color1)
        glVertex2f(pos[0]+size[1], self.h-(pos[1]+size[1]))
        glEnd()

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glRotate(4, 0.0, 0.0, 1.0)
        self.drawquad((10,10), (200,200), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        '''
        glBegin(GL_QUADS)
        #red color
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(150, 450)
        glVertex2f(150,150)
        #blue color
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(450, 150)
        glVertex2f(450,  450)
        glEnd()
        '''
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('OpenGL example')
        self.resize(600,600)
        self.gl = GLWidget(self)
        self.gl.format().setVersion(4, 2)
        self.gl.format().setProfile(QGLFormat.CoreProfile)
        self.setCentralWidget(self.gl)
        timer = QtCore.QTimer(self)
        timer.setInterval(30)   # period, in milliseconds
        timer.timeout.connect(self.gl.updateGL)
        timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


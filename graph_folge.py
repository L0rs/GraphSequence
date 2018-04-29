import sys
from PyQt5.QtTest import QTest as qtst
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import time
import random
import numpy as np
import re
import ctypes
from math import exp, sqrt, e, pi, sin, cos, tan, log

class Window(QDialog):
    range_i = 0
    running = False
    function = "1/n"
    linesOnOff = "*"
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        w = 1920
        h = 1080
        self.resize(w,h)
        self.setWindowTitle("SequenceProgram")
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.setWindowIcon(QIcon("Icons/ape256.png"))


        #create menuBar that user can change some settings
        self.myQMenuBar = QMenuBar(self)
        menuFile = self.myQMenuBar.addMenu("File")
        menuEdit = self.myQMenuBar.addMenu("Edit")
        menuHelp = self.myQMenuBar.addMenu("Help")

        #subMenu
        actQuit = QAction('Quit', self) 
        actQuit.triggered.connect(self.closeEvent)
        graphStyle = QAction('Lines On/Off', self) 
        graphStyle.triggered.connect(self.setLinesOnOff)
        readme = QAction('Information',self)
        message = "This program is created by Lars Stockum"
        title = "Information"
        messageIcon = QMessageBox.Information
        readme.triggered.connect(lambda *args, message=message, title=title, messageIcon=messageIcon: self.message_box(message, title, messageIcon)) 


        #set events for my menuBar
        menuFile.addAction(actQuit)
        menuEdit.addAction(graphStyle)
        menuHelp.addAction(readme)
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(1000)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # button connected to `plot` method
        self.button1 = QPushButton('+1')
        self.button1.clicked.connect(self.increment_plot)

        #textbox for user input
        self.textbox1 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)

        #button connected to text_plot function
        self.button2 = QPushButton('+')
        self.button2.clicked.connect(self.text_plot)

        #button connected to run_plot function
        self.button3 = QPushButton('Run/Pause')
        self.button3.clicked.connect(self.run_plot)
        #button connected to run_plot function
        self.button4 = QPushButton('OK')
        self.button4.clicked.connect(self.setFunction)

        #label to give last result of calculation
        self.label = QLabel("", self)
        #horizontal box to have the textbox on the same level as the belonging button
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.textbox1)
        hbox1.addWidget(self.button2)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.textbox2)
        hbox2.addWidget(self.button4)
        
        # set the layout --> vertical layout --> widgets or whole layouts placed one below the other
        layout = QVBoxLayout()
        layout.addWidget(self.myQMenuBar)
        layout.addWidget(self.toolbar)
        layout.addLayout(hbox2)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button1)
        layout.addLayout(hbox1)
        layout.addWidget(self.label)
        #layout.setSpacing(1)
        layout.addWidget(self.button3)
        
        self.setLayout(layout)
    def setLinesOnOff(self):
        self.linesOnOff = "*-" if self.linesOnOff == "*" else "*"
        if self.running == False and self.range_i>0:
            self.plot()
    def setFunction(self):
        input_sequence = self.textbox2.text()
       
        searchObj = re.search("[^0-9n\/\-\+\*\^\(\)\.|exp|sqrt|e|pi|sin|cos|tan|log]",input_sequence)
        if searchObj:
            self.message_box("The program can not handle your input","Wrong Symbols")
        else:
            self.function = input_sequence.replace("^","**")
    def text_plot(self):
        #get string from textbox
        textboxValue = self.textbox1.text()
        try:
            #parse string to integer and maybe catch wrong user input
            textboxValue_int=int(textboxValue)
        except ValueError:
            self.message_box("This is not a number","ValueError")
        else:
            if textboxValue_int <= 0:
                self.message_box("Number should be bigger than 0","Wrong Number")
            if textboxValue_int > 500000:
                self.message_box("Program not optimized for such big values","Wrong Number")
            else:
            #if everything seems fine we can give the new value range_i and plot the new numbers
                self.range_i = textboxValue_int 
                self.plot()

    def message_box(self, text, title, icon = QMessageBox.Critical):
        msg = QMessageBox()
        msg.setIcon(icon) 
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()   

    def run_plot(self):
        if self.running == False:
            self.running = True
        else:
            self.running = False
        while self.running == True:
            self.range_i+=1
            self.plot()
            qtst.qWait(0.01) #wait for 1ms
    def increment_plot(self):
        self.range_i+=1
        self.plot()

    def plot(self):
        try:
            y = [eval(self.function) for n in range( 1,self.range_i+1)] 
            x = range(1,self.range_i+1, 1)
            n = self.range_i
            text = str(eval(self.function)) 
        except:
            self.message_box("The program can not handle your input","Wrong Syntax")
            self.running = False
            self.range_i-=1
        else:
            self.label.setText(text)
            self.figure.clear()

            # create an axis
            ax = self.figure.add_subplot(111)
            ax.clear()

            ax.plot(x,y, self.linesOnOff)#'*-'
            # refresh canvas
            self.canvas.draw()
            
        
    def closeEvent(self, event):
        quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    
    main.show()
    sys.exit(app.exec_())


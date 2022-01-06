#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2022-01-05
"""

from QtCompat import QtWidgets, QtGui, QtCore, Signal, Slot, Qt

class LabelWidget(QtWidgets.QLabel):
    def __init__(self, name):
        super(LabelWidget, self).__init__()
        self.setText(name)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Arial", 11, 70))

class GroupBoxWidget(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super(GroupBoxWidget, self).__init__(parent)

        self.setTitle("Options")
        self.setFont(QtGui.QFont("Arial", 12, 60))
        self.setMinimumSize(QtCore.QSize(380, 110))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        css = """
            QGroupBox {    
                border: 1px solid gray;    
                border-radius: 9px;   
                margin-top: 0.4em;
            }
            QGroupBox::title {    
                subcontrol-origin: margin;    
                left: 10px;    
                padding: 0 3px 0 3px;
            }
        """
        self.setStyleSheet(css)

class TypeWidget(QtWidgets.QRadioButton):
    def __init__(self, name):
        super(TypeWidget, self).__init__()
        self.setObjectName(name)
        self.setMinimumSize(QtCore.QSize(50, 20))
        self.setMaximumSize(QtCore.QSize(120, 16777215))
        self.setText(name)
        self.setFont(QtGui.QFont("Arial", 11, 75))

class LineEditWidget(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEditWidget, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(300, 25))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Arial", 12, 70))

        self._value = None

    @property
    def value(self):
        if self.text() == None: return
        if len(str(self.text()))== 0: return

        return str(self.text())

    @value.setter
    def value(self, text):
        if len(text)== 0 : return
        if text == None  : return
        self.setText(str(text))

    def set_rule(self):
        regexRule = QtCore.QRegExp("[0-9A-Za-z\-\,]+")
        validator = QtGui.QRegExpValidator(regexRule)
        self.setValidator(validator)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.backspace()
        else:
            super(LineEditWidget, self).keyPressEvent(event) 
            self.setCursorPosition(0)
          

class LogoWidget(QtWidgets.QLabel):
    isTimeOut = QtCore.pyqtSignal() 

    def __init__(self, parent=None):
        super(LogoWidget, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(50, 25))
        self.setMaximumSize(QtCore.QSize(50, 16777215))
        self.setAlignment(QtCore.Qt.AlignCenter)

        self._second = 0
        self._status = False
        self.set_font()


        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer_second)

    @property
    def second(self):
        return int(self.text())

    @property
    def status(self):
        return self._status

    @second.setter
    def second(self, value):
        if not isinstance(value, int): 
            return
        
        if value >= 0:
            self.setText(str(value))

    @status.setter
    def status(self, new_status):
        if not isinstance(new_status, bool): 
            return

        self.status = new_status

        if new_status == True:
            self.start()
        else:
            self.stop()

    def update_timer_second(self):
        self.second -= 1
        if self.second == 0:
            self.isTimeOut.emit()

    def start(self):
        self.countdown_timer.start(1000)

    def stop(self):
        self.countdown_timer.stop()

    def set_font(self):
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)






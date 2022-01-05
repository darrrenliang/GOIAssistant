#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2022-01-05
"""

import os
import logging

# from i18n          import _
from QtCompat      import QtWidgets, QtGui, QtCore, Signal, Slot, Qt
from acsQt         import actions
from acstw.OracleInterface import OracleInterface

logger  = logging.getLogger(__name__)
USER    = os.getenv('ORACLE_USER', 'acs_qa')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_qa')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)

class GroupBoxWidget(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super(GroupBoxWidget, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(400, 450))
        self.setMaximumSize(QtCore.QSize(400, 16777215))

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addItem(QtWidgets.QSpacerItem(0,10,QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed))

        self.set_font()
        self.set_stylesheet()

        self._title = None
        
    @property
    def title(self):
        if self.text() == None: return
        if len(str(self.text()))== 0: return
        return str(self.text())

    @title.setter
    def title(self, text):
        if len(text)== 0 : return
        if text == None  : return
        self.setTitle(str(text))

    def addRow(self, key=None, value=None, unit=None):        
        layout = QtWidgets.QHBoxLayout()       
        label1 = self.gen_name_label(key)
        widget = self.gen_value_line(value)
      
        if label1 != None:
            layout.addWidget(label1)
            layout.addItem(QtWidgets.QSpacerItem(30,0,QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed))
        
        if widget != None:
            layout.addWidget(widget)
        
        label2 = self.gen_unit_label(unit)
        layout.addWidget(label2)

        self.layout.addRow(layout)

    def gen_name_label(self, text=None):
        if text == None:
            return text
        else:
            editor = QtWidgets.QLabel(self)
            editor.setText(str(text))
            editor.setAlignment(QtCore.Qt.AlignCenter)
            return editor
        
    def gen_value_line(self, text=None):
        if text == None:
            return text
        else:
            editor = QtWidgets.QLineEdit(self)
            editor.setReadOnly(True)
            editor.setText(str(text))
            editor.setAlignment(QtCore.Qt.AlignCenter)
            editor.setMinimumSize(QtCore.QSize(180, 25))
            editor.setMaximumSize(QtCore.QSize(180, 16777215))
            return editor

    def gen_unit_label(self, text=None):
        label = QtWidgets.QLabel(self)
        label.setMinimumSize(QtCore.QSize(35, 25))
        label.setMaximumSize(QtCore.QSize(35, 16777215))
        label.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        font.setPointSize(9)
        label.setFont(font)

        if text != None:
            label.setText(str(text))

        return label

    def set_font(self):
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.setFont(font)

    def set_stylesheet(self):
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
    

class LineEditWidget(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEditWidget, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(200, 25))
        self.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setReadOnly(True)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self._value = None
        self.set_font()

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

    def set_font(self):
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)

    def set_rule(self):
        regexRule = QtCore.QRegExp("[0-9A-Za-z\-\,]+")
        validator = QtGui.QRegExpValidator(regexRule)
        self.setValidator(validator)


class ColockWidget(QtWidgets.QLabel):
    isTimeOut = QtCore.pyqtSignal() 

    def __init__(self, parent=None):
        super(ColockWidget, self).__init__(parent)
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






#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2022-01-05
"""

import os
import sys
import time
import platform
import logging

from core.loggerInterface import logger_setup
from QtCompat             import QtWidgets, QtGui, QtCore, Slot, Qt
from QtCompat.QtCore      import (PYQT_VERSION_STR, QT_VERSION_STR, QSettings)

# from acsQt import labels 
# from acsQt import actions
# from acsQt.login           import LoginForm
from core.MyWidgets.application import create_q_application
from __init__  import (TITLE, PRISM, connect_database)

from version import __version__

from core.MyWidgets.widgets     import GroupBoxWidget, LineEditWidget, LabelWidget, TypeWidget
from core.MyWidgets.TableModel  import DeviceTableModel
from core.MyWidgets.TableView   import DeviceTableView

COPYRIGHT_YEAR = 2022
DEFAULT_WIDTH  = 400
DEFAULT_HEIGHT = 700

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QDialog):
    def __init__(self, device, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # set gui window size
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        self.device = device

        # setup ui
        self.setupUi()

        self.re_init_table()
        

    def setupUi(self):
        # =====================================================================
        # Main layout
        # =====================================================================
        VBoxLayout1 = QtWidgets.QVBoxLayout(self) 
        
        # =====================================================================
        # Filter Section 
        # =====================================================================
        GroupBox = GroupBoxWidget(self)

        VVBoxLayout = QtWidgets.QVBoxLayout() 
        filter_section = QtWidgets.QHBoxLayout()
        filterLabel    = LabelWidget("Filter")
        self.filterEditor = LineEditWidget(self)

        self.filterEditor.textEdited.connect(self.re_init_table)
        filter_section.addWidget(filterLabel)
        filter_section.addStretch()
        filter_section.addWidget(self.filterEditor)
        filter_section.addStretch()

        types_section = QtWidgets.QHBoxLayout()
        optionLabel   = LabelWidget("Type")
        self.byNumber = TypeWidget("ByNumber")
        self.byName   = TypeWidget("ByName")
        
        self.byNumber.setChecked(True)
        self.byNumber.toggled.connect(lambda x : self.filterEditor.setText(""))
        self.byName.toggled.connect(lambda x : self.filterEditor.setText(""))

        types_section.addWidget(optionLabel)
        types_section.addStretch()
        types_section.addWidget(self.byNumber)
        types_section.addStretch()
        types_section.addWidget(self.byName)
        types_section.addStretch()

        VVBoxLayout.addLayout(filter_section)
        VVBoxLayout.addLayout(types_section)
        GroupBox.setLayout(VVBoxLayout)
        VBoxLayout1.addWidget(GroupBox)

        # =====================================================================
        # TableView Widget
        # =====================================================================
        DeviceList_Section = QtWidgets.QHBoxLayout()
        self.deviceView  = DeviceTableView(self)
        self.deviceModel = DeviceTableModel(self)
        self.deviceView.setModel(self.deviceModel)
        self.deviceView.doubleClicked.connect(self.exec_operschem)

        DeviceList_Section.addWidget(self.deviceView)
        VBoxLayout1.addLayout(DeviceList_Section)

        # =====================================================================
        # Footer Section
        # =====================================================================
        Footer_Section = QtWidgets.QHBoxLayout()
        ButtonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel, self)
        ButtonBox.setFont(QtGui.QFont("Arial", 13, 70))
        ButtonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Exit")
        ButtonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

        Footer_Section.addStretch()
        Footer_Section.addWidget(ButtonBox)
        VBoxLayout1.addLayout(Footer_Section)

    def exec_operschem(self, item):
        number  = self.deviceModel._datas[item.row()][0]
        command = f"oiint {self.device} -c display -fwin {number}"
        PRISM.ExeNonCommand(command)


    def re_init_table(self):
        params = {
            "byname"  : self.byName.state,
            "bynumber": self.byNumber.state,
            "filter"  : str(self.filterEditor.text())
        }
        self.deviceModel.re_init(params)
        

def main(device):
    logger_setup()

    app = create_q_application(TITLE)
    goi_assistant = MainWindow(device)
    goi_assistant.show()
    app.exec_()

if __name__ == '__main__':
    import sys

    device = 1
    sys.exit(main(device))


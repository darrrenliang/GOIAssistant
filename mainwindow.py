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
from __init__  import (TITLE, connect_database)

from version import __version__

from core.MyWidgets.widgets     import GroupBoxWidget, LineEditWidget, LabelWidget, TypeWidget
from core.MyWidgets.TableModel  import DeviceTableModel
from core.MyWidgets.TableView   import DeviceTableView

COPYRIGHT_YEAR = 2022
DEFAULT_WIDTH  = 400
DEFAULT_HEIGHT = 700

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # set gui window size
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        # # =====================================================================
        # # argument area 
        # # =====================================================================
        # self._colock    = 60
        # self._casename  = 'SCA_OUT'
        # self._parameter = 'DTS DYNAMIC FAULT'

        # # =====================================================================
        # # data processing 
        # # =====================================================================
        # self.schema  = self.get_schema_by_case(casename=self.casename)
        # self.value   = self.get_table_value(self.schema)
        # self.dataset = self.gen_dataSet_by_schema(self.schema, self.value)

        self.setupUi()
        

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
        Filter_Section = QtWidgets.QHBoxLayout()
        FilterEditor   = LineEditWidget(self)
        FilterLabel    = LabelWidget("Filter")

        Filter_Section.addWidget(FilterLabel)
        Filter_Section.addStretch()
        Filter_Section.addWidget(FilterEditor)
        Filter_Section.addStretch()

        Types_Section = QtWidgets.QHBoxLayout()
        OptionLabel   = LabelWidget("Type")
        ByNum_Option  = TypeWidget("ByNumber")
        ByNum_Option.setChecked(True)
        ByName_Option = TypeWidget("ByName")

        Types_Section.addWidget(OptionLabel)
        Types_Section.addStretch()
        Types_Section.addWidget(ByNum_Option)
        Types_Section.addStretch()
        Types_Section.addWidget(ByName_Option)
        Types_Section.addStretch()

        VVBoxLayout.addLayout(Filter_Section)
        VVBoxLayout.addLayout(Types_Section)
        GroupBox.setLayout(VVBoxLayout)
        VBoxLayout1.addWidget(GroupBox)

        # =====================================================================
        # TableView Widget
        # =====================================================================
        DeviceList_Section = QtWidgets.QHBoxLayout()
        DeviceView  = DeviceTableView(self)
        DeviceModel = DeviceTableModel(self)
        DeviceView.setModel(DeviceModel)

        DeviceList_Section.addWidget(DeviceView)
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


def main():
    logger_setup()

    app = create_q_application(TITLE)
    goi_assistant = MainWindow()
    goi_assistant.show()
    app.exec_()

if __name__ == '__main__':
    import sys
    sys.exit(main())


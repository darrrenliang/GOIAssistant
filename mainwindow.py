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
from core.MyWidgets.application     import create_q_application
from __init__  import (TITLE, connect_database)


from version       import __version__

# from adms_widgets import GroupBoxWidget, LineEditWidget, ColockWidget

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

        # self.setupUi(dataset=self.dataset)

    def setupUi(self, dataset):
        # =====================================================================
        # Main layout
        # =====================================================================
        VBoxLayout1 = QtWidgets.QVBoxLayout(self) 
        
        # =====================================================================
        # CaseName widget
        # =====================================================================
        CaseName  = LineEditWidget(self)
        CaseName.value = self.casename
        HBoxLayout1 = QtWidgets.QHBoxLayout()
        HBoxLayout1.addItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        HBoxLayout1.addWidget(CaseName)
        HBoxLayout1.addItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        VBoxLayout1.addLayout(HBoxLayout1)

        # =====================================================================
        # GroupBox widget
        # =====================================================================
        HBoxLayout2 = QtWidgets.QHBoxLayout()
        groupboxes  = []
        for num in range(dataset['colcount']):
            col = num + 1
            GroupBox = GroupBoxWidget(self)
            HBoxLayout2.addWidget(GroupBox)
            groupboxes.append(GroupBox)

        VBoxLayout1.addLayout(HBoxLayout2)
        # =====================================================================
        # Attribute widget
        # =====================================================================
        for numcol, groups in dataset['dataset'].items():
            groupBox = groupboxes[int(numcol)-1]
            groupBox.title = groups['label']
            for num in range(len(groups['attributes'])):
                # print(num)
                if str(num+1) in groups['attributes']:
                    dataset = groups['attributes'][str(num+1)]
                    widget  = groupBox.addRow(dataset['colname'], dataset['value'], dataset['unit'])
                else:
                    widget  = groupBox.addRow(None, None, None)

        # =====================================================================
        # Countdown colock 
        # =====================================================================
        self.Clock = ColockWidget(self)
        self.Clock.second = self.colock
        self.Clock.start()
        self.Clock.isTimeOut.connect(self.close)

        ButtonBox  = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, self)
        ButtonBox.accepted.connect(self.close)

        HBoxLayout = QtWidgets.QHBoxLayout()
        HBoxLayout.addWidget(self.Clock)
        HBoxLayout.addItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        HBoxLayout.addWidget(ButtonBox)
        VBoxLayout1.addLayout(HBoxLayout)



def main():
    logger_setup()

    app = create_q_application(TITLE)
    goi_assistant = MainWindow()
    goi_assistant.show()
    app.exec_()

if __name__ == '__main__':
    import sys
    sys.exit(main())


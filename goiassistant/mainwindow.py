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

from goiassistant.__init__  import (TITLE, PRISM, connect_database)
from goiassistant.version   import __version__

from goiassistant.core.loggerInterface  import logger_setup
from goiassistant.core.QtCompat         import QtWidgets, QtGui, QtCore, Slot, Qt
from goiassistant.core.QtCompat.QtCore  import (PYQT_VERSION_STR, QT_VERSION_STR, QSettings)

from goiassistant.core.MyWidgets.application import create_q_application
from goiassistant.core.MyWidgets.widgets     import GroupBoxWidget, LineEditWidget, LabelWidget, TypeWidget
from goiassistant.core.MyWidgets.TableModel  import DeviceTableModel
from goiassistant.core.MyWidgets.TableView   import DeviceTableView

COPYRIGHT_YEAR = 2022
DEFAULT_WIDTH  = 600
DEFAULT_HEIGHT = 900

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QDialog):
    def __init__(self, device, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.settings = QSettings("acstw", TITLE) 
        self.device   = device
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
        self.byEquip  = TypeWidget("ByEquip")
        
        self.byNumber.setChecked(True)
        
        self.byNumber.toggled.connect(self.clear_content)
        self.byNumber.toggled.connect(self.re_init_table)
        self.byName.toggled.connect(self.clear_content)
        self.byName.toggled.connect(self.re_init_table)
        self.byEquip.toggled.connect(self.clear_content)
        self.byEquip.toggled.connect(self.re_init_table)

        types_section.addWidget(optionLabel)
        types_section.addStretch(1)
        types_section.addWidget(self.byNumber)
        types_section.addStretch(1)
        types_section.addWidget(self.byName)
        types_section.addStretch(1)
        types_section.addWidget(self.byEquip)
        types_section.addStretch(2)

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

    def clear_content(self):
        self.filterEditor.setText("")
        self.filterEditor.setFocus()

    def exec_operschem(self, item):
        number  = self.deviceModel._datas[item.row()][0]
        command = f"oiint {self.device} -c display -fwin {number}"
        PRISM.ExeNonCommand(command)

    def re_init_table(self):
        params = {
            "byname"  : self.byName.state,
            "bynumber": self.byNumber.state,
            "byequip" : self.byEquip.state,
            "content" : str(self.filterEditor.text())
        }
        self.deviceModel.re_init(params)
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            pass
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def restore_settings(self):
        """
        Load QSettings file if it exists. If it doesn't exist, then load
        some default settings.
        """
        self.settings.beginGroup("Misc")
        self.restoreGeometry(self.settings.value('Geometry', QtCore.QByteArray()))
        
        settings_width  = int(self.settings.value('Width' ))
        settings_height = int(self.settings.value('Height'))

        restore_width   = settings_width  if settings_width  else DEFAULT_WIDTH
        restore_height  = settings_height if settings_height else DEFAULT_HEIGHT

        self.resize(restore_width, restore_height)
        self.settings.endGroup()


        # deviceView - Column Widths
        self.settings.beginGroup("deviceView")
        try:
            st_view_col_cnt = int(self.settings.value("NumOfColumns"))
        except TypeError:
            # Invalid or missing value
            pass
        else:
            # Don't restore the width of the last column; it should automatically
            # expand as needed. If we restore the width, sometimes we get a
            # spurious scroll bar.
            for col in range(st_view_col_cnt - 1):
                Name = "Col_%02d" % col                
                w = int(self.settings.value(Name))
                self.deviceView.setColumnWidth(col, w)
        finally:
            self.settings.endGroup()

    def save_settings(self):
        self.settings.beginGroup("Misc")
        self.settings.setValue('Geometry',    self.saveGeometry())

        save_width  = self.width()  if self.width()  >= DEFAULT_WIDTH  else DEFAULT_WIDTH
        save_height = self.height() if self.height() >= DEFAULT_HEIGHT else DEFAULT_HEIGHT

        self.settings.setValue('Width' , save_width)
        self.settings.setValue('Height', save_height)
        self.settings.endGroup()

        # deviceView - Column Widths
        self.settings.beginGroup("deviceView")
        st_view_col_cnt = self.deviceView.horizontalHeader().count()
        self.settings.setValue("NumOfColumns", st_view_col_cnt)

        for col in range(st_view_col_cnt):
            name = "Col_%02d" % col
            self.settings.setValue(name, self.deviceView.columnWidth(col))
        self.settings.endGroup()    

    def load_settings(self):
        """
        Load QSettings configuration settings.
        We don't need to check whether the file exists, because it should
        gracefully handle any missing settings.
        """
        self.restore_settings()

    def closeEvent(self, event):
        """
        If adms_gui is not start compeletely, it will not save app settings.
        """
        if self.isVisible():
            self.save_settings()

def main(device):
    logger_setup()

    app = create_q_application(TITLE)
    goi_assistant = MainWindow(device)
    goi_assistant.load_settings()
    goi_assistant.show()
    app.exec_()

if __name__ == '__main__':
    import sys

    device = 1
    sys.exit(main(device))


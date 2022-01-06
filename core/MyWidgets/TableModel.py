# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'
__date__   = '2021-11-24'

import os
import operator
import datetime
import logging
from core.MyWidgets.refresh_mixin import RefreshMixin
from QtCompat            import QtWidgets, QtGui, QtCore, Qt
from __init__            import connect_database

logger  = logging.getLogger(__name__)

Mapdb   = connect_database()

HEADERS = ("NUMBER", "SUBSTATION", "NAME")


# TODO: merge with common station view/model in acsprism package?
class DeviceTableModel(RefreshMixin, QtCore.QAbstractTableModel):
    # parent is required for models, otherwise you get spurious Qt warnings
    def __init__(self, parent):
        super(DeviceTableModel, self).__init__()

        # get data from sql
        self._datas  = []
        self.HEADERS = HEADERS

        self.re_init()

    @property
    def datas(self):
        return self._datas

    def re_init(self):
        with self._pause_refresh():
            self._datas    = self.get_data()        
            self.endResetModel()
    
    def _on_refresh(self):
        self._datas = self.get_data()
        self.invalidate()
        logger.debug("Refreshing dasapp table")

    def invalidate(self):
        # logger.debug("Refreshing")

        # Behavior of emitting with invalid indexes is not documented
        # self.dataChanged.emit(QModelIndex(), QModelIndex())

        # Indicate that all the attribute values changed, so the view
        # will re-read them.
        # Even though I give the column, it still seems to read all columns.
        # Indeed, even if I specify just one row, it still seems to read
        # all the visible rows and columns. I wonder what the point of the
        # arguments are anyway... am I doing it wrong?
        # May need to check Qt source code.
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1, self.columnCount() - 1))

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.datas)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole:
            value = self.datas[row][column]           
            return str(value)

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        
        if role == QtCore.Qt.FontRole:
            return QtGui.QFont("Arial", 11, 70)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.HEADERS[section]
        return int(section + 1)
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def get_data(self):

        query = f"""
            select command_string, substation, textcontents from gis_command
        """
        data = list(map(list, Mapdb.ExecQuery(query)))
        return sorted(data, key=lambda tup: tup[0], reverse=False)
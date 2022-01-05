# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

from QtCompat import QtWidgets, QtGui, QtCore, Slot, Qt

__author__ = 'Darren Liang'

def create_spacer(self, width=None, height=None, policy=None): # policy: 0 (Fixed) | 1 (Expanding)
    width  = 0 if width  is None else width
    height = 0 if height is None else height
    policy = QtWidgets.QSizePolicy.Fixed if policy==0 else QtWidgets.QSizePolicy.Expanding
    spacer = QtWidgets.QSpacerItem(width,height,policy,policy)
    return spacer

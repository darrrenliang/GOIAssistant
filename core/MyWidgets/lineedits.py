# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

__author__ = 'Darrne Liang'

from QtCompat import QtGui

def set_lineedit_attributes(lineedit, text=None, size=None, PlaceholderText=None, Alignment=None, MaxLength=None, ReadOnly=None, tip=None):
    if text is not None:
        lineedit.setText(text)

    if size is not None:
        lineedit.resize(size[0], size[1])
    
    if PlaceholderText is not None:
        lineedit.setPlaceholderText(PlaceholderText)

    if Alignment is not None:
        lineedit.setAlignment(Alignment)

    if MaxLength is not None:
        lineedit.setMaxLength(int(MaxLength))
        
    if ReadOnly:
        lineedit.setReadOnly(ReadOnly)

    if tip:
        lineedit.setToolTip(tip)
        lineedit.setStatusTip(tip)

def create_lineedit(text=None, PlaceholderText=None, Alignment=None, MaxLength=None, ReadOnly=None, tip=None):
    lineedit = QtGui.QLineEdit()
    lineedit.set_lineedit_attributes(lineedit, text=None, PlaceholderText=None, Alignment=None, MaxLength=None, ReadOnly=None, tip=None)
    return lineedit
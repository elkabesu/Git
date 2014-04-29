# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProcureDialog
                                 A QGIS plugin
 Get shapefiles from the web
                             -------------------
        begin                : 2014-02-17
        copyright            : (C) 2014 by Derek Sanz
        email                : lkb_su13@hotmail.com
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_procure import Ui_Procure


class ProcureDialog(QtGui.QDialog, Ui_Procure):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from QTDesigner.
        self.setupUi(self)

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Procure
                                 A QGIS plugin
 Get shapefiles from the web
                             -------------------
        begin                : 2014-02-17
        copyright            : (C) 2014 by Derek Sanz
        email                : lkb_su13@hotmail.com
 ***************************************************************************/
"""

def classFactory(iface):
    # load Procure class from file Procure
    from procure import Procure
    return Procure(iface)

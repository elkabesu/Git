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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Procure class from file Procure
    from procure import Procure
    return Procure(iface)

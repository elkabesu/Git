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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
import glob
import os

import urllib
import urllib2
import zipfile

# Import the code for the dialog
from procuredialog import ProcureDialog
import os.path


class Procure:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'procure_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ProcureDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/procure/icon.png"),
            u"Get shapefiles from the web", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Procure", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Procure", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
		# show the dialog
        self.dlg.show()	
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
		
        if result == 1:
			self.downloadFile()
			self.unzipFile()
			self.uploadLayer()
			
    def downloadFile(self):
		# read and download the webpage containing the zip file
		url = urllib2.urlopen("http://www.nyc.gov/html/dcp/html/bytes/dwnfresh.shtml")
		html = url.read()
		
		# download the zip file
		download = "http://www.nyc.gov/html/dcp/download/bytes/nyc_freshzoning20111.zip"
		request = urllib2.urlopen(download)
		
		print "File downloaded"
	
		# save the zip file 
		output = open("abcd.zip", "r")
		output.write(request.read())
		output.close()
		
		print "File saved"
		
    def unzipFile(self):
		# create a new folder to keep the shapefiles
		newpath = r'C:\Shapefiles' 
		if not os.path.exists(newpath): os.makedirs(newpath)
		
		# unzip the zip file
		with zipfile.ZipFile('abcd.zip', "r") as z:
				z.extractall(newpath)
		
		print "File unzipped"
    
    def uploadLayer(self):
		# upload the layers
        vlayer = QgsVectorLayer("\Shapefiles\FRESH.shp", "FRESH.shp", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        if not vlayer.isValid():
            print "Layer failed to load!" 

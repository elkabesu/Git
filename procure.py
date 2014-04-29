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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from procuredialog import ProcureDialog
from collections import OrderedDict

import resources
import glob
import os
import urllib
import urllib2
import zipfile
import os.path
import win32api

samplezipfilepath = "C:\\Desktop\\sample.zip"
path = 'C:\Shapefiles\\'
shapefilesarray = ["Fresh Zoning Boundaries", "MapPLUTO - Brooklyn", "GIS Zoning Features", "Sidewalk Cafes"]
statesarray = {'NY'}
webpagedictionary = (("http://www.nyc.gov/html/dcp/html/bytes/dwnfresh.shtml", "http://www.nyc.gov/html/dcp/download/bytes/nyc_freshzoning20111.zip"),
	("http://www.nyc.gov/html/dcp/html/bytes/dwn_pluto_mappluto.shtml#mappluto", "http://www.nyc.gov/html/dcp/download/bytes/bk_mappluto13v2.zip"),
	("http://www.nyc.gov/html/dcp/html/bytes/dwnzdata.shtml", "http://www.nyc.gov/html/dcp/download/bytes/nycgiszoningfeatures_201401_shp.zip"),
	("http://www.nyc.gov/html/dcp/html/bytes/dwnsidewalk.shtml", "http://www.nyc.gov/html/dcp/download/bytes/nycgissidewalkcafe_201401_shp.zip"))

webpagedictionary = OrderedDict(webpagedictionary)

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

        self.dlg = ProcureDialog()
        self.adddialogfile(Procure)
        self.adddialogState(Procure)

    def adddialogfile(self,Procure):
    	for i in shapefilesarray:
   			self.dlg.comboBox.addItem(i)

    def adddialogState(self,Procure):
    	for i in statesarray:
    	    self.dlg.comboBox_2.addItem(i)

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

    def run(self):
		# show the dialog
        self.dlg.show()	

        # Run the dialog event loop
        result = self.dlg.exec_()

        # Check if OK was pressed
        if result == 1:
        	self.readchoice()

    def readchoice(self):
    	# check what was chosen in dialog box
    	choice = str(self.dlg.comboBox.currentText())
    	for i in shapefilesarray:
    		if i == choice:
    			break
    	shapefilesarrayindex = shapefilesarray.index(i)

    	self.downloadwebsite(shapefilesarrayindex)

    def downloadwebsite(self, shapefilesarrayindex):
    	# check to see if there exists internet connection. pop-up win32 window if no internet
    	try:
    		url = urllib2.urlopen(webpagedictionary.keys()[shapefilesarrayindex], timeout = 1)
    		downloadedurl = url.read()
    		self.downloadfile(shapefilesarrayindex)
    		return True
    	except urllib2.URLError as err: win32api.MessageBox(0, 'No Internet Connection', 'Error', 0x00001000) 
    	return False

    def downloadfile(self, shapefilesarrayindex):
		downloadedzip = webpagedictionary.values()[shapefilesarrayindex]
		openedzip = urllib2.urlopen(downloadedzip)

		self.savefile(openedzip)

    def savefile(self, openedzip):
    	# create a blank .zip file and copy the downloaded .zip file to that blank .zip file
		openedsamplezipfile = open(samplezipfilepath, "wb+")
		openedsamplezipfile.write(openedzip.read())
		openedsamplezipfile.close()

		self.createdirectory()

    def createdirectory(self):
		# create a new folder to keep the shapefiles
		if not os.path.exists(path): 
			os.makedirs(path)

		self.unzipfile()

    def unzipfile(self):
		with zipfile.ZipFile(samplezipfilepath) as z:
			z.extractall(path)

		self.uploadlayer()

    def uploadlayer(self):
    	# search the Shapefiles folder for the last modified .shp file and then upload it
    	directories, files = self.distinguishfilesanddirectories()
    	folderlessshapefiles = self.getfolderlessshapefiles(files)
    	mostrecent = self.mostrecentsubdirectory(directories)
    	mostrecentsubdirectoryfileslist = self.mostrecentsubdirectoryfiles(mostrecent)
    	shapefilesList = self.listshapefiles(mostrecentsubdirectoryfileslist)

    	self.upload(shapefilesList)

    def distinguishfilesanddirectories(self):
    	# traverse the C:\Shapefiles folder
    	directories = []
    	files = []

    	for d in os.listdir(path):
    		shapefilepath = os.path.join(path, d)
    		if os.path.isdir(shapefilepath):
    			directories.append(shapefilepath)
    		else:
    			files.append(shapefilepath)

    	return directories, files

    def getfolderlessshapefiles(self, files):
    	# find the shapefiles that are not in a folder
    	folderlessshapefiles = []
    	for f in files:
    		if f[-3:] == "shp":
    			folderlessshapefiles.append(f)

    	return folderlessshapefiles

    def mostrecentsubdirectory(self, directories):
    	mostrecent = directories[0]
    	for direc in directories:
    		if os.stat(mostrecent).st_ctime < os.stat(direc).st_ctime:
    			mostrecent = direc

    	return mostrecent

    def mostrecentsubdirectoryfiles(self, mostrecent):
    	# place all the files that exist in the most recent subdirectory into a list
    	mostrecentsubdirectoryfileslist = []
    	for d in os.listdir(mostrecent):
    		subshapefilepath = os.path.join(mostrecent, d)
    		if os.path.isdir(subshapefilepath):
    			for sd in os.listdir(subshapefilepath):
    				mostrecentsubdirectoryfileslist.append(os.path.join(subshapefilepath,sd))
    		else: 
    			mostrecentsubdirectoryfileslist.append(subshapefilepath)

    	return mostrecentsubdirectoryfileslist

    def listshapefiles(self, subfilesList):
    	# return the shapefiles that exist in the most recent subdirectory
    	shapefilesList = []
    	for f in subfilesList:
    		if f[-3:] == "shp":
    			print "shp is " + f
    			shapefilesList.append(f)

    	return shapefilesList

    def upload(self, shapefilesList):
    	# upload all the shapefiles (.shp) files in the most recent subdirectory
    	for i in shapefilesList:
    		vlayer = QgsVectorLayer(i, i[-16:-4], "ogr")
    		QgsMapLayerRegistry.instance().addMapLayer(vlayer)
    		if not vlayer.isValid():
    			print "Layer failed to load!"

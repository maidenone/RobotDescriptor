import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore

import xml.etree.ElementTree as ET 

from .RD_parser import initialize_element_tree
#directory to initilize icon 
__dirname__ = os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "RobotDescriptor")+"/robot_descriptor/icons/initialize.svg"
#class to store the selected properties

_DESCRIPTION_FORMAT='sdf'
_SDF_VERSION='1.10'
#this will hold the entire sdf definition of the sdf file 
#as a dictionary which will then be converted into a .sdf file
class RD_properties:
    def __init__(self):
        self.description_format='sdf'
        self.Type="ElementTree"
        #this will hold the entire sdf definition of the sdf file 
#as a dictionary which will then be converted into a .sdf file
        self._element_tree=None
    
    @property 
    def format(self):
        return self.description_format
    
    @format.setter
    def format(self,value):
        self.description_format=value

    
    
#
class initialize_widget(QtGui.QWidget):
	def __init__(self):
		super(initialize_widget,self).__init__()
		self.initUI()
	def initUI(self):
		uipath=FreeCAD.getUserAppDataDir()+"/Mod/RobotDescriptor/robot_descriptor/forms/initialize.ui"
		self.form=FreeCADGui.PySideUic.loadUi(uipath,self)
		self.format_qbox=self.form.format_popup
		self.accpt_btn=self.form.accept_button
  
#create callbacks (slots)
		
		self.format_qbox.currentTextChanged.connect(self.format_qb_cb)
		self.accpt_btn.clicked.connect(self.accpt_btn_cb)
		self.form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#set window size and initial position 
		self.form.setGeometry(400,300,400,300)
		self.form.show()	
  
	def format_qb_cb(self):
#urdf isn not yet implemented  ensure urdf is not selected
		self.format_item=self.format_qbox.currentText()
		if self.format_item=="urdf":
			self.msg=QtGui.QMessageBox.information(self.form,"","urdf is not yet supported switching to sdf")
			self.format_qbox.setCurrentText("sdf")
		else:
			pass
#button callback 

	def accpt_btn_cb(self):
		#ensure there is an active document
		try:
			document=FreeCAD.ActiveDocument
		except:
			FreeCAD.Console.PrintError("No active document found \n")
			return
# check to ensure  a document object exists, if it does not add it

		try:
			group=document.Robot_Description
			group.isValid()
				
		except:
			group =document.addObject("App::DocumentObjectGroupPython","Robot_Description")
			description_properties=RD_properties()
			description_properties.format=self.format_qbox.currentText()
			if description_properties.format=='sdf':
				group.Proxy=description_properties
	# create an element tree for the root node 
	# convert to string to allow serialization 
	#there might be a better way to handle this 
				root_elem=initialize_element_tree.convdict_2_tree("root.sdf").get_elements
				group.Proxy._element_tree=root_elem
				
			else:
				pass
				
				

class RD_init:
    
    def GetResources(self):
        return {"Pixmap":__dirname__,"Accel":"shift+i","MenuText":"Initialization ","ToolTip":"initialize properties"}
    
    def Activated(self):
        self.init_c=initialize_widget()
        
    def IsActive(slef):
        if _DESCRIPTION_FORMAT=='sdf':
            return True
        else:
            return False


FreeCADGui.addCommand('RD_initialize',RD_init()) 
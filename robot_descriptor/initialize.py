import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore

#import Spreadsheet
import xml.etree.ElementTree as ET 

from .RD_utils import initialize_element_tree
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
		self.Type="Dictionary"
		self._element_dict=None
	@property 
	def format(self):
		return self.description_format
    
	@format.setter
	def format(self,value):
		self.description_format=value
    
	@property
	def element_dict(self):
		return self._element_dict
    
	@element_dict.setter
	def element_dict(self,elem_d:dict):
		'''returns a dictionary {"tag":tag_name,"element_str":element converted to string,"children":[]}'''
		self._element_dict=elem_d
        
#===================================================
#initialize
#===================================================
class initialize:
	def __init__(self):
    #ensure there is an active document
		document=FreeCAD.ActiveDocument	
# check to ensure  a document object exists, if it does not add it
		if not hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
			group =document.addObject("App::DocumentObjectGroupPython","Robot_Description")
			#spreadsheet for points of the road 
			points=document.addObject('Spreadsheet::Sheet','points')
			group.addObject(points)
			# label columns 
			for row,label in [('A','x'),('B','y'),('C','z')]:
				points.set(f'{row}1',label)
				points.set(f'{row}2','0')
				points.setStyle(f'{row}1','bold')
			description_properties=RD_properties()
			if description_properties.format=='sdf':
				group.Proxy=description_properties
	# create an element tree for the root node 
	# convert to string to allow serialization 
	#there might be a better way to handle this 
				root_elem=initialize_element_tree.convdict_2_tree("root.sdf").get_element
				root_elem_str=ET.tostring(root_elem,encoding='unicode',xml_declaration=None)
# some elements may occur multiple times in a parent element e.g a world can have many models 
# the recurring key is used to track this , if false the elem_str will be a string , if 
#true elem_str will be a list of strings where each index will be an instance of the element
				group.Proxy.element_dict={"sdf":{"elem_str":root_elem_str,"recurring":False,"children":{}}}
    #object will store a pointer to the active widget

		document.recompute()
'''
dictionary format:
		{
			key: element tag name
			value: a dictionary 
   				{
					key: elem_str
					value: string representation of the element,

					key: recurring
					value: a boolean value that indicates if an element can have multiple occurences
     
					key: children
					value: a dictionary of children exhibiting the same  format as the parent
     				{
						
					}
				}
		}
'''								

class RD_init:
    
	def GetResources(self):
		return {"Pixmap":__dirname__,"Accel":"shift+i","MenuText":"Initialization ","ToolTip":"initialize properties"}
    
	def Activated(self):
		if FreeCAD.activeDocument() is None:
			return
		else:
			self.rd=initialize()
        
	def IsActive(self):
		if FreeCAD.activeDocument() is not None :
			#check if robot description document object is already defined 
			#return false if its already defined no need to re-initialize again
			if hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
				return False
			else:
				return True
		else:
			return False


FreeCADGui.addCommand('RD_initialize',RD_init()) 
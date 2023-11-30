import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore
#directory to initilize icon 
__dirname__ = os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "RobotDescriptor")+"/robot_descriptor/icons/initialize.svg"
#class to store the selected properties
class init_properties:
	def __init__(self):
		self._format='sdf'
		self._version='1.10'
		#this will hold the entire sdf definition of the sdf file 
		#as a dictionary which will then be converted into a .sdf file
		self._elements={}
  
	@property
	def format(self):
		return self._format
	@format.setter
	def format(self,value):
		self._format=value

	@property
	def version(self):
		return self._version
	@version.setter
	def version(self,value):
		self._version=value
  
	@property
	def elements(self):
		return self._elements
	#will be implemented later
	@elements.setter
	def elements(self,elem):
		pass

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
			self.msg=QtGui.QMessageBox.information(self.form,"","urdf not yet supported switching to sdf")
			self.format_qbox.setCurrentText("sdf")
		else:
			pass
#button callback 
	def accpt_btn_cb(self):
		try:
			document=FreeCAD.ActiveDocument
		except:
			FreeCAD.Console.PrintError("No active document found \n")
			return
		try:
			group=document.Robot_Description
			group.isValid()
			group.Proxy.format=self.format_qbox.currentText()
			
		except:
			group =document.addObject("App::DocumentObjectGroupPython","Robot_Description")
			group.Proxy=init_properties()
			group.Proxy.format=self.format_qbox.currentText()
			


class RD_init:
    
    def GetResources(self):
        return {"Pixmap":__dirname__,"Accel":"shift+i","MenuText":"Initialization ","ToolTip":"initialize properties"}
    
    def Activated(self):
        self.init_c=initialize_widget()
        
    def IsActive(slef):
        return True


FreeCADGui.addCommand('RD_initialize',RD_init()) 
import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore
#directory to initilize icon 
__dirname__ = os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "RobotCreator")+"/robot_creator/icons/initialize.svg"
#class to store the selected properties
class init_properties:
	def __init__(self):
		self._format='sdf'
		self._version='1.7'

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

#
class initialize_widget(QtGui.QWidget):
	def __init__(self):
		super(initialize_widget,self).__init__()
		self.initUI()
	def initUI(self):
		uipath=FreeCAD.getUserAppDataDir()+"/Mod/RobotCreator/robot_creator/ui/initialize.ui"
		self.form=FreeCADGui.PySideUic.loadUi(uipath,self)
		self.version_qbox=self.form.version_popup
		self.format_qbox=self.form.format_popup
		self.accpt_btn=self.form.accept_button
  
#create callbacks (slots)
		self.version_qbox.currentTextChanged.connect(self.version_qbox_cb)
		self.format_qbox.currentTextChanged.connect(self.format_qb_cb)
		self.accpt_btn.clicked.connect(self.accpt_btn_cb)
		self.form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#set window size and initial position 
		self.form.setGeometry(400,300,400,300)
		self.form.show()
	def version_qbox_cb(self):
		self.version_item=self.version_qbox.currentText()
		FreeCAD.Console.PrintMessage("version selection "+self.version_item+"\n")	
  
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
			group.Proxy.version=self.version_qbox.currentText()
		except:
			group =document.addObject("App::DocumentObjectGroupPython","Robot_Description")
			group.Proxy=init_properties()
			group.Proxy.format=self.format_qbox.currentText()
			group.Proxy.version=self.version_qbox.currentText()


class RC_init:
    
    def GetResources(self):
        return {"Pixmap":__dirname__,"Accel":"shift+i","MenuText":"Initialization ","ToolTip":"initialize properties"}
    
    def Activated(self):
        self.init_c=initialize_widget()
        
    def IsActive(slef):
        return True


FreeCADGui.addCommand('RC_initialize',RC_init()) 
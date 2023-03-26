from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

__title__ = "RobotCreator Workbench - Init file"
__author__ = "Anton Fosselius <anton.fosselius@ googles email .com>"
__url__ = "https://www.freecadweb.org"

class RobotCreator (Workbench):

	def __init__(self):
		def QT_TRANSLATE_NOOP(context, text):
			return text
		__dirname__ = os.path.join(FreeCAD.getResourceDir(), "Mod", "RobotCreator")
		_tooltip = "The RobotCreator workbench is used to create URDF or SDF files"
		self.__class__.Icon = os.path.join(__dirname__, "Resources", "icons", "SDFexportStatic.png")
		self.__class__.MenuText = QT_TRANSLATE_NOOP("RobotCreator", "RobotCreator")
		self.__class__.ToolTip = QT_TRANSLATE_NOOP("RobotCreator", _tooltip)

	def Initialize(self):
		"This function is executed when FreeCAD starts"
		__dirname__ = os.path.join(FreeCAD.getResourceDir(), "Mod", "RobotCreator")
		print("got dir:" + __dirname__);
		import GazeboSDFExportStatic, GazeboSDFExport, CreateJoint # import here all the needed files that create your FreeCAD commands
		self.list = ['RC_GazeboSDFExportStatic','RC_GazeboSDFExport', 'RC_CreateJoint'] # A list of command names created in the line above
		self.appendToolbar("RobotCreator",self.list) # creates a new toolbar with your commands
		self.appendMenu("My New Menu",self.list) # creates a new menu
		self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

	def Activated(self):
		"This function is executed when the workbench is activated"
		return

	def Deactivated(self):
		"This function is executed when the workbench is deactivated"
		return

	def ContextMenu(self, recipient):
		"This is executed whenever the user right-clicks on screen"
		# "recipient" will be either "view" or "tree"
		self.appendContextMenu("My commands",self.list) # add commands to the context menu

	def GetClassName(self): 
		# this function is mandatory if this is a full python workbench
		return "Gui::PythonWorkbench"

Gui.addWorkbench(RobotCreator())

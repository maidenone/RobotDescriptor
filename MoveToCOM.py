from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

class MoveToCOM:
    """RC_MoveToCOM"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+M", # a default shortcut (optional)
                'MenuText': "Move To Center Of Mass",
                'ToolTip' : "Centers your Mesh"}

    def Activated(self):
	print "moving shape to center of mass"
	com = Gui.ActiveDocument.Body.Object.Shape.CenterOfMass
	Gui.ActiveDocument.Body.Object.Placement = Gui.ActiveDocument.Body.Object.Placement.move(com*-1)
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('RC_MoveToCOM',MoveToCOM()) 

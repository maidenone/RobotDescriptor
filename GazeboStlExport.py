from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

class GazeboStlExport:
    """GazeboStlExport"""

    def GetResources(self):
        return {'Pixmap'  : 'OpenSCAD_Explode_Group', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "Gazebo STL export",
                'ToolTip' : "Exports STL in meters normal unit is millimeter"}

    def Activated(self):
        print "Scaling mesh"
	import Mesh,BuildRegularGeoms
	mat=FreeCAD.Matrix()
	mat.scale(0.001,0.001,0.001)
	
	obj = App.ActiveDocument.Objects[0]
	obj.Name
	mesh=App.ActiveDocument.Objects[0].Mesh.copy() #Cube is the name of the Object in the 	Document

	com = Gui.ActiveDocument.Body.Object.Shape.CenterOfMass
	Gui.ActiveDocument.Body.Object.Placement = Gui.ActiveDocument.Body.Object.Placement.move(com*-1)
	mesh.transform(mat) #add the result to the docuemnt
	Mesh.show(mesh)
	__objs__=[]
	__objs__.append(FreeCAD.ActiveDocument.getObject("Mesh"))
	Mesh.export(__objs__,u"/home/maiden/Projects/tinyArm/"+obj.Name+".stl")
	print "Saved mesh to /home/maiden/Projects/tinyArm/"+obj.Name+".stl"
	App.ActiveDocument.removeObject("Mesh")
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('RC_GazeboStlExport',GazeboStlExport()) 

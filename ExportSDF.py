from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

class ExportSDF:
    """RC_ExportSDF"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+E", # a default shortcut (optional)
                'MenuText': "Export Robot to SDF",
                'ToolTip' : "Export Robot to SDF"}

    def Activated(self):
	print "Exporting SDF file"
	robotName = "testing"

	sdfFile = open(robotName+'.sdf', 'w')
	sdfFile.write('<?xml version=\"1.0\"?>\n')
	sdfFile.write('<sdf version=\"1.5\">\n')
	sdfFile.write('<model name=\"'+robotName+'\">\n')

	objs = FreeCAD.ActiveDocument.Objects
	for obj in objs:
		if obj.TypeId == 'PartDesign::Body':
			name = obj.Name
			com = obj.Shape.CenterOfMass
			mass = obj.Shape.Mass
			inertia = obj.Shape.MatrixOfInertia
			pos = obj.Shape.Placement

			sdfFile.write('<link name=\"'+name+'\">\n')
			sdfFile.write('<pose> ' + str(pos.Base[0]+com.x) + ' ' + str(pos.Base[1]+com.y) + ' ' + str(pos.Base[2]+com.z)+ ' ' + str(pos.Rotation.toEuler()[0]) + ' ' + str(pos.Rotation.toEuler()[1])+ ' ' + str(pos.Rotation.toEuler()[2])+'</pose>\n')
			sdfFile.write('<inertial>\n')
			sdfFile.write('<pose> ' + str(pos.Base[0]+com.x) + ' ' + str(pos.Base[1]+com.y) + ' ' + str(pos.Base[2]+com.z)+ ' ' + str(pos.Rotation.toEuler()[0]) + ' ' + str(pos.Rotation.toEuler()[1])+ ' ' + str(pos.Rotation.toEuler()[2])+'</pose>\n')
			sdfFile.write('<inertia>\n')
			sdfFile.write('<ixx>'+str(inertia.A11/1000)+'</ixx>\n')
			sdfFile.write('<ixy>'+str(inertia.A12/1000)+'</ixy>\n')
			sdfFile.write('<ixz>'+str(inertia.A13/1000)+'</ixz>\n')
			sdfFile.write('<iyy>'+str(inertia.A22/1000)+'</iyy>\n')
			sdfFile.write('<iyz>'+str(inertia.A23/1000)+'</iyz>\n')
			sdfFile.write('<izz>'+str(inertia.A33/1000)+'</izz>\n')
			sdfFile.write('</inertia>\n')
			sdfFile.write('<mass>'+str(mass/1000)+'</mass>\n')
			sdfFile.write('</inertial>\n')
			sdfFile.write('<collision name=\"collision\">\n')
			sdfFile.write('<geometry>\n')
			sdfFile.write('<mesh>\n')
			sdfFile.write('<uri>model://'+robotName+'/meshes/'+name+'.stl</uri>\n')
			sdfFile.write('</mesh>\n')
			sdfFile.write('</geometry>\n')
			sdfFile.write('</collision>\n')
			sdfFile.write('<visual name=\"visual\">\n')
			sdfFile.write('<geometry>\n')
			sdfFile.write('<mesh>\n')
			sdfFile.write('<uri>model://'+robotName+'/meshes/'+name+'.stl</uri>\n')
			sdfFile.write('</mesh>\n')
			sdfFile.write('</geometry>\n')
			sdfFile.write('</visual>\n')
			sdfFile.write('</link>\n')
	sdfFile.write('</model>\n')
	sdfFile.write('</sdf>\n')

	sdfFile.close()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('RC_ExportSDF',ExportSDF()) 

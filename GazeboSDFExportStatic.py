from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math
import Mesh,BuildRegularGeoms
import os, sys, Mesh

def float_to_str(f):
  return '{:.20f}'.format(f)

def deg2rad(a):
  return a*0.01745329252

def str2obj(a):
  return FreeCAD.ActiveDocument.getObject(a)

def bodyFromPad(a):
  objs = FreeCAD.ActiveDocument.Objects
  for obj in objs:
    if obj.TypeId == 'PartDesign::Body':
      if obj.hasObject(a):
        return obj

def bodyLabelFromObjStr(a):
  b = str2obj(a)
  c = bodyFromPad(b)
  return c.Label


class GazeboSDFExportStatic:
	"""GazeboSDFExport"""

	def GetResources(self):
		return {'Pixmap' : str(FreeCAD.getUserAppDataDir()+"Mod" + "/RobotCreator/icons/SDFexportStatic.png"), # the name of a svg file available in the resources
				'Accel' : "Shift+a", # a default shortcut (optional)
				'MenuText': "Gazebo static SDF export",
				'ToolTip' : "Exports static SDF to Gazebo"}

	def Activated(self):
		print "Scaling mesh"

		# you might want to change this to where you want your exported mesh/sdf to be located.
		robotName = "testing"
		#projPath = "/home/maiden/Projects/RobotCreator/"+robotName + "/"
		projPath = os.path.expanduser('~') + "/.gazebo/models/" + robotName + "Static/"
		meshPath = projPath + "meshes/"

		if not os.path.exists(projPath):
			os.makedirs(projPath)

		if not os.path.exists(meshPath):
			os.makedirs(meshPath)

		#os.chdir(projectName)

		sdfFile = open(projPath+robotName+'Static.sdf', 'w')
		sdfFile.write('<?xml version=\"1.0\"?>\n')
		sdfFile.write('<sdf version=\"1.5\">\n')
		sdfFile.write('<model name=\"'+robotName+'\">\n')
		sdfFile.write('<static>true</static>\n')

		objs = FreeCAD.ActiveDocument.Objects
		for obj in objs:
			print obj.Name
			if "Joint" in obj.Name:
				print "Joint: " + obj.Name + " with label " + obj.Label+ " detected!"
				pos = obj.Shape.Placement
				pos.Base *= 0.001
				sdfFile.write(' <joint name="'+bodyLabelFromObjStr(obj.Parent)+bodyLabelFromObjStr(obj.Child)+'" type="revolute">\n')
				sdfFile.write('   <pose>'+str(pos.Base[0]) + ' ' + str(pos.Base[1]) + ' ' + str(pos.Base[2])+ ' 0 0 0 </pose>\n')
				sdfFile.write('   <child>'+bodyLabelFromObjStr(obj.Child)+'</child>\n')
				sdfFile.write('   <parent>'+bodyLabelFromObjStr(obj.Parent)+'</parent>\n')
				sdfFile.write('   <axis>')
				sdfFile.write('     <xyz>0 0 1</xyz>')
				sdfFile.write('   </axis>\n')
				sdfFile.write(' </joint>\n')

			if obj.TypeId == 'PartDesign::Body' or obj.TypeId == 'Part::Box':
				print "Link: " + obj.Name + " with label " + obj.Label+ " detected!"
				name = obj.Label
				mass = obj.Shape.Mass
				inertia = obj.Shape.MatrixOfInertia
				pos = obj.Shape.Placement
				com = obj.Shape.CenterOfMass
				com *= 0.001
				mass *= 0.001
				A11 = inertia.A11 * 0.000000001
				A12 = inertia.A12 * 0.000000001
				A13 = inertia.A13 * 0.000000001
				A22 = inertia.A22 * 0.000000001
				A23 = inertia.A23 * 0.000000001
				A33 = inertia.A33 * 0.000000001

				pos.Base *= 0.001

				#export shape as mesh (stl)
				obj.Shape.exportStl(meshPath+name+".stl")
				#import stl and translate/scale
				mesh = Mesh.read(meshPath+name+".stl")

				# scaling, millimeter -> meter
				mat=FreeCAD.Matrix()
				mat.scale(0.001,0.001,0.001)

				#apply scaling
				mesh.transform(mat)

				#move origo to center of mass
				pos.move(com*-1)
				mesh.Placement.Base *= 0.001

				#save scaled and transformed mesh as stl
				mesh.write(meshPath+name+".stl")

				sdfFile.write('<link name=\"'+name+'\">\n')
				sdfFile.write('<pose> ' + str(0) + ' ' + str(0) + ' ' + str(0)+ ' ' + str(deg2rad(pos.Rotation.Q[0])) + ' ' + str(deg2rad(pos.Rotation.Q[1]))+ ' ' + str(deg2rad(pos.Rotation.Q[2]))+'</pose>\n')
				sdfFile.write('<inertial>\n')
				sdfFile.write('<pose> ' + str(0+com.x) + ' ' + str(0+com.y) + ' ' + str(0+com.z)+ ' ' + str(deg2rad(pos.Rotation.Q[0])) + ' ' + str(deg2rad(pos.Rotation.Q[1]))+ ' ' + str(deg2rad(pos.Rotation.Q[2]))+'</pose>\n')
				sdfFile.write('<inertia>\n')
				sdfFile.write('<ixx>'+float_to_str(A11)+'</ixx>\n')
				sdfFile.write('<ixy>'+float_to_str(A12)+'</ixy>\n')
				sdfFile.write('<ixz>'+float_to_str(A13)+'</ixz>\n')
				sdfFile.write('<iyy>'+float_to_str(A22)+'</iyy>\n')
				sdfFile.write('<iyz>'+float_to_str(A23)+'</iyz>\n')
				sdfFile.write('<izz>'+float_to_str(A33)+'</izz>\n')
				sdfFile.write('</inertia>\n')
				sdfFile.write('<mass>'+str(mass)+'</mass>\n')
				sdfFile.write('</inertial>\n')
				sdfFile.write('<collision name=\"collision\">\n')
				sdfFile.write('<geometry>\n')
				sdfFile.write('<mesh>\n')
				sdfFile.write('<uri>model://'+robotName+'Static/meshes/'+name+'.stl</uri>\n')
				sdfFile.write('</mesh>\n')
				sdfFile.write('</geometry>\n')
				sdfFile.write('</collision>\n')
				sdfFile.write('<visual name=\"visual\">\n')
				sdfFile.write('<geometry>\n')
				sdfFile.write('<mesh>\n')
				sdfFile.write('<uri>model://'+robotName+'Static/meshes/'+name+'.stl</uri>\n')
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

FreeCADGui.addCommand('RC_GazeboSDFExportStatic',GazeboSDFExportStatic()) 

from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

import FreeCAD as App
import FreeCADGui
import FreeCAD
import Part
import sys
from PySide import QtGui, QtCore

class CreateHingeJointForm(QtGui.QDialog):
	""""""
	def __init__(self):
		super(CreateHingeJointForm, self).__init__()
		self.initUI()

	def initUI(self):
		option1Button = QtGui.QPushButton("OK")
		option1Button.clicked.connect(self.onOption1)
		option2Button = QtGui.QPushButton("Cancel")
		option2Button.clicked.connect(self.onOption2)

		labelPosition = QtGui.QLabel('Position')
		labelRotation = QtGui.QLabel('Rotation')

		onlyDouble = QtGui.QDoubleValidator()
		self.posX = QtGui.QLineEdit('0')
		self.posX.setValidator(onlyDouble)
		self.posY = QtGui.QLineEdit('0')
		self.posY.setValidator(onlyDouble)
		self.posZ = QtGui.QLineEdit('0')
		self.posZ.setValidator(onlyDouble)
		self.rotX = QtGui.QLineEdit('1')
		self.rotX.setValidator(onlyDouble)
		self.rotY = QtGui.QLineEdit('0')
		self.rotY.setValidator(onlyDouble)
		self.rotZ = QtGui.QLineEdit('0')
		self.rotZ.setValidator(onlyDouble)

		# buttonBox = QtGui.QDialogButtonBox()
		buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
		buttonBox.addButton(option1Button, QtGui.QDialogButtonBox.ActionRole)
		buttonBox.addButton(option2Button, QtGui.QDialogButtonBox.ActionRole)
		#
		posLabelLayout = QtGui.QHBoxLayout()
		posLabelLayout.addWidget(labelPosition)

		posValueLayout = QtGui.QHBoxLayout()
		posValueLayout.addWidget(QtGui.QLabel('X'))
		posValueLayout.addWidget(self.posX)
		posValueLayout.addWidget(QtGui.QLabel('Y'))
		posValueLayout.addWidget(self.posY)
		posValueLayout.addWidget(QtGui.QLabel('Z'))
		posValueLayout.addWidget(self.posZ)

		rotLabelLayout = QtGui.QHBoxLayout()
		rotLabelLayout.addWidget(labelRotation)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(QtGui.QLabel('X'))
		hbox.addWidget(self.rotX)
		hbox.addWidget(QtGui.QLabel('Y'))
		hbox.addWidget(self.rotY)
		hbox.addWidget(QtGui.QLabel('Z'))
		hbox.addWidget(self.rotZ)


		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addLayout(posLabelLayout)
		mainLayout.addLayout(posValueLayout)
		mainLayout.addLayout(rotLabelLayout)
		mainLayout.addLayout(hbox)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		# define window   xLoc,yLoc,xDim,yDim
		self.setGeometry( 250, 250, 0, 50)
		self.setWindowTitle("Create a hinge joint")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	def onOption1(self):
		self.retStatus = 1
		self.close()

	def onOption2(self):
		self.retStatus = 2
		self.close()

def routine1():
	print("create!")

def routine2():
	print("abort!")

class Joint:
	def __init__(self, obj,parent,child):
		'''"App two point properties"'''
		obj.addProperty("App::PropertyString","Parent","Joint").Parent = parent.Name
		obj.addProperty("App::PropertyString","Child","Joint").Child = child.Name
		obj.addProperty("App::PropertyAngle","Angle1","Joint","Angle1 of joint").Angle1 = 90
		obj.addProperty("App::PropertyVector","axis","rotation","End point").axis=FreeCAD.Vector(1,0,0)
		obj.Proxy = self

	def execute(self, fp):
		'''"Print a short message when doing a recomputation, this method is mandatory" '''
		fp.Shape = Part.makeSphere(1)

class ViewProviderJoint:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.ShapeColor=(1.0,0.0,0.0)
		obj.Proxy = self

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Flat Lines"


class CreateJoint:
	"""RC_CreateJoint"""

	def GetResources(self):
		print(FreeCAD.getUserAppDataDir()+"Mod" + "/RobotCreator/icons/createJoint.png")
		return {'Pixmap'  : str(FreeCAD.getUserAppDataDir()+"Mod" + "/RobotCreator/icons/createJoint.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+j", # a default shortcut (optional)
			'MenuText': "Create a joint",
			'ToolTip' : "Create a joint"}

	def Activated(self):
		print("creating a joint")

		selection = Gui.Selection.getSelection()
		if len(selection) == 2:
			form = CreateHingeJointForm()
			form.exec_()
			if form.retStatus==1:
				routine1()
				j=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Joint")
				Joint(j,selection[0],selection[1])
				j.Placement.Base = FreeCAD.Vector(float(form.posX.text()),float(form.posY.text()),float(form.posZ.text()))
				j.axis = FreeCAD.Vector(float(form.rotX.text()),float(form.rotY.text()),float(form.rotZ.text()))
				ViewProviderJoint(j.ViewObject)
				App.ActiveDocument.recompute() 
			elif form.retStatus==2:
				print("abort!")
		else:
			print("Only support selection of two elements on two different objects")

	def IsActive(self):
		"""Here you can define if the command must be active or not (greyed) if certain conditions
		are met or not. This function is optional."""
		return True

FreeCADGui.addCommand('RC_CreateJoint',CreateJoint()) 

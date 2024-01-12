import FreeCAD
from .. import common
from ..RD_utils import initialize_element_tree

from PySide import QtCore

class link_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
        
#gravity   
    @property
    def gravity(self):
        
        state= self.ui.link_gravity_checkbox.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
        
    @gravity.setter
    def gravity(self,state):
        if state=='true':
            self.ui.link_gravity_checkbox.setCheckState(QtCore.Qt.Ckecked)
        else:
            self.ui.link_gravity_checkbox.setCheckState(QtCore.Qt.Unchecked)
            
#enable wind
    @property
    def enable_wind(self):
        state=self.ui.link_enable_wind_checkbox.isChecked(QtCore.Qt.Checked)
        if state:
            return str('true')
        else:
            return str('false')
        
    @enable_wind.setter
    def enable_wind(self,state):
        if state=='true':
            self.ui.link_enable_wind_checkbox.setCheckState(QtCore.Qt.Ckecked)
        else:
            self.ui.link_enable_wind_checkbox.setCheckState(QtCore.Qt.Unchecked)

#self_collide
    @property
    def self_collide(self):
        return str('true') if self.ui.link_self_collide_checkbox.isChecked() else str('false')

    @self_collide.setter
    def self_collide(self,state):
        self.ui.link_self_collide_checkbox.setCheckState(QtCore.Qt.Ckecked) if state=='true' else self.ui.link_self_collide_checkbox.setCheckState(QtCore.Qt.Unchecked)
        
#kinematic
    @property
    def kinematic(self):
        return str('true') if self.ui.link_kinematic_checkbox.isChecked() else str('false')
    @kinematic.setter
    def kinematic(self,state):
        self.ui.link_kinematic_checkbox.setCheckState(QtCore.Qt.Ckecked) if state=='true' else self.ui.link_kinematic_checkbox.setCheckState(QtCore.Qt.Unchecked)
        
#velocity decay 
    #linear
    @property
    def linear(self):
       return  self.ui.velocity_decay_linear_sp.value()
    @linear.setter
    def linear(self,value):
        self.ui.velocity_decay_linear_sp.setValue(value)

    #angular
    @property
    def angular(self):
       return  self.ui.link_angular_vel_decay_sp.value()
    @angular.setter
    def angular(self,value):
        self.ui.link_angular_vel_decay_sp.setValue(value)
#======================
#link
#====================
class link:
    def __init__(self,ui,elem_struct):
        self.ui=ui
        self.file_name='link.sdf'
        self.tag='link'
        #models will be store as children of sdf 
        self.parent_path=['sdf','model']
        self.properties=link_properties(self.ui)
        self.link_element=initialize_element_tree.convdict_2_tree(self.file_name)
        self._root_dict=elem_struct
        self.configUI()
        
    def configUI(self):
        self.ui.link_gravity_checkbox.stateChanged.connect(self.onGravity)
        self.ui.link_enable_wind_checkbox.stateCahanged.connect(self.onEnableWind)
        self.ui.ink_self_collide_checkbox.stateChanged.connect(self.onSelfCollide)
        self.ui.link_kinematic_checkbox.stateChanged.conned(self.onKinematic)
        self.ui.velocity_decay_linear_sp.clicked.connect(self.onLinear)
        self.ui.link_angular_vel_decay_sp.clicked.connect(self.onAngular)
        
    def onGravity(self):
        common.set_xml_data(self.link_element,'gravity',False,self.properties.gravity)
    
    def onEnableWind(self):
        common.set_xml_data(self.link_element,'enable_wind',False,self.properties.enable_wind)
        
    def onSelfCollide(self):
        common.set_xml_data(self.link_element,'self_collide',False,self.properties.self_collide)
        
    def onKinematic(self):
        common.set_xml_data(self.link_element,'kinematic',False,self.properties.kinematic)
        
    def onLinear(self):
        common.set_xml_data(self.link_element,'linear',False,self.properties.linear)
        
    def onAgular(self):
        common.set_xml_data(self.link_element,'angular',False,self.properties.angular)
    
    #element to be updaed sent to the list 
    def UpdateUi(self,element):
        self.properties.gravity=common.get_xml_data(element,'gravity',False)
        self.properties.enable_wind=common.get_xml_data(self.element,'enable_wind',False)
        self.properties.self_collide=common.get_xml_data(element,'self_collide',False)
        self.properties.kinematic= common.get_xml_data(element,'kinematic')
        self.properties.linear=common.set_xml_data(element,'linear')
        self.properties.angular=common.set_xml_data(element,'angular')
    
    #this needs to reset the  data of all links in the model 
    #how will this information be extracted 
    def reset(self,default=True):
        if default:
            self.link_element=initialize_element_tree.convdict_2_tree(self.file_name)
        else:
            elem_dict=common.parse_dict(self._root_dict,self.parent_path+[self.tag])
            
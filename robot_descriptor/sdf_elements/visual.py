from .. import common
import copy
import FreeCAD,FreeCADGui
from PySide2 import QtCore
from ..RD_utils import initialize_element_tree
import xml.etree.ElementTree as ET
import os 

from . import material

class visual_properties:
    def __init__(self,ui):
        self.ui=ui
#shadows        
    @property
    def cast_shadows(self):
        return  str('true') if self.ui.visual_cast_shadows_checkBox.isChecked() else str('false')
    @cast_shadows.setter
    def cast_shadows(self,state):
        self.ui.visual_cast_shadows_checkBox.setCheckState(QtCore.Qt.Checked) if state=='true' else self.ui.visual_cast_shadows_checkBox.setCheckState(QtCore.Qt.Unchecked)
    
#transparency     
    @property
    def transparency(self):
        return self.ui.visual_transparency_sp.value()
    @transparency.setter
    def transparency(self,val):
        self.ui.visual_transparency_sp.setValue(val)
#laser retro      
    @property
    def laser_retro(self):
        return self.ui.visual_laser_retro_sp.value()
    @laser_retro.setter
    def laser_retro(self,value):
        self.ui.visual_laser_retro_sp.setValue(value)

#visibility flags       
    @property
    def visibility_flags(self):
        return self.ui.visual_visibility_flags_sp.value()
    @visibility_flags.setter
    def visibility_flags(self,value):
        print(value)
        self.ui.visual_visibility_flags_sp.setValue(value)
    
#check boxes 
    @property
    def visual_laser_retro_cb(self):
        return self.ui.visual_laser_retro_cb.isChecked()
    
    @property
    def visual_transparency_cb(self):
        return self.ui.visual_transparency_cb.isChecked()
    
    @property
    def visual_visibility_flags_cb(self):
        return self.ui.visual_visibility_flags_cb.isChecked()
    

#=============
#====================
class visual:
    def __init__(self,parent_ui):
        self.ui=parent_ui
        self.file_name="visual.sdf"
        self._visual_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=visual_properties(self.ui)
        #maertial 
        self._material_ui=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,"material.ui"))
        self._material_cls=material.material(self._material_ui)
        #add widget to parent widget 
        self.ui.material_scroll.setWidget(self._material_ui.widget)
        self.configUI()
        self.updateUI()
        
        
  
    def configUI(self):
        self.ui.visual_laser_retro_sp.valueChanged.connect(self.on_laser_retro)
        self.ui.visual_transparency_sp.valueChanged.connect(self.on_transparency)
        self.ui.visual_visibility_flags_sp.valueChanged.connect(self.on_visibility_flags)
        self.ui.visual_cast_shadows_checkBox.stateChanged.connect(self.on_cast_shadows)
        
    def on_laser_retro(self):
        element=self._visual_elem
        common.set_xml_data(element,"laser_retro",False,self.properties.laser_retro)
        
    def on_transparency(self):
        element=self._visual_elem
        common.set_xml_data(element,"transparency",False,self.properties.transparency)
        
    def on_visibility_flags(self):
        element=self._visual_elem
        common.set_xml_data(element,"visibility_flags",False,self.properties.visibility_flags)
        
    def on_cast_shadows(self):
        element=self._visual_elem
        common.set_xml_data(element,"cast_shadows",False,self.properties.cast_shadows)
        
    
    def updateUI(self):
        self.properties.laser_retro=common.get_xml_data(self._visual_elem,"laser_retro",False)
        self.properties.transparency=common.get_xml_data(self._visual_elem,"transparency",False)
        #this causes an overflow  so dont update for now , ui is also disabled ,
        # t
        # self.properties.visibility_flags=common.get_xml_data(self._visual_elem,"visibility_flags",False)
        self.properties.cast_shadows=common.get_xml_data(self._visual_elem,"cast_shadows",False)
        
    def update_elements(self,item):
        self._visual_elem=item._visual_element
        self._material_cls.update_elements(item)
        self.updateUI()
        
    @property
    def element(self):
        t_visual_elem=copy.deepcopy(self._visual_elem)
        visual_pairs={"laser_retro":"visual_laser_retro_cb","transparency":"visual_transparency_cb","visibility_flags":"visual_visibility_flags_cb"}
        for tag  in visual_pairs.keys():
            if not getattr(self.properties,visual_pairs[tag]):
                t_visual_elem.remove(t_visual_elem.find(tag))
        if t_visual_elem.find("material") is None:
            t_visual_elem.append(self._material_cls.element)
        return t_visual_elem
        
    
from ..RD_utils import initialize_element_tree
from .. import common
from . import surface
import copy
import os 
import xml.etree.ElementTree as ET
import FreeCADGui 


class  collision_properties:
    def __init__(self,ui):
        self.ui=ui
#laser retro     
    @property
    def laser_retro(self):
        return self.ui.collision_laser_retro_sp.value()
    @laser_retro.setter
    def laser_retro(self,value):
        self.ui.collision_retro_sp.setValue(value)
        
#max contacts 
    @property 
    def max_contacts(self):
        return self.ui.collision_max_contacts_sp.value()
    @max_contacts
    def max_contacts(self,value):
        self.ui.collision_max_contacts_sp.setValue(value)
        
#checkboxes 
    @property
    def collision_laser_retro_cb(self):
        return self.ui.collision_laser_retro_cb.isChecked()
    
    @property
    def collison_max_contacts_cb(self):
        return self.ui.collison_max_contacts_cb.isChecked()
    

    
class collison:
    def __init__(self,parent_ui):
        #model editor ui 
        self.ui=parent_ui
        self.tag='collision'
        self.parennt_path=''
        self.properties=collision_properties(self.ui)
        self.file_name='collision.sdf'
        self.collision_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        #surface element 
        self.surface_ui=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,"surface.ui"))
        self.surface_elem=surface.surface(self.surface_ui)
        #add widget to parent 
        self.ui.collision_scroll.setWidget(self.surface_ui.widget)
        
        self.configUI()
        
    def configUI(self):
        self.ui.collision_max_contacts_sp.valueChanged.connect(
            lambda collision_elem=self.collision_elem: common.set_xml_data(collision_elem,"max_contacts",False,self.properties.max_contacts)
            )
        self.ui.collision_laser_retro_sp.valueChanged.connect(
            lambda collision_elem=self.collision_elem: common.set_xml_data(collision_elem,"laser_retro",False,self.properties.laser_retro)
            )
        
    def updateUI(self):
        data=["max_contacts","laser_retro"]
        for item in data:
            setattr(self.properties,item,common.get_xml_data(self.collision_elem,item,False))
    
    def update_elem(self,elem:ET.Element):
        surf=elem.find("surface")
        if surf is not None:
            self.surface_elem.update_elem(surf)
            elem.remove(surf)
            self.collision_elem=elem
            
    def reset(self):
        pass
    
    @property
    def element(self):
        t_collision_elem=copy.deepcopy(self.collision_elem)
        if not  self.properties.collision_laser_retro_cb:
            t_collision_elem.remove("laser_retro")
        
        if not self.properties.collison_max_contacts_cb:
            t_collision_elem.remove("max_contacts")
        
        t_surface=self.surface_elem.element
        
        return t_collision_elem.append(t_surface)
    
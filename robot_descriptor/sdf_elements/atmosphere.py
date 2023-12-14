from  .. import RD_globals 
#reponsible for creating an element tree using xml.etree
from ..RD_parser import  initialize_element_tree
import xml.etree.ElementTree as ET

import FreeCAD

class atmosphere_properties:
    def __init__(self,ui_form):
            self._ui_form=ui_form
            
    @property
    def type(self):
        return self.form.atm_type.currentText()
    
    #optional property 
    #check for None 
    @type.setter
    def type (self,atm_txt):
        '''currently atm text can only be  adiabatic'''
        if atm_txt!=None:
            lst={'adiabatic':0}
            self._ui_form.setCurrentIndex(lst[atm_txt])
        else:
            pass
#temperature  
    @property
    def temperature(self):
        '''returns none if group id disabled'''
        return self._ui_form.atm_temp.value()
    #optional property check for none
         
    @temperature.setter
    def temperature(self,temp:float):
        if temp!=None:
            self._ui_form.atm_temp.setValue(temp)
        else:
            pass
#pressure 
    @property
    def pressure(self):
            return self._ui_form.atm_pressure.value()
    #optional property ,check for none 
    @pressure.setter
    def pressure(self,temp:float):
        if temp!=None:
            self._ui_form.atm_pressure.setValue(temp)
        else:
            pass
#temperature gradient 
    @property
    def temp_gradient(self):
        return self._ui_form.atm_temp_grad.value()
    #optional property ,check for none
    @temp_gradient.setter
    def temp_gradient(self,grad:float):
        if grad!=None:
            self._ui_form.atm_temp_grad.setValue(grad)
        else:
            pass
    
    def checked(self):
        return self._ui_form.atmosphere_group.isChecked()
    
#==============================================================
#atmosphere 
#===============================================================
class atmosphere:
    def __init__(self,ui):
        self.ui=ui
        self.parent_path=['sdf','world']
        self.tag="atmosphere"
        self.file_name="atmosphere.sdf"
#initialize properties before reset
        self.properties=atmosphere_properties(ui)
#get world element 
        self._atm_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
    
        self.configUI()
#update ui with previously configured values if available      
        self.reset(default=False)
        
    def configUI(self):
        self.ui.atm_temp.valueChanged.connect(self.on_atm_temp)
        self.ui.atm_type.currentIndexChanged.connect(self.on_type_change)
        self.ui.atm_pressure.valueChanged.connect(self.on_atm_pressure)
        self.ui.atm_temp_grad.valueChanged.connect(self.on_temp_gradient)
#callbacks
    def on_atm_temp(self):
        RD_globals.set_xml_data(self._atm_elem,"temperature",False,self.properties.temperature)
        
        
    def on_type_change(self):
        RD_globals.set_xml_data(self._atm_elem,"atmosphere",True,{"type":self.properties.type})
        
    def on_atm_pressure(self):
        RD_globals.set_xml_data(self._atm_elem,"pressure",False,self.properties.pressure)
        
    
    def on_temp_gradient(self):
        RD_globals.set_xml_data(self._atm_elem,"temperature_gradient",False,self.properties.temp_gradient)
#end callbacks 
    def update_ui(self): 
        self.properties.temperature=float(RD_globals.get_xml_data(self._atm_elem,"temperature",False))
        self.properties.pressure=float(RD_globals.get_xml_data(self._atm_elem,"pressure",False))
        self.properties.temp_gradient=float(RD_globals.get_xml_data(self._atm_elem,"temperature_gradient",False))
        
#the reset method should also be used for extracting  previously configured values 

    def reset(self,default:bool=True):
        '''this method will be used to restore the element tree\n
         basically it undos  the update_elem method'''
        if default:
            self._atm_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        else:
#update  to allow  for retrieval of values from RD_Description
#use RD_globals parse dict to get the element
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=RD_globals.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict!=None:
                el_str=el_dict['elem_str']
                RD_globals.merge_elements(self._atm_elem,ET.fromstring(el_str))  
                
            else:
                pass
                      
        self.update_ui()
     
    def is_checked(self):
        status=self.ui.atmosphere_group.isChecked()
        return status
    @property 
    def atmosphere_element(self):
        '''returns the atmosphere property if the groupbox is checked and none otherwise'''
        if self.is_checked():
            return self._atm_elem
        else:
            None

       
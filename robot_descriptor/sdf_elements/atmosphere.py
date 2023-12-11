from  .. import RD_globals 
#reponsible for creating an element tree using xml.etree
from ..RD_parser import  initialize_element_tree



class atmosphere_properties:
    def __init__(self,ui_form):
            self._ui_form=ui_form
            
    @property
    def type(self):
        return self.form.atm_type.currentText()
    
    @type.setter
    def type (self,atm_txt):
        '''currently atm text can only be  adiabatic'''
        lst={'adiabatic':0}
        self._ui_form.setCurrentIndex(lst[atm_txt])
#temperature  
    @property
    def temperature(self):
        '''returns none if group id disabled'''
        return self._ui_form.atm_temp.value()
         
    @temperature.setter
    def temperature(self,temp:float):
        self._ui_form.atm_temp.setValue(temp)
#pressure 
    @property
    def pressure(self):
            return self._ui_form.atm_pressure.value()
    @pressure.setter
    def pressure(self,temp:float):
        self._ui_form.atm_pressure.setValue(temp)
#temperature gradient 
    @property
    def temp_gradient(self):
        return self._ui_form.atm_temp_grad.value()
      
    @temp_gradient.setter
    def temp_gradient(self,grad:float):
        self._ui_form.atm_temp_grad.setValue(grad)
    
    def checked(self):
        return self._ui_form.atmosphere_group.isChecked()
    
    
class atmosphere:
    def __init__(self,ui):
        self.ui=ui
        self.parent_path=['sdf','world']
        self.tag="atmosphere"
        self.file_name="atmosphere.sdf"
        self._atm_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=atmosphere_properties(ui)
       
        self.configUI()
        self.update_ui()
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
    def reset(self):
        '''this method will be used to restore the element tree\n
         basically it undos  the update_elem method'''
        self._atm_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
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
        

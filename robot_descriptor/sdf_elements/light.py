import xml.etree.ElementTree as ET
from PySide import QtCore
import FreeCAD


class light_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#name     
    @property
    def name(self):
        return self.ui.light_name.text()
    @name.setter
    def name(self,text):
        self.ui.light_name.setText(text)
    
#type 
    @property
    def type(self):
        return self.ui.light_type.currentText()
    @type.setter
    def type(self,text:str):
        self.ui.light_type.setCurrentText(text)
        
#intensity 
    @property
    def intensity(self):
        return self.ui.intensity_sp.value()

    @intensity.setter
    def intensity(self,value):
        self.ui.intensity_sp.setValue(value)

#light on 
    @property
    def light_on(self):
        state= self.ui.light_on_check_b.checkState()
        if state:
            return 1
        else:
            return 0
    @light_on.setter
    def light_on(self,state:bool):
        if state:
            self.ui.light_on_check_b.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.light_on_check_b.setCheckState(QtCore.Qt.UnChecked)
    
    
        
class light:
    def __init__(self,ui) -> None:
        self.ui=ui
        
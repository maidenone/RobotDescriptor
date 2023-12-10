
import xml.etree.ElementTree as ET
from ..RD_parser import initialize_element_tree


class physics_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
        
    @property
    def name(self):
        pass
    
    
class physics:
    def __init__(self,ui) -> None:
        self.parent_tag="world"
        self.ui=ui
        self.file_name="physics.sdf"
        self.physics_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=physics_properties()
    
    

from .. import RD_globals

from . import  RD_parse_sdf
    
import xml.etree.ElementTree as ET


class convdict_2_tree:
    def __init__(self,sfile:str):
        '''sfile : file name to read the element properties from  located in ../sdf \n
        use the get_elem  property  to get the initialized element '''
        #initialize class
        self.struct_class=RD_parse_sdf.sdf_parse(file=sfile)
        #get the dictionary structure
        self.structured=self.struct_class.data_structure
        #a stack of parent elements
        #this stack is provided to allow for  having a parent  key in the dictionary 
        #to help when creating an xnl tree by adding subnode 
       
        #get stuff started 
        self.create_root()
        self.construct_tree(self._root_elem,self.structured["children"])
    
        self.e_tree=ET.ElementTree(self._root_elem)
    #create the root element 
    #this does not need other properties as it does not have them ,this I'm sure of 
    #so no need to add them
    def create_root(self)->ET.Element:
        self._root_elem=ET.Element(self.structured["tag"])
        if self.structured["attributes"] is not None:
            for attr in self.structured["attributes"]:
                self._root_elem.set(attr.name,attr.attr_value)
        
    def construct_tree(self,parent_elem:ET.Element,st_lst)->ET.Element:
        
        attr=dict()
        for child in st_lst:
            if child["attributes"] is not None:
                for _att in child["attributes"]:
            #recall  attributes are stored as class Element_attributes defined in RD_parse_sdf.py
                    attr[_att.name]=_att.attr_value
            s=ET.SubElement(parent_elem,child["tag"],attr)
            if child["value"] is not None:
                s.text=child["value"]
            if len(child["children"]) >0:
                self.construct_tree(s,child["children"])
    @property
    def get_tree(self)->ET.ElementTree:
        return self.e_tree
    @property
    def get_element(self)->ET.Element:
        return self._root_elem
    
if __name__=="__main__":
    t=convdict_2_tree("world.sdf")
    tree=t.get_tree
    elm=t.get_elements
    e_elem=RD_globals.set_xml_data('linear_velocity',elm,False,[12,9,8])
    e_elem_t=ET.ElementTree(e_elem)
    tree.write("out.xml",encoding='utf8',xml_declaration=True)
    e_elem_t.write("out.xml",encoding='utf8',xml_declaration=True)
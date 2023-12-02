'''
This contains variables and functions that will be used globally \n
by many functions 
functions:\n
set_xml_data()
get_xml_data

variable:
UI_PATH
ICON_PATH

'''

import os 
import FreeCAD
import xml.etree.ElementTree as ET

import re
from typing import Union
ICON_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/icons"
UI_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/forms"
_DOCUMENT=FreeCAD.ActiveDocument

#will be used to extract vectors from element types
def extract_vector_n(input_string):
    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', input_string)
    return [float(num) for num in numbers]

#define and exception()
class tag_not_found(Exception):
    pass
# this will check if a string is a vector of numbers 
# will be used bu get_xml_content to validate objects of type vector3,pose ... e.t.c
def assert_vect(s):
    return bool(re.match(r'^\d+(\s+\d+)*$', s))

#The is attribute parameter id used to determine how the 
#value will be handled i.e what ET method will be used to update the values 
# 
def set_xml_data(tag:str,element:ET.Element,Is_Attribute:bool,value:Union[dict,float,int,list,str])->ET.Element:
    '''
    tag is the tag name of the element to be edited \n
    Is Attribute  can either be true or false , True if th value is an attribute \n
    if Is_Attribute is True value has to be a dictionary with one or more elements \n
    The value parameter will contain the actual value to be updated
    '''
    #get the affected element
    elem_tag=element.find(tag)
    if elem_tag ==None:
        print("tag not found: function set_xml_data")
        raise tag_not_found
        return
    else:
        pass
    # ensure no dictionaries are sent for non attributes 
    if Is_Attribute== False and isinstance(value,dict)== False:
        if isinstance(value,list):
            # equivalent string 
            string_eq=' '.join(map(str,value))
            elem_tag.text=string_eq
        else:
            elem_tag.text=str(value)
    else:
        for key in dict(value).keys:
            elem_tag.set(key,value[key])
    return element
            
def get_xml_data(tag:str,element:ET.Element,Is_Attribute:bool,subElement:Union[str,None])->Union[list,dict,str]:
    '''
    see set_xml_data()
    The functions have  similar parameters
    except for the value parameter
    '''
    def get_value(elem:ET.Element):
        if assert_vect(elem):
            # equivalent string 
            vect_eq=extract_vector_n(elem)
            return vect_eq
        else:
            #the caller will handle the conversion of this value to the relevant data type 
            return elem
        
    elem_tag=element.find(tag)
    if elem_tag ==None:
        print("tag not found: function get_xml_data")
        raise tag_not_found
        return
    else:
        pass
    if Is_Attribute== False:
        if subElement==None:
            txt=elem_tag.text()
            return get_value(txt)
        else:
            elem_child=elem_tag.find(subElement)
            return   get_value(elem_child)
    else:
        # return the  the attribute dictionary 
        if subElement==None:
            return  elem_tag.attrib()
        else:
            elem_child=elem_tag.find(subElement)
            return   elem_child.attrib()

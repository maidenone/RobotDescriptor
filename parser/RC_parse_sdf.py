import xml.etree.ElementTree as ET
import os 
import FreeCAD 

_dir=os.path.join(FreeCAD.getUserAppDataDir(),"Mod","RobotCreator","Resources","formats","sdf")
class Element_Attribute:
    pass

class sdf_parse:
    def __init__(self,version='1.7',file='root.sdf'):
        #initialize directory with the root.sdf
        self.root_dir=os.path.join(_dir,version,file)
        #create a dictionary 
        self.Main_ElemDict={}
        #parse tree and store the result in local variable tree
        self.tree=self.parse_tree(self.root_dir)
        #get the root element 
        self.root=self.tree.getroot()
        #populate the dictionary with data 
       
        # call the tree with the parent  root element
        self.Main_ElemDict=self.populate_structure(self.root)
        
        #a stack of parent elements
        #this stack is provided to allow for  having a parent  key in the dictionary 
        #to help when creating an xnl tree by adding subnode 
        self.parent_stack=[]
        
    def populate_structure(self,Element):
        #add elements to structure 
        ElemDict={};
        # append alement to  list 
        self.parent_stack.append(Element)
        ElemDict["tag"]=Element.attrib["name"]
        #find all attributes and store them  in a list
        #this is due to some classes having multiple attributes 
        #store attibute dictionary and descritpion in a tuple 
        #there the first element is a dictionary of  of the attributes and 
        #the second element is a string of description
        #list to store class atrributes 
        self._attr=[]
        for result in Element.findall("attribute"):
            
            description=result.find("description").text
            self._attr.append((result.attrib,description))
        #check to see that attributes are not empty
        if len(self._attr)==0:
            ElemDict["attributes"]=None
        else:
            ElemDict["attributes"]=self._attr
        
        ElemDict["value"]=Element.text
        
        #set parent node
        if Element ==self.root:
            ElemDict["parent"]=None
        else:
            ElemDict["parent"]=self.parent_stack[-2]
              
        
        #some elements do not have default value and type so
        #checking if the data exists first before adding it
        # None is used if the following keys are not part of the attributes 
        
        #check fo type 
        if "type" in Element.attrib.keys:
            ElemDict["type"]=Element.attrib["type"]
        else:
             ElemDict["type"]=None

        #check for default
        if "default" in Element.attrib.keys:
            ElemDict["default"]=Element.attrib["default"]
        else:
             ElemDict["default"]=None
        
        #check for the required key 
        if "required" in Element.attrib.keys:
            ElemDict["required"]=Element.attrib["required"]
        else:
             ElemDict["required"]=None
        #now   loop  through every other children and store their data in the 
        #data in the children field 
        for child in Element:
            if child.tag =="include":
                #if model is 
                file=child.attrib["filename"]
                self.c_dir= self.root_dir=os.path.join(_dir,self.version,file)
            
                #child tree aka c_tree
                self.c_tree=self.parse_tree(self.c_dir)
                self._c_root=self.c_tree.getroot()
                ElemDict["children"].append(self.populate_structure(self._c_root))
            else:
                 ElemDict["children"].append(self.populate_structure(child))
        self.parent_stack.pop()         
        return ElemDict   
        
# parse and return tree structure
    def parse_tree(self,dir):
        with open(dir) as file:
            tr=ET.parse(file)
        return tr
    #property to be called to get the element dictionary structure 
    @property
    def Tree(self):
        return self.Main_ElemDict
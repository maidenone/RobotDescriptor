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
        self.ElemDict={}
        #parse tree and store the result in local variable tree
        self.tree=self.parse_tree(self.root_dir)
        #get the root element 
        self.root=self.tree.getroot()
        #populate the dictionary with data 
        
        # call the tree with the parent  root element
        self.populate_structure(self.root)
        
        #the first argument is the parent of the element
        #the second is the dictionary structure to store the data 
    def populate_structure(self,parent):
        #add elements to structure 
        
        self.ElemDict["tag"]=parent.attrib["name"]
        #find all attributes and store them  in a list
        #this is due to some classes having multiple attributes 
        #store attibute dictionary and descritpion in a tuple 
        #there the first element is a dictionary of  of the attributes and 
        #the second element is a string of description
        for result in parent.findall("attribute"):
            self._attr=[]
            description=result.find("description").text
            self._attr.append((result.attrib,description))
        self.ElemDict["attributes"]=self._attr
        self.ElemDict["value"]=parent.text
        
        #the parent node cannot have the root as itself 
        if self.root==parent:
            self.ElemDict["parent"]=None
        else:
            self.ElemDict["parent"]=parent
            
        
        #some elements do not have default value and type so
        #checking if the data exists first before adding it
        # None is used if the following keys are not part of the attributes 
        
        #check fo type 
        if "type" in parent.attrib.keys:
            self.ElemDict["type"]=parent.attrib["type"]
        else:
             self.ElemDict["type"]=None

        #check for default
        if "default" in parent.attrib.keys:
            self.ElemDict["default"]=parent.attrib["default"]
        else:
             self.ElemDict["default"]=None
        
        #check for the required key 
        if "required" in parent.attrib.keys:
            self.ElemDict["required"]=parent.attrib["required"]
        else:
             self.ElemDict["required"]=None
        #now   loop  through every other children and store their data in the 
        #data in the children field 
        for child in parent:
            if child.tag =="include":
                file=child.attrib["filename"]
                self.c_dir= self.root_dir=os.path.join(_dir,self.version,file)
                
                #child tree aka c_tree
                self.c_tree=self.parse_tree(self.c_dir)
                self._c_root=self.c_tree.getroot()
                self.ElemDict["children"].append(self.populate_structure(self._c_root))
            else:
                 self.ElemDict["children"].append(self.populate_structure(parent))
                
        
# parse and return tree structure
    def parse_tree(self,dir):
        with open(dir) as file:
            tr=ET.parse(file)
        return tr
    #property to be called to get the element dictionary structure 
    @property
    def Tree(self):
        return self.ElemDict
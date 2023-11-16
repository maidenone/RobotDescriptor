import xml.etree.ElementTree as ET
import os 
import re
#import FreeCAD 

#_dir=os.path.join(FreeCAD.getUserAppDataDir(),"Mod","RobotCreator","Resources","formats","sdf")

_dir=os.path.join(os.path.expanduser("~"),'Documents',"RobotCreator","Resources","formats","sdf")

#this class will store element attributes to allow ease of access later 
class Element_Attributes:
    def __init__(self):
        self._name=""
        self._default=""
        self._type=""
        self._required=""
        self._description=""
        
    #name property
    @property
    def name(self):
       return self._name
    @name.setter
    def name(self,value):
        self._name=value
    
    #type property
    @property
    def type(self):
       return self._type
    @type.setter
    def type(self,value):
        self._type=value
    
    #default property
    @property
    def default(self):
       return self._default
    @default.setter
    def default(self,value):
        self._default=value
    
    #required property
    @property
    def required(self):
       return self._required
    @required.setter
    def required(self,value):
        self._required=value
    
    #description property
    @property
    def description(self):
       return self._description
    @description.setter
    def description(self,value):
        self._description=value

    #get a dictionary of all elements 
    def exatract_all(self):
        return {"name":self._name,"type":self._type,"default":self._default,"required":self._required,"description":self._description}
    #get only the name and default value 
    def extract_main(self):
        return {"name":self._name,"default":self._default}
        
#class to parse the sdf file and generate a dictioanary 
class sdf_parse:
    def __init__(self,version='1.7',file='root.sdf'):
        #initialize directory with the root.sdf
        self.root_dir=os.path.join(_dir,version,file)
        self.version=version
        #create a dictionary 
        self.Main_ElemDict={}
        #parse tree and store the result in local variable tree
        self.tree=self.parse_tree(self.root_dir)
        #get the root element 
        self.root=self.tree.getroot()
        
        
        #populate the dictionary with data 
        # call the tree with the parent  root element
        self.Main_ElemDict=self.populate_structure(self.root)
        
        
    def populate_structure(self,Element):
        #add elements to structure 
        ElemDict={}

        #skip child if name property is not available
        #considering the copydata element in plugin.sdf 
        #that should not be included 
        try:
            ElemDict["tag"]=Element.attrib["name"]
        except:        
            return ElemDict  
        
        #find all attributes and store them  in a list
        #this is due to some classes having multiple attributes 
        #store attibute dictionary and descritpion in a tuple 
        #there the first element is a dictionary of  of the attributes and 
        #the second element is a string of description
        #list to store class atrributes 
        self._attr=[]
        for result in Element.findall("attribute"):
            e=Element_Attributes()
            e.name=result.attrib["name"]
            e.type=result.attrib["type"]
            e.default=result.attrib["default"]
            e.required=result.attrib["required"]
            #remove whitespaces ,tabs and newline characters
            e.description=re.sub('\s+',' ',str(result.find("description").text).strip())
            self._attr.append(e)
        
        #check to see that attributes are not empty
        if len(self._attr)==0:
            ElemDict["attributes"]=None
        else:
            ElemDict["attributes"]=self._attr
       
        #some elements do not have default value and type so
        #checking if the data exists first before adding it
        # None is used if the following keys are not part of the attributes 
        #check fo type 
        if "type" in dict(Element.attrib):
            ElemDict["type"]=Element.attrib["type"]
        else:
             ElemDict["type"]=None
        #check for default
        if "default" in dict(Element.attrib):
            ElemDict["default"]=Element.attrib["default"]
        else:
             ElemDict["default"]=None
        
        #check for the required key 
        if "required" in dict(Element.attrib):
            ElemDict["required"]=Element.attrib["required"]
        else:
             ElemDict["required"]=None
        
        #create a children key
        ElemDict["children"]=[]
        #now   loop  through every other children and store their data in the 
        #data in the children field 
        for child in Element:
            if child.tag =="include":
                #if model is 
                file=child.attrib["filename"]
                self.c_dir=os.path.join(_dir,self.version,file)
            
                #child tree aka c_tree
                self.c_tree=self.parse_tree(self.c_dir)
                self._c_root=self.c_tree.getroot()
                _c=self.populate_structure(self._c_root)
                #dont add empty dictionaries
                #some elements will be skipped
                if len(_c) !=0:
                    ElemDict["children"].append(_c)
                    
            elif child.tag =="element":
                _c=self.populate_structure(child)
                if len(_c) !=0:
                    ElemDict["children"].append(_c)
            #add description item 
            elif child.tag =="description":
                ElemDict["description"]=re.sub('\s+',' ',str(child.text).strip())
            else:
               pass 
           
        return ElemDict   
        
# parse and return tree structure
    def parse_tree(self,dir):
        with open(dir) as file:
            tr=ET.parse(file)
        return tr
    #property to be called to get the element dictionary structure 
    @property
    def data_structure(self):
        return self.Main_ElemDict
     
if __name__=="__main__":  
    s=sdf_parse()
    d=s.data_structure
    print("done with this stage hopefully")
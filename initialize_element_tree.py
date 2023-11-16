import   RC_parse_sdf
import xml.etree.ElementTree as ET

INCLUDE_COMMENTS=False
# #to be used later 
 
#         #set parent node
#         if Element ==self.root:
#             #root element will have a none parent 
#             ElemDict["parent"]=None
#         else:
#             # the parent is most  probably be the previously added element 
#             ElemDict["parent"]=self.parent_stack[-2]

# #end
#convert dictionary to and element tree  that will be filled with data 
class convdict_2_tree:
    def __init__(self):
        #initialize class
        self.struct_class=RC_parse_sdf.sdf_parse()
        #get the dictionary structure
        self.structured=self.struct_class.data_structure
        #a stack of parent elements
        #this stack is provided to allow for  having a parent  key in the dictionary 
        #to help when creating an xnl tree by adding subnode 
        self.parent_stack=[]
        
        #get stuff started 
        self.create_root()
        self.construct_tree(self._root_elem,self.structured["children"])
        
    #create the root element 
    #this does not need other properties as it does not have them ,this I'm sure of 
    #so no need to add them
    def create_root(self):
        self._root_elem=ET.Element(self.structured["tag"])
        if self.structured["attributes"] != None:
            for attr in self.structured["attributes"]:
                self._root_elem.set(attr.name,attr.default)
        
        
    
    def construct_tree(self,parent_elem,st_lst):
        
        #add the root element to the list of parents 
        self.parent_stack.append(parent_elem)
        attr=dict()
        for child in st_lst:
            if child["attributes"] !=None:
                for _att in child["attributes"]:
                    attr[_att.name]=_att.default
            s=ET.SubElement(parent_elem,child["tag"],attr)
            if child["default"] !=None:
                s.text=child["default"]
            if len(child["children"]) >0:
                self.construct_tree(s,child["children"])
        
    def add_comment(self,tree_elem,comment:str):
        if INCLUDE_COMMENTS:
            self._root_elem.append(comment)
        else:
            pass
    
if __name__=="__main__":
    t=convdict_2_tree()
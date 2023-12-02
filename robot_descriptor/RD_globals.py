import os 
import FreeCAD

import re

ICON_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/icons"
UI_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/forms"
_DOCUMENT=FreeCAD.ActiveDocument

#will be used to extract vectors from element types
def extract_vector_n(input_string):
    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', input_string)
    return [float(num) for num in numbers]
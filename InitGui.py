from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math

class RobotCreator (Workbench):

    MenuText = "RobotCreator"
    ToolTip = "A description of my workbench"
    Icon = '''
/* XPM */
static char * C:\Program Files\FreeCAD 0_15\Mod\Fasteners\wbicon_xpm[] = {
"16 16 5 1",
" 	c None",
".	c #000000",
"+	c #03B83F",
"@	c #0D8132",
"#	c #034D1C",
"                ",
" .....    ..... ",
" .+@@.    .@@#. ",
" .+@@.    .@@#. ",
" .+@@......@@#. ",
" .+@@@@@@@@@@#. ",
" .+@@@@@@@@@@#. ",
" .+@@@@@@@@@@#. ",
" .............. ",
"     .+@@#.     ",
"     .+@@#.     ",
"     .+@@#.     ",
"     .+@@#.     ",
"     .+@@#.     ",
"     ......     ",
"                "};
'''

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import GazeboStlExport, MoveToCOM # import here all the needed files that create your FreeCAD commands
        self.list = ['RC_GazeboStlExport', 'RC_MoveToCOM'] # A list of command names created in the line above
        self.appendToolbar("RobotCreator",self.list) # creates a new toolbar with your commands
        self.appendMenu("My New Menu",self.list) # creates a new menu
        self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu
    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"

Gui.addWorkbench(RobotCreator())

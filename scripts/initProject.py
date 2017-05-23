import sys, os


projectName = "testProj"
robotName = "testRobot"

links = ["a","b","c"]

if not os.path.exists(projectName):
    os.makedirs(projectName)
 
os.chdir(projectName)

worldFile = open('testRobot'+'.world','w')
worldFile.write("<?xml version=\"1.0\"?>\n")
worldFile.write("  <sdf version=\"1.4\">\n")
worldFile.write("    <world name=\"default\">\n")
worldFile.write("\n")
worldFile.write("    <!-- A ground plane -->\n")
worldFile.write("    <include>\n")
worldFile.write("      <uri>model://ground_plane</uri>\n")
worldFile.write("    </include>\n")
worldFile.write("\n")
worldFile.write("    <!-- A global light source -->\n")
worldFile.write("    <include>\n")
worldFile.write("      <uri>model://sun</uri>\n")
worldFile.write("    </include>\n")
worldFile.write("\n")
worldFile.write("    <include>\n")
worldFile.write("      <uri>model://"+robotName+"</uri>\n")
worldFile.write("    </include>\n")
worldFile.write("\n")
worldFile.write("    </world>\n")
worldFile.write("  </sdf>\n")

sdfFile = open(robotName+'.sdf', 'w')
sdfFile.write('<?xml version=\"1.0\"?>\n')
sdfFile.write('<sdf version=\"1.5\">\n')
sdfFile.write('<model name=\"'+robotName+'\">\n')

objs = FreeCAD.ActiveDocument.Objects
for obj in objs:
	if obj.TypeId == PartDesign::Body:
		name = obj.Name
		com = obj.Shape.CenterOfMass
		mass = obj.Shape.Mass
		inertia = obj.Shape.MatrixOfInertia
		pos = obj.Shape.Placement

		sdfFile.write('<link name=\"'name'\">\n')
		sdfFile.write('<pose> ' + str(pos.Base[0]) + ' ' + str(pos.Base[1]) + ' ' + str(pos.Base[2])+ ' ' + str(pos.Rotation.toEuler()[0]) + ' ' + str(pos.Rotation.toEuler()[1])+ ' ' + str(pos.Rotation.toEuler()[2])+'</pose>\n')
		sdfFile.write('<inertial>\n')
		sdfFile.write('<pose> ' + str(pos.Base[0]) + ' ' + str(pos.Base[1]) + ' ' + str(pos.Base[2])+ ' ' + str(pos.Rotation.toEuler()[0]) + ' ' + str(pos.Rotation.toEuler()[1])+ ' ' + str(pos.Rotation.toEuler()[2])+'</pose>\n')
		sdfFile.write('<inertia>\n')
		sdfFile.write('<ixx>'+str(inertia.A11/1000)+'</ixx>\n')
		sdfFile.write('<ixy>'+str(inertia.A12/1000)+'</ixy>\n')
		sdfFile.write('<ixz>'+str(inertia.A13/1000)+'</ixz>\n')
		sdfFile.write('<iyy>'+str(inertia.A22/1000)+'</iyy>\n')
		sdfFile.write('<iyz>'+str(inertia.A23/1000)+'</iyz>\n')
		sdfFile.write('<izz>'+str(inertia.A33/1000)+'</izz>\n')
		sdfFile.write('</inertia>\n')
                sdfFile.write('<mass>'+str(mass/1000)+'</mass>\n')
		sdfFile.write('</inertial>\n')
		sdfFile.write('<collision name=\"collision\">\n')
		sdfFile.write('<geometry>\n')
		sdfFile.write('<mesh>\n')
		sdfFile.write('<uri>model://'+robotName+'/meshes/'+name+'.stl</uri>\n')
		sdfFile.write('</mesh>\n')
		sdfFile.write('</geometry>\n')
		sdfFile.write('</collision>\n')
		sdfFile.write('<visual name=\"visual\">\n')
		sdfFile.write('<geometry>\n')
		sdfFile.write('<mesh>\n')
		sdfFile.write('<uri>model://'+robotName+'/meshes/'+name+'.stl</uri>\n')
		sdfFile.write('</mesh>\n')
		sdfFile.write('</geometry>\n')
		sdfFile.write('</visual>\n')
		sdfFile.write('</link>\n')
sdfFile.write('</model>\n')
sdfFile.write('</sdf>\n')

sdfFile.close()


#    x  y  z
#
# x  xx xy xz
#
# y  xy yy yz
#
# z  xz zy zz


<?xml version="1.0"?>
<sdf version="1.4">
    <model name="simple_gripper">
        <link name="riser">
            <pose>-0.15 0.0 0.5 0 0 0</pose>
            <inertial>
                <pose>0 0 -0.5 0 0 0</pose>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>10.0</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.2 0.2 1.0</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.2 0.2 1.0</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Purple</script>
                </material>
            </visual>
        </link>
        <link name="palm">
            <pose>0.0 0.0 0.05 0 0 0</pose>
            <inertial>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>0.5</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Red</script>
                </material>
            </visual>
        </link>
        <link name="left_finger">
            <pose>0.1 0.2 0.05 0 0 -0.78539</pose>
            <inertial>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>0.1</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.1 0.3 0.1</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.1 0.3 0.1</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Blue</script>
                </material>
            </visual>
        </link>
        <link name="left_finger_tip">
            <pose>0.336 0.3 0.05 0 0 1.5707</pose>
            <inertial>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>0.1</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Blue</script>
                </material>
            </visual>
        </link>
        <link name="right_finger">
            <pose>0.1 -0.2 0.05 0 0 .78539</pose>
            <inertial>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>0.1</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.1 0.3 0.1</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.1 0.3 0.1</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Green</script>
                </material>
            </visual>
        </link>
        <link name="right_finger_tip">
            <pose>0.336 -0.3 0.05 0 0 1.5707</pose>
            <inertial>
                <inertia>
                    <ixx>0.01</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.01</iyy>
                    <iyz>0</iyz>
                    <izz>0.01</izz>
                </inertia>
                <mass>0.1</mass>
            </inertial>
            <collision name="collision">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
            </collision>
            <visual name="visual">
                <geometry>
                    <box>
                        <size>0.1 0.2 0.1</size>
                    </box>
                </geometry>
                <material>
                    <script>Gazebo/Green</script>
                </material>
            </visual>
        </link>
        <static>true</static>
    </model>
</sdf>


<?xml version="1.0" ?>
<sdf version="1.5">
<model name="baseBot">
  <!-- Give the base link a unique name -->
  <link name="base">

    <!-- Offset the base by half the lenght of the cylinder -->
    <pose>0 0 -0.005 0 0 0</pose>
    <inertial>
      <mass>1.2</mass>
      <inertia>
       <ixx>0.0010608477766732891</ixx>
       <iyy>-0.00023721360899498273</iyy>
       <izz>0.00024999999996488216</izz>
        <ixy>0</ixy>
        <ixz>0</ixz>
        <iyz>0</iyz>
      </inertia>
    </inertial>

    <collision name="base_collision">
      <geometry>
	     <mesh>
	       <!-- The URI should refer to the 3D mesh. The "model:"
		   URI scheme indicates that the we are referencing a Gazebo
		   model. -->
	       <uri>model://baseBot/meshes/plate.stl</uri>
	     </mesh>
      </geometry>
    </collision>

    <!-- The visual is mostly a copy of the collision -->
    <visual name="base_visual">
      <geometry>
	     <mesh>
	       <!-- The URI should refer to the 3D mesh. The "model:"
		   URI scheme indicates that the we are referencing a Gazebo
		   model. -->
	       <uri>model://baseBot/meshes/plate.stl</uri>
	     </mesh>
      </geometry>
    </visual>
  </link>

  <!-- Give the base link a unique name -->
  <link name="top">

    <!-- Vertically offset the top cylinder by the length of the bottom
        cylinder and half the length of this cylinder. -->
    <pose>0.00 0.00 0.005 0 0 0</pose>
   <inertial>
     <mass>0.1</mass>
     <inertia>
       <ixx>0.0010608477766732891</ixx>
       <iyy>-0.00023721360899498273</iyy>
       <izz>0.00024999999996488216</izz>
       <ixy>0</ixy>
       <ixz>0</ixz>
       <iyz>0</iyz>
     </inertia>
   </inertial>
    <collision name="top_collision">
      <geometry>
	     <mesh>
	       <uri>model://baseBot/meshes/holder.stl</uri>
	     </mesh>
      </geometry>
    </collision>

    <!-- The visual is mostly a copy of the collision -->
    <visual name="top_visual">
      <geometry>
	     <mesh>
	       <uri>model://baseBot/meshes/holder.stl</uri>
	     </mesh>
      </geometry>
    </visual>
  </link>

<!-- Each joint must have a unique name -->
<joint type="revolute" name="joint">

  <!-- Position the joint at the bottom of the top link -->
  <pose>0.00 0.00 -0.00048 0 0 0</pose>

  <!-- Use the base link as the parent of the joint -->
  <parent>base</parent>

  <!-- Use the top link as the child of the joint -->
  <child>top</child>

  <!-- The axis defines the joint's degree of freedom -->
  <axis>

    <!-- Revolve around the z-axis -->
    <xyz>0 0 1</xyz>

    <!-- Limit refers to the range of motion of the joint -->
    <limit>

      <!-- Use a very large number to indicate a continuous revolution -->
      <lower>-10000000000000000</lower>
      <upper>10000000000000000</upper>
    </limit>
  </axis>
</joint>
</model>
</sdf>

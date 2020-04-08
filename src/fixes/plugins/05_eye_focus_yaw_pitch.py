import re

proto2_eye_yaw_pitch='''
  <link
    name="eyes_link_pitch">
  </link>
  <joint
    name="eyes_pitch"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="-1.3878E-14 -6.9398E-15 -7.6286E-17" />
    <parent
      link="bone54" />
    <child
      link="eyes_link_pitch" />
    <axis
      xyz="0 -1 0" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="2.4"
      velocity="6.2832" />
  </joint>
  <link
   name="eyes_link_yaw">
   <visual>
      <origin
        xyz="0.3 0 0"
        rpy="0 0 0" />
      <geometry>
        <mesh
          filename="package://sweetie_bot_proto2_description/meshes/arrow.STL" />
      </geometry>
      <material
        name="">
        <color
          rgba="0.752941176470588 0.752941176470588 0.752941176470588 1" />
      </material>
    </visual>
  </link>
  <joint
    name="eyes_yaw"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="-1.3878E-14 -6.9398E-15 -7.6286E-17" />
    <parent
      link="eyes_link_pitch" />
    <child
      link="eyes_link_yaw" />
    <axis
      xyz="0 0 -1" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="2.4"
      velocity="6.2832" />
  </joint>
'''

proto3_eye_yaw_pitch='''
  <link
    name="eyes_link_pitch">
  </link>
  <joint
    name="eyes_pitch"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="-1.3878E-14 0.76 -7.6286E-17" /> <!-- -6.9398E-15  -->
    <parent
      link="head_link4" />
    <child
      link="eyes_link_pitch" />
    <axis
      xyz="0 -1 0" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="2.4"
      velocity="6.2832" />
  </joint>
  <link
   name="eyes_link_yaw">
   <visual>
      <origin
        xyz="0.3 0 0"
        rpy="0 0 0" />
      <geometry>
        <mesh
          filename="package://sweetie_bot_proto3_description/meshes/arrow.STL" />
      </geometry>
      <material
        name="">
        <color
          rgba="0.752941176470588 0.752941176470588 0.752941176470588 1" />
      </material>
    </visual>
  </link>
  <joint
    name="eyes_yaw"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="-1.3878E-14 -6.9398E-15 -7.6286E-17" />
    <parent
      link="eyes_link_pitch" />
    <child
      link="eyes_link_yaw" />
    <axis
      xyz="0 0 -1" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="2.4"
      velocity="6.2832" />
  </joint>
'''

class Plugin:
    name = "eye-focus"
    cmd_name = name
    cmd_letter = "e"
    display_name = "Add eyes focus and yaw pitch joints"
    enabled = True
    eyes_regexp = r'(<link[^>]+?name="eyes_link_(pitch|yaw)"[^>]*?>)([\s\S]+?<joint[^>]+?name="eyes_(pitch|yaw)"[\s\S]+?</joint>[\s\S]*?)'
    proto2_eye_right_sel  = '(<joint name="eye_right"[\s\S]*?</joint>)'
    proto3_eye_right_sel  = '(<joint name="eye_r_joint"[\s\S]*?</joint>)'

    def rollout(self, robot, filename, package_name):

      if robot.name.startswith("sweetie_bot_proto2"):
          eye_yaw_pitch = proto2_eye_yaw_pitch
          eye_right_sel = self.proto2_eye_right_sel
      elif robot.name.startswith("sweetie_bot_proto3"):
          eye_yaw_pitch = proto3_eye_yaw_pitch
          eye_right_sel = self.proto3_eye_right_sel
      else:
        return False

      with open(filename, 'r+') as f:
       urdf = f.read()

       #if bool(re.search(self.fcus_regexp, urdf)):
       # eye focus fix not needed
       #  return False

       urdf = re.sub(eye_right_sel, r'\1'+eye_yaw_pitch, urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()
      return True


    def rollback(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       #urdf = re.sub(self.fcus_regexp, '', urdf)
       urdf = re.sub(self.eyes_regexp, '', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()
      return True

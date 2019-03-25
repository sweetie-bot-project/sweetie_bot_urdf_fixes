import re

joint_eyes_focus = '''
  <link
    name="link_eyes_x">
  </link>
  <joint
    name="joint_eyes_focus_x"
    type="prismatic">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="bone54" />
    <child
      link="link_eyes_x" />
    <axis
      xyz="1 0 0" />
    <limit
      lower="-0.5"
      upper="0.5"
      effort="0.24"
      velocity="1.5708" />
  </joint>
  <link
    name="link_eyes_y">
  </link>
  <joint
    name="joint_eyes_focus_y"
    type="prismatic">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="link_eyes_x" />
    <child
      link="link_eyes_y" />
    <axis
      xyz="0 1 0" />
    <limit
      lower="-0.5"
      upper="0.5"
      effort="0.24"
      velocity="1.5708" />
  </joint>
  <link
    name="link_eyes_z">
    <visual>
      <origin
        xyz="0 0 0"
        rpy="0 0 0" />
      <geometry>
        <mesh
          filename="package://sweetie_bot_proto2_description/meshes/sphere.STL" />
      </geometry>
      <material
        name="">
        <color
          rgba="0.75294 0.75294 0.75294 1" />
      </material>
    </visual>
  </link>
  <joint
    name="joint_eyes_focus_z"
    type="prismatic">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="link_eyes_y" />
    <child
      link="link_eyes_z" />
    <axis
      xyz="0 0 1" />
    <limit
      lower="-0.5"
      upper="0.5"
      effort="0.24"
      velocity="1.5708" />
  </joint>
'''

eye_yaw_pitch='''
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
      effort="0.24"
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
      effort="0.24"
      velocity="6.2832" />
  </joint>
'''

class Plugin:
    name = "eye-focus"
    cmd_name = name
    cmd_letter = "e"
    display_name = "Add eyes focus and yaw pitch joints"
    enabled = False
    fcus_regexp = r'(<link[^>]+?name="link_eyes_[xyz]"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint_eyes_focus_[xyz]"[\s\S]+?</joint>[\s\S]*?)'
    eyes_regexp = r'(<link[^>]+?name="eyes_link_(pitch|yaw)"[^>]*?>)([\s\S]+?<joint[^>]+?name="eyes_(pitch|yaw)"[\s\S]+?</joint>[\s\S]*?)'

    def rollout(self, robot, filename):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(self.fcus_regexp, urdf)):
         # eye focus fix not needed
         return False

       eye_right_sel  = '(<joint[\s\S]*name="eye_right"[\s\S]*?</joint>)'
       urdf = re.sub(eye_right_sel, r'\1'+joint_eyes_focus+eye_yaw_pitch, urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()
      return True


    def rollback(self, robot, filename):
      with open(filename, 'r+') as f:
       urdf = f.read()

       urdf = re.sub(self.fcus_regexp, '', urdf)
       urdf = re.sub(self.eyes_regexp, '', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()
      return True

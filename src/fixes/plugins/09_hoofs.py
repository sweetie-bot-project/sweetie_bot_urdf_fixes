import re

proto2_hoof_template = '''
  <link
    name="bone{0}6">
  </link>
  <joint
    name="joint{0}6"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="bone{0}5" />
    <child
      link="bone{0}6" />
    <axis
      xyz="0 0 1" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="2.4"
      velocity="6.2832" />
  </joint>
  <link
    name="hoof{0}">
  </link>
  <joint
    name="joint_hoof{0}"
    type="fixed">
    <origin
      xyz="0 0 -0.03"
      rpy="0 0 0" />
    <parent
      link="bone{0}5" />
    <child
      link="hoof{0}" />
  </joint>
'''

proto3_hoof_template = '''
  <link
    name="leg{0}_link7">
  </link>
  <joint
    name="leg{0}_joint7"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="leg{0}_link6" />
    <child
      link="leg{0}_link7" />
    <axis
      xyz="0 0 1" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="0.24"
      velocity="6.2832" />
  </joint>
  <link
    name="hoof{0}">
  </link>
  <joint
    name="joint_hoof{0}"
    type="fixed">
    <origin
      xyz="0 0 -0.035"
      rpy="0 0 0" />
    <parent
      link="leg{0}_link6" />
    <child
      link="hoof{0}" />
  </joint>
'''

proto2_hoof_sel = r'(<link[^>]+?name="bone[1234]6"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint[1234]6"[\s\S]+?</joint>[\s\S]*?)(<link[^>]+?name="hoof[1234]"[^>]*?>)?([\s\S]+?<joint[^>]+?name="joint_hoof[1234]"[\s\S]+?</joint>)?'

proto3_hoof_sel = r'(<link[^>]+?name="leg[1234]_link7"[^>]*?>)([\s\S]+?<joint[^>]+?name="leg[1234]_joint7"[\s\S]+?</joint>[\s\S]*?)(<link[^>]+?name="hoof[1234]"[^>]*?>)?([\s\S]+?<joint[^>]+?name="joint_hoof[1234]"[\s\S]+?</joint>)?'

proto2_joint_sel  = '(<joint[^>]*name="joint{0}5"[\s\S]*?</joint>)'


proto3_joint_sel  = '(<joint[^>]*name="leg{0}_joint6"[\s\S]*?</joint>)'

class Plugin:
    name = "virtual-hoof-joints"
    cmd_name = name
    cmd_letter = "v"
    display_name = "Add virtual hoof joints"
    enabled = True
    only_for = ['sweetie_bot_proto3_description']

    def rollout(self, robot, filename, package_name):

      if robot.name.startswith("sweetie_bot_proto2"):
          hoof_template = proto2_hoof_template
          hoof_sel = proto2_hoof_sel
          joint_sel = proto2_joint_sel
      elif robot.name.startswith("sweetie_bot_proto3"):
          hoof_template = proto3_hoof_template
          hoof_sel = proto3_hoof_sel
          joint_sel = proto3_joint_sel
      else:
        return False

      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(hoof_sel, urdf)):
         # hoofs fix not needed
         return False

       for i in [1, 2, 3, 4]:
         urdf = re.sub(joint_sel.format(i), r'\1'+hoof_template.format(i), urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

    def rollback(self, robot, filename, package_name):

      if robot.name.startswith("sweetie_bot_proto2"):
          hoof_template = proto2_hoof_template
          hoof_sel = proto2_hoof_sel
          joint_sel = proto2_joint_sel
      elif robot.name.startswith("sweetie_bot_proto3"):
          hoof_template = proto3_hoof_template
          hoof_sel = proto3_hoof_sel
          joint_sel = proto3_joint_sel
      else:
        return False

      with open(filename, 'r+') as f:
       urdf = f.read()

       urdf = re.sub(hoof_sel, '', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

import re

bone55_56 = '''
  <link
    name="bone55">
  </link>
  <joint
    name="joint55"
    type="revolute">
    <origin
      xyz="0.12 0.0 -0.02"
      rpy="0 0 0" />
    <parent
      link="bone54" />
    <child
      link="bone55" />
    <axis
      xyz="0 0 1" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="0.24"
      velocity="6.2832" />
  </joint>
  <link
    name="bone56">
  </link>
  <joint
    name="joint56"
    type="revolute">
    <origin
      xyz="0 0 0"
      rpy="0 0 0" />
    <parent
      link="bone55" />
    <child
      link="bone56" />
    <axis
      xyz="0 1 0" />
    <limit
      lower="-1.5708"
      upper="1.5708"
      effort="0.24"
      velocity="6.2832" />
  </joint>
'''

jointx54_sel  = r'(<joint[\s\S]*name="joint5{0}"[\s\S]*?</joint>)'
nose_regexp = r'(<link[^>]+?name="bone5[56]"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint5[56]"[\s\S]+?</joint>[\s\S]*?)'

class Plugin:
    name = "nose-bones"
    cmd_name = name
    cmd_letter = "n"
    display_name = "Add nose bone55,56"
    enabled = False
    only_for = ['sweetie_bot_proto2_description']

    def rollout(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(jointx54_sel.format(5), urdf)):
         # nose bones fix not needed
         return False

       urdf = re.sub(jointx54_sel.format(4), r'\1'+bone55_56, urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True


    def rollback(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       urdf = re.sub(nose_regexp, '', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True


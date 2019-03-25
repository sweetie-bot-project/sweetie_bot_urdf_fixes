import re

hoof_template = '''
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
      xyz="0 0 -0.03"
      rpy="0 0 0" />
    <parent
      link="bone{0}5" />
    <child
      link="hoof{0}" />
  </joint>
'''

hoof_sel = r'(<link[^>]+?name="bone[1234]6"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint[1234]6"[\s\S]+?</joint>[\s\S]*?)(<link[^>]+?name="hoof[1234]"[^>]*?>)?([\s\S]+?<joint[^>]+?name="joint_hoof[1234]"[\s\S]+?</joint>)?'

class Plugin:
    name = "hoofs-joints"
    cmd_name = name
    cmd_letter = "h"
    display_name = "Add bone6 and hoof joints"
    enabled = False

    def rollout(self, robot, filename):

      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(hoof_sel, urdf)):
         # hoofs fix not needed
         return False

       jointx5_sel  = '(<joint[^>]*name="joint{0}5"[\s\S]*?</joint>)'
       for i in [1, 2, 3, 4]:
         urdf = re.sub(jointx5_sel.format(i), r'\1'+hoof_template.format(i), urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

    def rollback(self, robot, filename):

      with open(filename, 'r+') as f:
       urdf = f.read()

       urdf = re.sub(hoof_sel, '', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

import re

head_base = r'''\1
  <link
    name="head_base">
  </link>
  <joint
    name="head_base_joint"
    type="fixed">
    <parent
      link="head_link4" />
    <child
      link="head_base" />
    <axis
      xyz="0 0 0" />
    <origin
      xyz="0.0 0.0 0.0"
      rpy="0.0 0.463648 0.0" />
  </joint>'''

class Plugin:
    name = "head-base"
    cmd_name = name
    cmd_letter = "h"
    display_name = "Add head_base link and joint"
    enabled = True
    only_for = ['sweetie_bot_proto3_description']

    def rollout(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(r'<link[^>]*?name=\"head_base\"[^>]*?>', urdf)):
         # inertia fix not needed
         return False

       head_joint4_sel = r"(<joint\s.*?head_joint4[\s\S]*?</joint>)"
       urdf = re.sub(head_joint4_sel, head_base, urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

    def rollback(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if not bool(re.search(r'<link[^>]*?name="head_base"[^>]*?>', urdf)):
         # inertia rollback not neede
         return False

       head_base_sel = r'(<link\s.*?head_base[\s\S]*?</joint>)'
       urdf = re.sub(base_link_sel, r'\1'+'\n    '+r'\5\3', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True


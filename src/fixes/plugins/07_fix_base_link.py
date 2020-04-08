import re

inertia_template = r'''\1\3
  <link
    name="base_link_inertia">
    \2
  </link>
  <joint 
    name="fictive_base_joint" type="fixed">
      <parent link="base_link"/>
      <child link="base_link_inertia"/> 
  </joint>'''

class Plugin:
    name = "base-inertia"
    cmd_name = name
    cmd_letter = "i"
    display_name = "Fix base_link inertia warning"
    enabled = True

    def rollout(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if bool(re.search(r'<link[^>]*?name=\"base_link_inertia\"[^>]*?>', urdf)):
         # inertia fix not needed
         return False

       base_link_sel = r'(<link[\s\S]*?base_link">[\s\S]*?)(<inertial>[\s\S]*?</inertial>)([\s\S]*?</link>)'
       urdf = re.sub(base_link_sel, inertia_template, urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True

    def rollback(self, robot, filename, package_name):
      with open(filename, 'r+') as f:
       urdf = f.read()

       if not bool(re.search(r'<link[^>]*?name="base_link_inertia"[^>]*?>', urdf)):
         # inertia rollback not neede
         return False

       base_link_sel = r'(<link[\s\S]*?base_link">)()([\s\S]*?)(<link[\s\S]*?name="base_link_inertia">[\s\S]*?)(<inertial>[\s\S]*?</inertial>)([\s\S]*?</joint>)'
       urdf = re.sub(base_link_sel, r'\1'+'\n    '+r'\5\3', urdf)

       f.truncate(0)
       f.seek(0)
       f.write(urdf)
       f.close()

      return True


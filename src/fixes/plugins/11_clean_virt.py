import re

proto3_link_sel = r'<link name="(nose_link[12]|eye_[lr]_link|camera_link)">[\s\S]*?</link>'

link_template = r'<link name="\1"/>'

class Plugin:
    name = "clean-virtual-links"
    cmd_name = name
    cmd_letter = "e"
    display_name = "Clean virtual links"
    enabled = True
    only_for = ['sweetie_bot_proto3_description']

    def rollout(self, robot, filename, package_name):

      if robot.name.startswith("sweetie_bot_proto3"):
          link_sel = proto3_link_sel
      else:
        return False

      with open(filename, 'r+') as f:
        urdf = f.read()

        urdf = re.sub(link_sel, link_template, urdf)

        f.truncate(0)
        f.seek(0)
        f.write(urdf)
        f.close()

      return True


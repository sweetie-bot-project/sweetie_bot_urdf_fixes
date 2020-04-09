import re

class Plugin:
    name = "add-collision"
    cmd_name = name
    cmd_letter = "s"
    display_name = "Add collision STL"
    only_for = ["sweetie_bot_proto2_description"]
    enabled = True

    def rollout(self, robot, filename, package_name):
      if package_name in self.only_for:
        for link in robot.links:
          for collision in link.collisions:
            collision.geometry.filename = re.sub("(meshes/)(base|bone)([\w]*)(\.STL)", r"\1collision/\2\3\4", collision.geometry.filename)

    def rollback(self, robot, filename, package_name):
      if package_name in self.only_for:
        for link in robot.links:
          for collision in link.collisions:
            collision.geometry.filename = re.sub("/meshes/collision/", "/meshes/", collision.geometry.filename)

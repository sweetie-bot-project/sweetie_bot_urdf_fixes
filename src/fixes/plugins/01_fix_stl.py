import re

class Plugin:
    name = "add-collision"
    cmd_name = name
    cmd_letter = "s"
    display_name = "Add collision STL"
    enabled = False

    def rollout(self, robot, filename):
        for link in robot.links:
          for collision in link.collisions:
            collision.geometry.filename = re.sub("(meshes/)(base|bone)([\w]*)(\.STL)", r"\1collision/\2\3\4", collision.geometry.filename)

    def rollback(self, robot, filename):
        for link in robot.links:
          for collision in link.collisions:
            collision.geometry.filename = re.sub("/meshes/collision/", "/meshes/", collision.geometry.filename)

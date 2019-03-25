import re

class Plugin:
    name = "dae-meshes"
    cmd_name = name
    cmd_letter = "d"
    display_name = "Change meshes to .DAE"
    enabled = False

    def rollout(self, robot, filename):
        for link in robot.links:
          for visual in link.visuals:
            visual.geometry.filename = re.sub(r"(meshes/)(base|bone)([\w]*)(\.STL)", r"\1\2\3.DAE", visual.geometry.filename)

    def rollback(self, robot, filename):
        for link in robot.links:
          for visual in link.visuals:
            visual.geometry.filename = re.sub(r'(meshes/)(base|bone)([\w]*)(\.DAE)', r"\1\2\3.STL", visual.geometry.filename)

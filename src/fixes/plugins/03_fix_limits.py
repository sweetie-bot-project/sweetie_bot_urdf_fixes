import json
import os
import roslib; roslib.load_manifest('urdfdom_py')
from urdf_parser_py.urdf import *

class Plugin:
    name = "set-limits"
    cmd_name = name
    cmd_letter = "l"
    display_name = "Set limits"
    enabled = False

    def __init__(self):
        self.limits_dict = {}
        path = os.path.splitext(os.path.realpath(__file__))[0]
        with open(path + ".json", "r") as f:
          self.limits_dict = json.loads(f.read())
          f.close()

    def rollout(self, robot, filename):
        
        for joint in robot.joints:
          if joint.type == 'revolute' and joint.name in self.limits_dict:
            joint.limit = JointLimit(**self.limits_dict[joint.name])

        return False

    def rollback(self, robot, filename):
        for joint in robot.joints:
          if joint.type == 'revolute' and joint.name in self.limits_dict:
            joint.limit = None
	return False

import json
import os
import roslib; roslib.load_manifest('urdfdom_py')
from urdf_parser_py.urdf import JointLimit

class Plugin:
    name = "set-limits"
    cmd_name = name
    cmd_letter = "l"
    display_name = "Set limits"
    enabled = True

    def load_limits_from_file(self, package_name):
        path = os.path.splitext(os.path.realpath(__file__))[0]
        with open(path + "_" + package_name + ".json", "r") as f:
          self.limits_dict = json.loads(f.read())
          f.close()

    def __init__(self):
        self.limits_dict = {}

    def rollout(self, robot, filename, package_name):
        self.load_limits_from_file(package_name)
        for joint in robot.joints:
          if joint.type == 'revolute' and joint.name in self.limits_dict:
            joint.limit = JointLimit(**self.limits_dict[joint.name])
        return False

    def rollback(self, robot, filename, package_name):
        self.load_limits_from_file(package_name)
        for joint in robot.joints:
          if joint.type == 'revolute' and joint.name in self.limits_dict:
            joint.limit = None
	return False

class Plugin:
    name = "fix-axis"
    cmd_name = name
    cmd_letter = "a"
    display_name = "Fix axis"
    axis_to_reverse = ['joint11','joint15','joint21','joint25','joint31','joint35','joint41','joint45']
    enabled = False

    def rollout(self, robot, filename):
        for joint in robot.joints:
          if joint.name in self.axis_to_reverse:
            joint.axis[0] = -1.0

    def rollback(self, robot, filename):
        for joint in robot.joints:
          if joint.name in self.axis_to_reverse:
            joint.axis[0] = 1.0


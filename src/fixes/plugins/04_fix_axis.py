class Plugin:
    name = "fix-axis"
    cmd_name = name
    cmd_letter = "a"
    display_name = "Fix rotation directions"
    axis = {'joint11': [-1, 0, 0], 'joint15': [-1, 0, 0], 'joint21': [-1, 0, 0], 'joint25': [-1, 0, 0],
            'joint31': [-1, 0, 0], 'joint35': [-1, 0, 0], 'joint41': [-1, 0, 0], 'joint45': [-1, 0, 0],
            'leg1_joint2': [1, 0, 0], 'leg1_joint3': [0, -1, 0], 'leg1_joint4': [0, -1, 0], 'leg1_joint6': [-1, 0, 0],
            'leg2_joint2': [-1, 0, 0], 'leg2_joint3': [0, -1, 0], 'leg2_joint6': [-1, 0, 0],
            'leg3_joint6': [-1, 0, 0],
            'leg4_joint2': [-1, 0, 0], 'leg4_joint6': [-1, 0, 0],
            'head_joint1': [0, 1, 0], 'head_joint3': [-1, 0, 0]}
    enabled = True

    def rollout(self, robot, filename, package_name):
        for joint in robot.joints:
            if joint.name in self.axis.keys():
                joint.axis = self.axis[joint.name]

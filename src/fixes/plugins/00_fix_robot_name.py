class Plugin:
    name = "fix-robot-name"
    cmd_name = name
    cmd_letter = "r"
    display_name = "Fix robot name"
    enabled = False

    def rollout(self, robot, filename):
	if robot.name.endswith('_description'):
	  robot.name = robot.name[0:-12] 

    def rollback(self, robot, filename):
	if not robot.name.endswith('_description'):
	  robot.name = robot.name + '_description'

import re, os
import roslib; roslib.load_manifest('urdfdom_py')
from urdf_parser_py.urdf import *

class Plugin:
    name = "make-dynamics"
    cmd_name = name
    cmd_letter = "m"
    display_name = "Make dynamics URDF"
    enabled = False
    links_to_remove = ['bone16', 'bone26', 'bone36', 'bone46']
    joints_to_remove = ['joint16', 'joint26', 'joint36', 'joint46']
    hoof_regexp = r'(<link[^>]+?name="bone[1234]6"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint[1234]6"[\s\S]+?</joint>[\s\S]*?)(<link[^>]+?name="hoof[1234]"[^>]*?>)?([\s\S]+?<joint[^>]+?name="joint_hoof[1234]"[\s\S]+?</joint>)?'
    nose_regexp = r'(<link[^>]+?name="bone5[56]"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint5[56]"[\s\S]+?</joint>[\s\S]*?)'
    fcus_regexp = r'(<link[^>]+?name="link_eyes_[xyz]"[^>]*?>)([\s\S]+?<joint[^>]+?name="joint_eyes_focus_[xyz]"[\s\S]+?</joint>[\s\S]*?)'
    scrn_regexp = r'(<link[^>]+?name="screen_(left|right)"[^>]*?>)([\s\S]+?<joint[^>]+?name="screen_(left|right)"[\s\S]+?</joint>[\s\S]*?)'
    eyes_regexp = r'(<link[^>]+?name="eyes_link_(pitch|yaw)"[^>]*?>)([\s\S]+?<joint[^>]+?name="eyes_(pitch|yaw)"[\s\S]+?</joint>[\s\S]*?)'
    base_link_sel = r'(<link[\s\S]*?base_link">)()([\s\S]*?)(<link[\s\S]*?name="base_link_inertia">[\s\S]*?)(<inertial>[\s\S]*?</inertial>)([\s\S]*?</joint>)'

    def rollout(self, robot, filename):
	with open(filename, 'r+') as f:
	  urdf = f.read()

	urdf = re.sub(self.hoof_regexp, '', urdf)
	urdf = re.sub(self.nose_regexp, '', urdf)
	urdf = re.sub(self.fcus_regexp, '', urdf)
	urdf = re.sub(self.eyes_regexp, '', urdf)
	urdf = re.sub(self.scrn_regexp, '', urdf)
	urdf = re.sub(self.base_link_sel, r'\1'+'\n    '+r'\5\3', urdf)

	robot_dyn = URDF.from_xml_string(urdf)

        with open(os.path.splitext(filename)[0]+"_dynamics.urdf", 'w') as f:
	  f.truncate(0)
	  f.seek(0)
	  f.write(robot_dyn.to_xml_string())
	  f.close()

	return True

    def rollback(self, robot, filename):
	if os.path.exists(os.path.splitext(filename)[0]+"_dynamics.urdf"):
	  os.remove(os.path.splitext(filename)[0]+"_dynamics.urdf")

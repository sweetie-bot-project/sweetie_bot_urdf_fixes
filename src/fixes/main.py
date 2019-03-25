#!/usr/bin/env python

# import custom plugins from plugins directory
import plugins

# Load the urdf_parser_py manifest, you use your own package
# name on the condition but in this case, you need to depend on
# urdf_parser_py.
import roslib; roslib.load_manifest('urdfdom_py')
import rospy
import rospkg
import locale
import argparse
import sys, os
import re

from dialog import Dialog

rospack = rospkg.RosPack()

from urdf_parser_py.urdf import URDF

locale.setlocale(locale.LC_ALL, '')

class SweetieFixes:

	title = "Sweetie bot urdf fix program"

	description = '''This program applies custom fixes to URDF file.\nYou only need this if you are exporting new files and want to distribute the changes.\n'''
	what_file = 'What package do you want to fix?'
	what_todo = 'What do you want to do?'
        what_func = "What fixes do you want to %s ?"

	choices={}

	parser = argparse.ArgumentParser(description=title)


	def __init__(self):
            pass


	def is_valid_file(self, arg):
	   if not os.path.isfile(arg):
	       self.parser.error("The file %s does not exist!" % arg)
	   else:
	       return arg


	def is_valid_pkg(self, arg):
	    if not arg in rospack.list():
	        self.parser.error("The package %s does not exist!" % arg)
	    else:
	        return self.is_valid_file(rospack.get_path(arg) + '/urdf/' + arg + '.urdf')


	def read_cmdline_args(self):
	  self.parser.add_argument('-t', '--tui', action='store_true', default=True, help='Show ncurses tui')
	  self.parser.add_argument("-f", "--file", required=False, type=self.is_valid_file, metavar="FILE", help="the URDF file to apply fixes")
	  self.parser.add_argument("-p", "--pkg",  required=False, type=self.is_valid_pkg, metavar="PKG", help="robot description package name")

	  group = self.parser.add_mutually_exclusive_group(required=False)
	  for func_name, plugin_list in plugins.functions.items():
	    group.add_argument('--'+func_name, nargs='+', choices=plugin_list)

	  self.parser.parse_args(namespace=self)
	  args = self.parser.parse_args()

	  self.file = self.pkg if not self.pkg is None else self.file
	  if self.file is None:
		  if not self.rollout is None or not self.rollback is None:
		    self.parser.error("one of the arguments --file --pkg is required")
		  else: # empty args or only --tui
		    return False
	  else:
		  if self.rollout is None and self.rollback is None:
		    self.parser.error("one of the arguments --%s is required" % ' --'.join(plugins.functions.keys()))
		  else: 
		    self.tui = False 
		    return True

	  return False


	def read_tui(self):
	  description_pkgs = [(pkg, '') for pkg in filter(lambda x: re.search('sweetie_bot_[\w]+?_description', x), rospack.list())]
          if len(description_pkgs) == 0:
	    self.parser.error("ROS packages sweetie_bot_*_description not found")

	  d = Dialog(dialog="dialog")
	  d.set_background_title(self.title)

	  code, package_name = d.menu(self.description + self.what_file, choices=description_pkgs)

	  if code != d.OK:
            return False

	  self.file = self.is_valid_pkg(package_name)

	  code, func_name = d.menu(self.description + self.what_todo, choices=plugins.functions_names)

	  if code != d.OK:
	    return False

	  choices = []
	  for plugin in plugins.loaded.values():
	    if func_name in dir(plugin):
	      choices.append((plugin.display_name, plugin.cmd_letter, plugin.enabled))

          code, tags = d.checklist(self.what_func % func_name, choices=choices, title=func_name+' '+ os.path.basename(self.file), width=60)

	  if code != d.OK:
	    return False

          plugin_choices_list = []
	  for plugin in plugins.loaded.values():
	     if(plugin.display_name in tags):
		plugin_choices_list.append( plugin.name )

	  setattr(self, func_name, plugin_choices_list)
	  return True


	def read_user_input(self):
	  if not self.read_cmdline_args():
	    if not self.read_tui():
		return False
	  return True


	def read_robot_from_file(self, filename = None):
	  if filename == None: 
	    filename = self.file
	  self.robot = URDF.from_xml_file(self.file)


	def write_robot_to_file(self, filename = None):
	  if filename == None: 
	    filename = self.file
	  with open(self.file, 'w') as f:
	    f.truncate(0)
	    f.seek(0)
	    f.write(self.robot.to_xml_string())
	    f.close()


	def do(self):
	  self.robot = URDF.from_xml_file(self.file)
          for func_name in plugins.functions.keys():
	    if getattr(self, func_name) is not None:
	      break

	  for plugin in plugins.loaded.values():
	    if plugin.name in getattr(self, func_name):
	      func = getattr(plugin, func_name)
	      if func(self.robot, self.file):
	        # if function returned True that means file changed in place, we need re read it
	        self.read_robot_from_file()
	      else:
                # write changes to disk
	        self.write_robot_to_file()

	    self.write_robot_to_file()


def main():
    try:
        #run_fixes()
        fixes = SweetieFixes()
	if fixes.read_user_input():
	  fixes.do()

    except rospy.ROSInterruptException:
        pass

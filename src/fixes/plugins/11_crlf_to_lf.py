import os

class Plugin:
    name = "crlf-to-lf"
    cmd_name = name
    cmd_letter = "c"
    display_name = "Convert CRLF to LF"
    enabled = True

    # replacement strings
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'

    def crlf_to_lf(self, filename):
	self.convert_line_ending(filename, self.WINDOWS_LINE_ENDING, self.UNIX_LINE_ENDING)

    def lf_to_crlf(self, filename):
	self.convert_line_ending(filename, self.UNIX_LINE_ENDING, self.WINDOWS_LINE_ENDING)

    def convert_line_ending(self, filename, le_from, le_to):
	with open(filename, 'r+') as f:
	  content = f.read()
	  content = content.replace(le_from, le_to)
          f.truncate(0)
          f.seek(0)
	  f.write(content)
	  f.close()


    def rollout(self, robot, filename, package_name):
	pdir = os.path.dirname(filename)
	pdir = os.path.dirname(pdir)

	self.crlf_to_lf(os.path.join(pdir, 'package.xml'))
	self.crlf_to_lf(os.path.join(pdir, 'CMakeLists.txt'))

	for file in os.listdir(os.path.join(pdir, 'config')):
	  if file.endswith(".yaml"):
	    self.crlf_to_lf(os.path.join(pdir, 'config', file))

	for file in os.listdir(os.path.join(pdir, 'launch')):
	  if file.endswith(".launch"):
	    self.crlf_to_lf(os.path.join(pdir, 'launch', file))

    def rollback(self, robot, filename, package_name):
	pass

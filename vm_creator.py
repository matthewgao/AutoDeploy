#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-10-12

__author__ = 'Matthew Gao'

BASE_PATH = '/home/shgao/vm-imaging/vm-imaging/Firmware/EXSeriesVPN/'

import getopt
import sys
import os
from bob_downloader import BobDownloader, BRANCH_MAP

def error_hander(func):
	def wrapper(*args, **kargs):
		try:
			func(*args, **kargs)
		except CommanderRunnerExcpetion as e:
			print(e)
			usage()
			sys.exit(2)
		except getopt.GetoptError as err:
			print(err) # will print something like "option -a not recognized"
			usage()
			sys.exit(2)

	return wrapper

class CommanderRunnerExcpetion(Exception):
	def __init__(self, err_str):
		super(CommanderRunnerExcpetion, self).__init__()
		self.err_str = err_str

	def __str__(self):
		return "CommanderRunner Error: {0}".format(self.err_str)

class CommandRunner(object):
	"""docstring for CommandRunner"""

	def __init__(self):
		super(CommandRunner, self).__init__()
		self.internal_ip = None
		self.build = None
		self.appl_name = None

	@error_hander
	def opts_parser(self):
	    opts, args = getopt.getopt(sys.argv[1:], "h:b:n:", ["host=","help","build=","name="])

	    output = None
	    verbose = False
	    for o, a in opts:
	        if o in ("-h", "--host"):
	            self.internal_ip = a
	        elif o in ('-b', '--build'):
	        	self.build = a
	        elif o in ('-n', '--name'):
	        	self.appl_name = a
	        elif o in ("--help"):
	            usage()
	            sys.exit()

	    if self.internal_ip is None:
	    	raise CommanderRunnerExcpetion("You have to specify a internla IP")
	    if self.build is None:
	    	raise CommanderRunnerExcpetion("You have to specify a bob build version")
	    if self.appl_name is None:
	    	raise CommanderRunnerExcpetion("You have to specify a appliance name")


	def __call__(self):
		self.opts_parser()
		ver_str, build_str = self.build.split('-')
		b = BobDownloader(ver_str,build_str,'/home/shgao/bob_build')
		_full_iso_path = b.start()
		print(ver_str,build_str)
		_path = BASE_PATH + BRANCH_MAP[ver_str][1] + '/vm-imaging/'
		os.chdir(_path)
		#print(os.getcwd())
		appliance_name = self.appl_name.replace('.','-') + '-' + self.internal_ip.replace('.','-')

		shell_str = './make-machine.sh -n {0} -i {1} -h {2}'.format(appliance_name, 
		 								_full_iso_path, self.internal_ip)
		print(shell_str)
		os.system(shell_str)
		print("ALL DONE, VM name is {0}".format(appliance_name))
		print("You can access AMC through : https://{0}:8443".format(self.internal_ip))
	

def usage():
	usage_str = 'Usage:\n'
	usage_str += '\t-h [IP]|--host=[IP]: Specify the internal IP address of the appliance \n'
	usage_str += '\t-b [ISO name]|--build=[ISO name]: Specify the version of the ISO(NOT unstripped prefix) \n'
	usage_str += '\t-n [appliance name]|--build=[appliance name]: Specify the appliance name \n'
	print(usage_str)

if __name__ == "__main__":
    CommandRunner()()

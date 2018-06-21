#!/usr/bin/python

import subprocess
from optparse import OptionParser
import os

logdir = "logs"

tools = {}
tools['rcl-show-environments']=['', '--arch=ppc64', '--vendor=GenuineIntel', '--microarch=IVB', '--family=, --model=45', '--family=6 --model=45 --stepping=7', '--virt=kvm', '--kernel=3.10.0-693.el7', '--microarch=IVB --csv']
tools['rcl-show-events'] = ['', '--name cpu-cycles', '--csv']
tools['rcl-show-experiments'] = ['', '--name linpack1000d', '--csv']
tools['rcl-show-kernels'] = ['', '--name 4.14.0-6.el7a', '--csv']
tools['rcl-show-tools'] = ['', '--name oprofile', '--name papi', '--name perf --version 2.6.32-696.el6']
tools['rcl-show-vendors'] = ['', '--name GenuineIntel', '--csv']
tools['rcl-show-virt'] = ['', '--name kvm', '--csv']
tools['rcl-show-results'] = ['--event=cpu-cycles', '--event=instructions --experiment=simple', '--event=instructions --experiment=linpack1000d',
'--event=cpu-cycles --env-details=2', '--event=instructions --experiment=simple --env-detail=2', '--event=instructions --experiment=linpack1000d --env-details=2',
'--event=cpu-cycles --env-details=2 --tool-datails --kernel-details', '--event=instructions --experiment=simple --env-detail=2', '--event=instructions --experiment=linpack1000d --env-details=2',
'--event=instructions --cpu-vendor=GenuineIntel --cpu-model=45', '--event=instructions --cpu-vendor=GenuineIntel --cpu-model=45 --cpu-family=6',
'--event=instructions --cpu-arch=x86_64 --cpu-model=58', '--cpu-arch=ppc64le --cpu-microarch=POWER9'
'--event=instructions --cpu-arch=x86_64 --cpu-model=87', '--cpu-arch=ppc64le --virt=ibm_power-kvm',
'--event=instructions --cpu-arch=x86_64 --cpu-model=58 --kernel=4.14.0-6.el7a', '--cpu-arch=ppc64le --cpu-microarch=POWER9 --kernel=4.14.0-6.el7a'
'--event=instructions --cpu-arch=x86_64 --cpu-model=87 --experiment=simple', '--cpu-arch=ppc64le --virt=ibm_power-kvm --experiment=simple']    

optparser = OptionParser()

(options, args) = optparser.parse_args()

# use arguments if are given
if args:
	tool_list = args
else:
	tool_list = tools.keys()

if not os.path.exists(logdir):
	os.makedirs(logdir)

for tool in tool_list:

	# validate tool
	if tool not in tools.keys():
		continue

	tool_dir = os.path.join(logdir, tool)
	if not os.path.exists(tool_dir):
		os.makedirs(tool_dir)
	log = 0
	print "Running %s ..." % tool

	for opt in tools[tool]:
		p = subprocess.Popen(tool + ' ' + opt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		f = open(os.path.join(tool_dir, str(log).zfill(2)), "w")
		for line in p.stdout.readlines():
			f.write(line)
		retval = p.wait()
		f.close()
		if retval == 0:
			print "\t[OK] %s %s" % (tool, opt)
		else:
			print "\t[!!] %s %s" % (tool, opt)
		log += 1

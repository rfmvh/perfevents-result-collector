#!/usr/bin/python

import subprocess

tools={}
tools['rcl-show-environments']=['', '--arch=ppc64', '--vendor=GenuineIntel', '--microarch=IVB', '--family=, --model=45', '--family=6 --model=45 --stepping=7', '--virt=kvm', '--kernel=3.10.0-693.el7', '--microarch=IVB --csv']
tools['rcl-show-events'] = ['', '--name cpu-cycles', '--csv']
tools['rcl-show-experiments'] = ['', '--name linpack1000d', '--csv']
tools['rcl-show-kernels'] = ['', '--name ???', '--csv']  
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

command = 'rcl-show-environments'
options = ['', '--vendor=GenuineIntel', '--microarch=IVB', '--family=6 --model=45', ]

for opt in options:
	p = subprocess.Popen(command + ' ' + opt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		print line,
	retval = p.wait()
	if retval == 0:
		print "Probehlo OK"
	else:
		print "Chyba nastala"
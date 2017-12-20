#!/usr/bin/python

import subprocess

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

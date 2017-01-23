#!/usr/bin/python

import sys, threading
import os, signal, subprocess # This is used when exiting the program


###
### Below code KILLS any currently running sensorClient.py process
### EXCLUDING itself
###
class singletonExecution():

	@staticmethod
	def ensureOnlyOneInstance():

		myPid = os.getpid()
		print "My PID= [" + str(myPid) + "]"

		cmd = "ps -ef | grep 'python sensorClient.py' | grep -v grep | awk '{print $2}'"
		p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		out = p.communicate() [0]
		for pid in out.splitlines():
		    if myPid != pid:
		        #print pid
		        if int(pid) != int(myPid):
		            try:
		                os.kill(int(pid), signal.SIGKILL)
		                print "KILLED old sensorClient.py record [" + pid + "]"
		            except:
		                print "err - could not kill previous running instance [" + pid + "]"
#!/usr/bin/python
import os
import signal
import subprocess  # This is used when exiting the program


#
#  Below code KILLS any currently running weatherSensor.py process
#  EXCLUDING itself
#
class SingletonExecution(object):

    @staticmethod
    def ensure_only_one_instance():

        my_pid = os.getpid()
        print("My PID= [" + str(my_pid) + "]")

        cmd = "ps -ef | grep 'python weatherSensor.py' | grep -v grep | awk '{print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]
        for pid in out.splitlines():
            if my_pid != pid:
                # print pid
                if int(pid) != int(my_pid):
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                        print("KILLED old weatherSensor.py record [" + pid + "]")
                    except Exception as e:
                        print("err - could not kill previous running instance [" + pid + "]")
                        print("Error was: [%s]", e.__str__())

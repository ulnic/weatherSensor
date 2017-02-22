#!/usr/bin/python
"""
Singleton classed
"""
import os
import signal
import subprocess  # This is used when exiting the program


class SingletonExecution(object):
    """
    Ensures the weatherSensor implements the singleton pattern to only have one instance active at any time
    """
    @staticmethod
    def ensure_only_one_instance():
        """
        Validates if there are more than one instance of the python application running.
        IF yes, it kills the other instances
        """
        my_pid = os.getpid()
        print("My PID= [{0}]".format(str(my_pid)))

        cmd = "ps -ef | grep 'python weatherSensor.py' | grep -v grep | awk '{print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]
        for pid in out.splitlines():
            if my_pid != pid and int(pid) != int(my_pid):
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print("KILLED old weatherSensor.py record [ {0} ]".format(pid))
                except Exception as e:
                    print("err - could not kill previous running instance [ {0} ]".format(pid))
                    print("Error was: [{0}]".format(e.__str__()))

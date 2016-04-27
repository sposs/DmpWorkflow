"""
Created on Mar 22, 2016

@author: zimmer
"""
from DmpWorkflow.utils.shell import run
from DmpWorkflow.config.defaults import AppLogger
class BatchJob(object):
    """ generic batch job which can be expanded by classes inheriting from this class """
    name = None
    logFile = None
    queue = None
    cputime = 0.
    memory = 0.
    command = ""
    extra = ""
    defaults = None
    requirements = []
    status = None
    logging = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.__processDefaults__()
        self.logging = AppLogger(LOG_LEVEL="INFO")
        
    def __processDefaults__(self):
        if self.defaults is None: return 
        self.queue = self.defaults['queue']
        self.requirements = self.defaults['requirements']
        self.extra = self.defaults['extra']
        self.memory = self.defaults['memory']
        self.cputime = self.defaults['cputime']

    def __execWithUpdate__(self, cmd, key, value=None):
        """ execute command cmd & update key with output from running """
        output, error, rc = run([cmd])
        self.logging.debug("execution with rc: %i",int(rc))
        if error:
            for e in error.split("\n"): 
                if len(e): self.logging.error(e)
                
        if value is None:
            self.update(key, output)
        else:
            self.update(key, value)

    def submit(self, **kwargs):
        """ each class MUST implement its own submission command """
        pass

    def kill(self):
        """ likewise, it should implement its own batch-specific removal command """
        pass

    def update(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value

    def get(self, key, callable=str):
        if key in self.__dict__:
            return callable(self.__dict__[key])
        return None
    
    def __run__(self,cmd):
        output, error, rc = run([cmd])
        self.logging.debug("execution with rc: %i",int(rc))
        if error:
            for e in error.split("\n"): 
                if len(e): self.logging.error(e)
        if rc:
            self.logging.error("exception during execution")
        return output


class BATCH(object):
    """
    generic Batch class, all HPC-specific modules should inherit from it.
    """
    allJobs = {}
    keys = []
    status_map = {}

    def __init__(self):
        self.allJobs = self.update()
        self.logging = AppLogger(LOG_LEVEL="INFO")

    def update(self):
        return {}

    def __checkKeys__(self, key):
        if key not in self.keys:
            self.logging.error("could not extract key, allowed keys %s", str(self.keys))
            raise Exception

    def getJob(self, jobID, key="STAT", callable=str):
        if jobID not in self.allJobs:
            self.logging.error("could not find job %s", jobID)
        self.__checkKeys__(key)
        return callable(self.allJobs[jobID][key])

    def getAttributeForAllJobs(self, attr="MEM"):
        """ convenience function to return all values for a certain attribute """
        key = attr
        self.__checkKeys__(key)
        ret = {}
        for jobID in self.allJobs:
            val = None
            if key not in self.allJobs[jobID]:
                self.logging.error("could not find key %s in job %s", key, jobID)
            else:
                val = self.allJobs[jobID][key]
            print val
            ret[jobID] = val
        return ret

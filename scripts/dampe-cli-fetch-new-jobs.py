'''
Created on Mar 15, 2016

@author: zimmer
'''
import copy
from core.DmpJob import DmpJob
import requests
if __name__ == "__main__":
    newJobInstances = []
    res = requests.get("some_url_to_define/jobs")
    res.raise_for_status()
    for job in res.json():
        newJobs = [j for j in job['jobInstances'] if j['status'] == 'New']
        if len(newJobs):
            dJob = DmpJob(job['body'])
            for j in newJobs:
                dInstance = copy.deepcopy(dJob)
                dInstance.setInstanceParameters(j['body'])
                newJobInstances.append(dInstance)
    print 'found %i new job instances to deploy'%len(newJobInstances)
    

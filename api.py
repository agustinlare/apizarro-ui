import logging
import requests
import os

apizarro = os.environ['APIZARRO_API_URL']

def caseBtn(form):
    resp = ""

    for k in form:
        if k == 'start':
            resp = "start"
            break
        elif k == 'done':
            resp = "done"
            break
            
    return resp

def doYouthing(form):
    print(form)
    
    return form

def getCluster(config, cluster):
    for c in config['clusters']:
        if c['name'] == cluster:
            return c
        
        if c == None:
            logging.critical("Cluster configuration not found")

def getActions(config, action):
    for c in config['actions']:
        if c['name'] == action:
            return c

        if c == None:
            logging.critical("Action configuration not found")

def getProjects(env):
    project_list = []

    ploads = {'cluster': env}
    response = requests.get('http://127.0.0.1:5001/Pizarro/ocp4/getProject',ploads)
    response = response.json()

    for i in response['message']:
        if not i.startswith('openshift'):
            project_list.append(i)

    return project_list

def getPods(env,ns):
    pods_list = []

    ploads = {'cluster': env, 'project': ns}
    response = requests.get('http://127.0.0.1:5001/Pizarro/ocp4/getPods',ploads)
    response = response.json()

    for i in response['message']:
        pods_list.append(i)

    return pods_list
# encoding = utf-8
import json
import requests
import sys

try:
  from requests.packages.urllib3.exceptions import InsecureRequestWarning
  requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def reqtask(node, task, token, environment, url, parameters=None):
  headers = {'X-Authentication': token}

  if parameters:
    params = json.loads(parameters)
  else:
    params = {}

  req = {
    'environment' : environment,
    'task' : task,
    'params' : params,
    'scope' : {
      'nodes' : [node]
    }
  }

  endpoint = '{}/command/task'.format(url)

  #https://puppet.angrydome.org:8143/orchestrator/v1/command/task

  try:
    r = requests.post(endpoint, json=req, headers=headers, verify=False)
  except:
    print('Unexpected error:', sys.exc_info()[0])
    print >> sys.stderr, 'Error: {}'.format(sys.exc_info()[0])
    raise

  if r.status_code == 202:
    job = json.loads(r.text)['job']
    return job
  else:
    raise ValueError('Unable to submit task command', r.status_code, r.text)




def process_event(helper, *args, **kwargs):

    victor_ops_token = helper.get_global_setting("victorops_token")
    alert_entity_id = helper.get_param("alert_entity_id")
    dropdown_list = helper.get_param("severity")
    state_message = helper.get_param("module")
    view_report = helper.get_param("severity")
    description = helper.get_param("description")
    parameters = helper.get_param("parameters")
    node = helper.get_param("host")
    env = helper.get_param("environment")
    pe_token = helper.get_global_setting("puppet_enterprise_token")
    pe_server = helper.get_global_setting("puppet_enterprise_server")
    pe_port = helper.get_global_setting("port")
    noop  = helper.get_param("noop")

    method = 'POST'
    api_request = 'application/json'

    urlpe = "https://" + pe_server + ":" + pe_port + "/orchestrator/v1"
    helper.set_log_level(dropdown_list)
    helper.log_info("Alert action Puppet Tasks Alert Action started.")
    try:
        jobid = reqtask(node, state_message,pe_token,env,urlpe)
    except:
        ValueError('Unable to submit task command', state_message, pe_server)

    return 0
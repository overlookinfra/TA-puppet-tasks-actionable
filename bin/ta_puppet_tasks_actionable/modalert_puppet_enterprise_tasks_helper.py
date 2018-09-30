# encoding = utf-8
import json
import urllib2
import requests
import sys

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
    
    urlpe = pe_server + ":" + pe_port + "/orchestrator/v1/command/task"
    
    headers = {
       'X-Authentication': pe_token,
       'Content-Type': api_request
       }

    if noop == 1:
        data = '{ "environment" : "%s", "task" : "%s" ,"description" : "%s" ,"params" :  {%s},"scope" : {"nodes" : ["%s"]}}, "noop" : "true"' % (env, state_message, description, parameters, node)
        
        print >> sys.stderr, "ERROR Server response: %s" % data
    else:
        data = '{ "environment" : "%s", "task" : "%s" ,"description" : "%s" ,"params" :  {%s},"scope" : {"nodes" : ["%s"]}}' % (env, state_message, description, parameters, node)
    
        print >> sys.stderr, "ERROR Server response: %s" % data
    
    response = requests.post(urlpe, headers=headers, data=data, verify=False)
    
    if victor_ops_token == "":
        
        print >> sys.stderr, "No VictorOps Account Setup" 
        return
        
    else:
        
        url = "https://alert.victorops.com/integrations/generic/20131114/alert/" + victor_ops_token + ""
            
        
        data = dict(
            message_type=dropdown_list,
            monitoring_tool='Puppet Tasks',
            state_message=state_message,
            job_description=description,
            entity_id=alert_entity_id,
            view_report=data,
            pe_server=pe_server,
            pe_port=pe_port,
            node=node
        )
        
        
        search_name = helper.get_events()
        entity_id = "Puppet Tasks Alert: %s" % search_name
        
        view_report = helper.get_param('results_link')
        
        helper.log_info("Alert action Puppet Tasks VictorOps Alert Action started.")
        
      
        response = helper.send_http_request(url, 
                                        method, 
                                        parameters=None, 
                                        payload=json.dumps(data),
                                        headers=headers, 
                                        cookies=None, 
                                        verify=False, 
                                        cert=None,
                                        timeout=None, 
                                        use_proxy=True)
        
        
        body = json.dumps(data)
        
        req = urllib2.Request(url, body, {"Content-Type": "application/json"})
        
        try:
            res = urllib2.urlopen(req)
            body = res.read()
            print >> sys.stderr, "INFO VictorOps server responded with HTTP status=%d" % res.code
            print >> sys.stderr, "DEBUG VictorOps server response: %s" % json.dumps(body)
            return 200 <= res.code < 300
        except urllib2.HTTPError, e:
            print >> sys.stderr, "ERROR Error sending message: %s (%s)" % (e, str(dir(e)))
            print >> sys.stderr, "ERROR Server response: %s" % e.read()
            return False
         
    
        return 0

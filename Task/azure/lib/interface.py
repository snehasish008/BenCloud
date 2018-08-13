# -*-coding: utf-8 -*-
#
#!/usr/bin/python

import sys
import requests
import json
import pathlib

#arg1=sys.argv[1]
#arg2=sys.argv[2]
#arg3=sys.argv[3]
#arg4=sys.argv[4]
#arg5=sys.arg[5]


def azure_get_request(subs_id,rg_name,NwIntf_name,api_version,API_KEY):
    
    URL='https://management.azure.com/subscriptions/'+subs_id+'/resourceGroups/'+rg_name+'/providers/Microsoft.Network/networkInterfaces/'+NwIntf_name+'/ipConfigurations?api-version='+api_version
    
    header={'Authorization':'Bearer '+API_KEY,'Accept':'application/json','Content-Type':'application/json'}
    #r=requests.get(url=URL, params=None, headers=header)
    r=requests.get(url=URL, params=None, headers=header)
    #json_data=r.json()
    
    #with open('/home/snehasish/Task/azure/json_files/'+NwIntf_name+'.json','w') as f:
    #    json.dump(json_data,f,indent=2)
    json_obj=json.loads(r.text)
    return json_obj    





#def create_config_json(vmName,APIJSONPath,NwIntfJSONFileName,NwIntfJSONPath):
    
#    if vmName=='PIPGW':
#        with open(APIJSONPath+NwIntfJSONFileName) as f:
#            data=json.load(f)
#        with open(NwIntfJSONPath+vmName+'.json','w') as c:
#            json.dump(data,c,indent=2)
#        c.close()
#        f.close()
#        check_file = pathlib.Path(NwIntfJSONPath+vmName+'.json')
#        if check_file.is_file():
#            print('Deployment JSON successfully created')
#        else:
#            print('Deployment JSON creation failed')
#            sys.exit(1)
#
#    elif vmName=='IGW':
#        with open(APIJSONPath+NwIntfJSONFileName) as f:
#            data=json.load(f)
#        with open(NwIntfJSONPath+vmName+'.json','w') as c:
#            json.dump(data,c,indent=2)
#        c.close()
#        f.close()
#        check_file = pathlib.Path(NwIntfJSONPath+vmName+'.json')
#        if check_file.is_file():
#            print('Deployment JSON successfully created')
#        else:
#            print('Deployment JSON creation failed')
#            sys.exit(1)
#
#    else:
#        print('Invalid vmName given')
#        sys.exit(1)

import sys
import requests
import json

intf_details_string= '''
{
        "Interfaces": [{
                        "Name": "eth0",
                        "IPConfigurations": [{
                                "IPAddress": "12.1.5.5",
                                "PrefixLength": 24,
                                "DefaultGateway": "12.1.5.1",
                                "IsPrimary": true
                        }],
                        "Description": "connected to cloudsimple network",
                        "IsPrimary": true
                },
                {
                        "Name": "eth1",
                        "IPConfigurations": [{
                                "IPAddress": "12.1.5.8",
                                "PrefixLength": 24,
                                "DefaultGateway": "12.1.5.1",
                                "IsPrimary": true
                        }],
                        "Description": "connected to internet"
                }
        ],
        "Tunnels": [{
                        "VNI": 142,
                        "RemoteVtep": "11.0.0.4",
                        "LocalVtep": "12.1.5.5",
                        "TunnelInterface": {
                                "IPConfigurations": [{
                                        "IPAddress": "169.254.42.2",
                                        "PrefixLength": 30,
                                        "DefaultGateway": "169.254.42.1",
                                        "IsPrimary": true
                                }],
                                "MTU": 1370,
                                "Description": "IGW-to-CSDC"
                        },
                        "Description": "IGW-to-CSDC"
                },
                {
                        "VNI": 162,
                        "RemoteVtep": "10.0.3.6",
                        "LocalVtep": "12.1.5.5",
                        "TunnelInterface": {
                                "IPConfigurations": [{
                                        "IPAddress": "169.254.62.2",
                                        "PrefixLength": 30,
                                        "DefaultGateway": "169.254.62.1",
                                        "IsPrimary": true
                                }],
                                "MTU": 1370,
                                "Description": "IGW-to-PIP"
                        },
                        "Description": "IGW-to-PIP"
                }
        ],
        "PublicIPs": [
                {
                        "VNI": 162,
                        "Description": "any service",
                        "VPIN-VM": "11.0.1.5",
                        "VIP-Mapped-Private-IP": "10.0.3.9"
                }
        ]
}
'''

_vm_name=str(sys.argv[1])
#_sub_id=str(sys.argv[2])
#_rg_name=str(sys.argv[3])
#_NwIntf_name=str(sys.argv[4])
#_api_version=str(sys.argv[5])
#_api_key=str(sys.argv[2])


def azure_configIGWandPIP(vm=_vm_name):

    igw='IGW'
    pip='PIPGW'
    if pip.lower() in vm.lower():
        json_obj=json.dumps(intf_details_string)
        endpoint_ipaddr= json_obj['Interfaces'][0]['IPConfigurations'][0]['IPAddress']    
        api_endpoint="http://"+endpoint_ipaddr+":8080/api/v1/config/all"
        header={'Content-Type':'Application/json'}
        
        r=requests.post(api_endpoint,data=json_obj,headers=header)
        if r:
            azure_response=r.text
            print('Response recieved \n %s' %azure_response)
            print('\n')
            print(vm+' Configuration Successful')
            print('\n')
            print(json.dumps(json_obj, indent=1))
        else:
            print(vm+' Configuration failed')

    elif igw.lower() in vm.lower():
        json_obj=json.dumps(intf_details_string)
        endpoint_ipaddr=json_obj['Interfaces'][0]['IPConfigurations'][0]['IPAddress']
        api_endpoint="http://"+endpoint_ipaddr+":8080/api/v1/config/all"
        header={'Content-Type':'Application/json'}
               
        r=requests.post(url=api_endpoint,data=json_obj,headers=header)
        if r:
            azure_response=r.text
            print('Response recieved \n %s' %azure_response)
            print('\n')
            print(vm+' Configuration Successful')
            print('\n')
            print(json.dumps(json_obj, indent=1))
        else:
            print(vm+' Configuration failed')
        
    else:
        print('Invalid VM name')

if __name__=="__main__":
    azure_configIGWandPIP()

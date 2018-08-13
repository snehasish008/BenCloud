from tests.network.azure.utils.nested_dic_lookup import nested_lookup

query_ethernet_intf_name= nested_lookup('name',json_obj)
query_ethernet_intf_priority= nested_lookup('primary',json_obj)
query_ethernet_intf_ipaddr= nested_lookup('privateIPAddress',jsob_obj)


def get_config():
    json_config_dic={}
    json_config_dic.update(interfaces_config())
    json_config_dic.update(tunnels_config())
    json_config_dic.update(publicIPS())
    



def interfaces_config():
    interfaces_list=[]
    interface_dic={}
    interface_dic['Name']=query_ethernet_intf_name[0]
    interface_dic['IPConfigurations']=interfaces_ipconfig()
    interface_dic['Description']='Connected to cloudsimple network'
    interface_dic['IsPrimary']=query_ethernet_intf_priority[1]



def interfaces_ipconfig(json_obj):
    interfaces_ipconfig_list=[]
    interfaces_ipconfig_dic={}
    ethernet_intf_ipaddr= query_ethernet_intf_ipaddr[0]
    ethernet_intf_priority= query_ethernet_intf_priority[0]
    interfaces_ipconfig_dic['IPAddress']=ethernet_intf_ipaddr
    interfaces_ipconfig_dic['IsPrimary']=ethernet_intf_priority





def tunnels_config():
    tunnels_list=[]
    tunnels_dic={}
    tunnel_interface_dic={}
    tunnels_dic['VNI']= 42
    tunnels_dic['LocalVtep']= query_ethernet_intf_ipaddr[0]




def tunnels_ipconfig():
    tunnels_ipconfig_list=[]
    tunnels_ipconfig_dic={}
    



def publicIPs():
    publicIPS_list=[]
    public_IPs_dic={}

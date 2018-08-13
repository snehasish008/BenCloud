#Pre-requisites:
#AZ-CLI needs to be installed in the DUT--> Guideline link( https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest )
#Subscription ID and credential is to be set
#Log in to azure using "az login" (Note: For one device logging in only once is enough in a life-time)
#UnderlayVnet.json file needs to be created manually as per the requirement to deploy the Underlay
#InternetAndPublicIpGateways.parameters.json file needs to be created manually as per the requirement to deploy IGW & PIP

import sys
import glob
import json
import os

arg=sys.argv[1]

def createIGWPIP(InternetVnet_LOC=arg):

    jdata =  json.load(open('InternetAndPublicIpGateways.parameters.BVT_IGWPIP_test.json'))
    string=''
    os.environ["rg"]=str(jdata['resource_group'])
    file_list=glob.glob('UnderlayVnet.*.json')
    for f in file_list:
        string+=f
    if file_list:
        os.system('az group deployment create --resource-group $rg --template-file %s' %string)
    else:
        os.system('az group create --name $rg --location "%s"' %str(jdata['location']))

    os.system('az group deployment create --resource-group $rg --template-file %sInternetAndPublicIpGateways.json --parameters InternetAndPublicIpGateways.parameters.BVT_IGWPIP_test.json' %InternetVnet_LOC)

if __name__=="__main__":
    createIGWPIP()

import os
import glob
os.system('ls -ltr')
os.system('cat ~/.azure/credentials')
store=''
file_list=glob.glob('*_sample.txt')
for f in file_list:
    store+=f
if file_list:
    os.system('more %s' %store)

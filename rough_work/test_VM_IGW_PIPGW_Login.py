
import os
import paramiko

# To log in to jump-box:

jsh = paramiko.SSHClient()
paramiko.util.log_to_file("/home/snehasish/projects/deployment/git_TestAutomation/test-automation/logs/test_Jumpbox.txt")
jsh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
jsh.connect('52.183.83.17', username='swati', password='Password123@.')
#jsh_stdin, jsh_stdout, jsh_stderr = jsh.exec_command('ls')
#print "Output", jsh_stdout.read()
#error = jsh_stderr.read()
#if error:
#    print "err:", error

# To log in to IGW from Jump-box:

ish = paramiko.SSHClient()
paramiko.util.log_to_file("/home/snehasish/projects/deployment/git_TestAutomation/test-automation/logs/test_IGW.txt")
cmd_path = '/usr/sbin/'

# cmd_path variable is taken to mention the entire path where the'ip' cmd resides in IGW & PIPGW.
# During execution path is getting changed coz of the imported modules, which is still to be figured out

ish.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
ish.connect('12.1.3.6', username='csadmin', password=None)
ish_stdin, ish_stdout, ish_stderr = ish.exec_command(cmd_path+'ip rule list')
print "Output", ish_stdout.read()
error = ish_stderr.read()
if error:
        print "err:", error

ish.close()

#To log in to PIPGW from Jump-box:

psh = paramiko.SSHClient()
paramiko.util.log_to_file("/home/snehasish/projects/deployment/git_TestAutomation/test-automation/logs/test_PIPGW.txt")
psh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
psh.connect('12.1.3.4', username='csadmin', password=None)
psh_stdin, psh_stdout, psh_stderr = psh.exec_command(cmd_path+'ip rule list')
print "Output", psh_stdout.read()
error = psh_stderr.read()
if error:
        print "err:", error

psh.close()

jsh.close()

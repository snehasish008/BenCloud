
import os
import paramiko
ssh = paramiko.SSHClient()
paramiko.util.log_to_file("/home/swati/snehasish/logs_sample/log_sample.txt")
cmd_path = '/usr/sbin/'
#cmd_path variable is taken to mention the entire path where the'ip' cmd resides in IGW & PIPGW. During execution path is getting changed coz of the imported modules, which is still to be figured out
ssh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
ssh.connect('12.1.3.6', username='csadmin', password=None)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_path+'ip rule list')
print "Output", ssh_stdout.read()
error = ssh_stderr.read()
if error:
        print "err:", error

ssh.close()

jsh = paramiko.SSHClient()
paramiko.util.log_to_file("/home/swati/snehasish/logs_sample/log_sample.txt")
jsh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
jsh.connect('12.1.3.4', username='csadmin', password=None)
jsh_stdin, jsh_stdout, jsh_stderr = jsh.exec_command(cmd_path+'ip rule list')
print "Output", jsh_stdout.read()
error = jsh_stderr.read()
if error:
        print "err:", error

jsh.close()


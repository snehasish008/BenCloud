import os
import paramiko
#server, username, password = ('host', 'username', 'password')
ssh = paramiko.SSHClient()
paramiko.util.log_to_file("/home/snehasish/rough_work/log_sample.txt")
ssh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
ssh.connect('52.183.83.17', username='swati', password='Password123@.')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls \n cd snehasish \n ssh csadmin@12.1.3.6 \n ip rule list \n exit')
print "Output", ssh_stdout.read()
error = ssh_stderr.read()
if error:
    print "err:", error, len(error)

ssh.close()

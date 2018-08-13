# -*- coding: utf-8 -*-
#
#  Device module
# Author : amodi@cloudsimple.com
# Copyright ©2017 Cloudsimple Inc.
#

from utils.Connection import Connection
from utils.Logger import Logger


class Device (object):

    def __init__(self, infoDict):
        self.__ip = infoDict['ip']
        self.__username = infoDict['username']
        if 'passwordless' in infoDict:
            self.__passwordless = infoDict['passwordless']
            self.__password = ""
        else:
            self.__passwordless = False
            self.__password = infoDict['password']
        self.__logObj = Logger.getInstance()

        if 'os' in infoDict:
            self.__os = infoDict['os']
        else:
            self.__os = None
        self.__connObj = Connection(self.__ip, self.__username, self.__password, self.__passwordless)
        #    '''
        #     ToDo The telnet object association will be done here
        #    '''
        #self.__logObj.info("Telnet connection interface not yet configured")


    def executeCommand(self, command, use_sudo=False):

        self.__sshObj = self.__connObj.ssh()
        if use_sudo:
            command = "sudo " + command
        self.__logObj.info("Running the command %s in the host %s" % (command, self.__ip))
        returnDict = {}
        returnDict['stderr'] = ""
        returnDict['stdout'] = ""

        try:
            stdin, stdout, stderr = self.__sshObj.exec_command(command,get_pty=use_sudo)
            #print "stdout :",stdout.read()

            for line in stdout.readlines():
                returnDict['stdout'] += line
            for line in stderr.readlines():
                if "Warning: Permanently added" not in line:
                    returnDict['stderr'] += line
        except Exception, e:
            self.__logObj.error("Execute command failed to run %s" % (command))
            self.__logObj.error("Exception was %s" % (str(e)))
            returnDict['stderr'] += str(e)
            #return e

        finally:
            self.__sshObj.close()
            return returnDict


    def filetransfer_to_remotehost(self, local_file_path, remote_dest_path, use_sudo=False):

        self.__sshObj = self.__connObj.ssh()
        self.__scpObj = self.__connObj.scp_transfer(self.__sshObj)
        returnDict = {}
        returnDict['stderr'] = ''
        returnDict['stdout'] = ''
        try:
            self.__scpObj.put(local_file_path, remote_dest_path)

        except Exception, e:
            self.__logObj.error("scp failed to transfer file %s to remote host %s" % (local_file_path,self.__ip))
            self.__logObj.error("Exception was %s" % (str(e)))
            returnDict['stderr'] =  str(e)
        finally:
            self.__sshObj.close()
            self.__scpObj.close()
            return returnDict


    def filetransfer_from_remotehost(self, remote_file_path, local_path=".", recursive=True, use_sudo=False):
        self.__connObj = Connection(self.__ip, self.__username, self.__password, self.__passwordless)
        self.__sshObj = self.__connObj.ssh()
        self.__scpObj = self.__connObj.scp_transfer(self.__sshObj)
        returnDict = {}
        returnDict['stderr'] = ''
        returnDict['stdout'] = ''
        try:
            self.__scpObj.get(remote_file_path, local_path, recursive)

        except Exception, e:
            self.__logObj.error("scp  failed to get file %s" % (remote_file_path))
            self.__logObj.error("Exception was %s" % (str(e)))
            returnDict['stderr'] = str(e)
        finally:
            self.__sshObj.close()
            self.__scpObj.close()
            return returnDict


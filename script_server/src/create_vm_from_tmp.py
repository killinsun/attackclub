#!/bin/env python 
# -*- coding: utf-8 -*-
 
import sys
import time
import re
import os
#from paramiko import SSHClient, AutoAddPolicy
import pexpect
 
def main():
	
    (vm_name,Password) = (sys.argv[1],sys.argv[2])
    esxi_name               = "iv11esx01m"
    template_vm             = "iv11-take-zabbix" 
    template_datastore      = "iv11_test_vol_01"
    deploy_target_datastore = "iv11_test_vol_01"
    old_text                = "iv11-take-dummy-vm"
    new_text                = vm_name
    this_file_path          = os.path.dirname(os.path.abspath(__file__))


    #Create vmx file from template vmx file..
    dir_path = this_file_path +  "/../resources/"
    f_old = open(dir_path + old_text +".vmx",'r')
    f_new = open(dir_path + new_text +".vmx",'w')
    print(dir_path)

    for line in f_old:
      new_line = re.sub(old_text, new_text, line.strip())
      f_new.write(new_line + "\n")

    f_old.close()
    f_new.close()


    #Upload vmx file.

   # ssh = SSHClient()
   # ssh.set_missing_host_key_policy(AutoAddPolicy())
   # ssh.connect(esxi_name, 22, "root", Password)
   # sftp = ssh.open_sftp()

    local_file = dir_path + new_text + ".vmx"
    remote_file = "/vmfs/volumes/" + deploy_target_datastore + "/" + vm_name + "/" + vm_name + ".vmx"
   # sftp.put(local_file, remote_file)
   # 
   # sftp.close()
   # ssh.close()
   # 
    child = pexpect.spawn("scp " + local_file + " root@" + esxi_name + ":" + remote_file)
    child.expect("Password:")
    child.sendline(Password)
    print(child.after.decode('utf-8'))
    print(child.before.decode('utf-8'))
    child.close()
    print("section1 complete")
    print("scp " + local_file + " root@" + esxi_name + ":" + remote_file)


    #Delete be created local vmx file.
    vmx_path = remote_file

    child = pexpect.spawn("/usr/bin/ssh root@" + esxi_name)
    child.expect("Password:")
    child.sendline(Password)
    child.expect("~ #")
    child.sendline("vim-cmd solo/registervm " + vmx_path + " " + vm_name)
    print(child.after.decode('utf-8'))
    print(child.before.decode('utf-8'))
    child.expect("~ #")
    print(child.after.decode('utf-8'))
    print(child.before.decode('utf-8'))
    time.sleep(0.1)
    child.close()
 
if __name__ == "__main__": 
        main()

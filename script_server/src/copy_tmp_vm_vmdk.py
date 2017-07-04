#!/bin/env python 
# -*- coding: utf-8 -*-
 
import pexpect
import sys
import time
 
def main():
	
    (vm_name,Password) = (sys.argv[1],sys.argv[2])
    esxi_name               = "iv11esx01m"
    template_vm             = "iv11-take-zabbix" 
    template_datastore      = "iv11_test_vol_01"
    deploy_target_datastore = "iv11_test_vol_01"


    child = pexpect.spawn("/usr/bin/ssh root@" + esxi_name)
    child.expect("Password:")
    child.sendline(Password)
    child.expect("~ #")
    child.sendline("mkdir /vmfs/volumes/" + deploy_target_datastore + "/" + vm_name + "/")
    child.expect("~ #")
    child.sendline("vmkfstools -i /vmfs/volumes/" + template_datastore + "/" + template_vm + "/" + template_vm + ".vmdk /vmfs/volumes/" + deploy_target_datastore + "/" + vm_name +"/" + vm_name +".vmdk -d thin")
    index = child.expect([r"Clone: [0-9][0-9]% done",r"~ #"])
    while True:
      if index == 0:
        child.sendline("")
        index = child.expect([r"Clone: [0-9][0-9]% done",r"~ #"])
        print(child.after.decode('utf-8'))
        time.sleep(10)
      elif index == 1:
        child.sendline("")
        index = child.expect([r"Clone: [0-9][0-9]% done",r"~ #"])
        print("Completed!")
        time.sleep(0.1)
        child.close()
        print(child.after.decode('utf-8'))
        print(child.before.decode('utf-8'))
        break
  
 
if __name__ == "__main__": 
        main()

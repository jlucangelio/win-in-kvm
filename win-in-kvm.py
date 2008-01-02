#!/usr/bin/python

import sys
import os
import time
import shelve
import getpass

import qemumonitor

vmdb = shelve.open("vmdbpy")

argc = len(sys.argv)

if argc < 2:
	print "wik: Usage: %s (add|rm|run) <name> [cmdline] [executable]" % sys.argv[0]
	sys.exit(1)

cmdlilne = ""

if sys.argv[1] == "add" and argc >= 4:
	vmdb[sys.argv[2]] = sys.argv[3]
	vmdb.close()
	sys.exit(0)
elif sys.argv[1] == "rm" and argc >= 3:
	del vmdb[sys.argv[2]]
	vmdb.close()
	sys.exit(0)
elif sys.argv[1] == "run" and argc >= 4:
	cmdline = vmdb[sys.argv[2]]


user = raw_input("wik: Windows username: ")
passwd = getpass.getpass("wik: Windows password: ")

telnet_port = 10000 + os.getpid()

cmdline = "qemu-system-x86_64 %s -daemonize -monitor telnet:localhost:%d,server,nowait -vnc :1" % (cmdline, telnet_port)

os.system(cmdline)
print "wik: Launched VM"
time.sleep(1)

mon = qemumonitor.QEMUMonitor("localhost", telnet_port)
print "wik: Launched monitor"
print "wik: Waiting for VM boot"

ten_secs_wait = 4

for i in range(ten_secs_wait):
	print "wik: %d seconds left" % ((ten_secs_wait - i) * 10)
	time.sleep(10)

os.system("rdesktop -u %s -p %s localhost -s \"%s\" -S standard -D" % (user, passwd, sys.argv[3]))

print "wik: Shutting down VM"
mon.soft_poweroff(user, passwd)

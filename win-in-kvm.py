#!/usr/bin/python

import sys
import os
import time
import shelve

import qemumonitor

vmdb = shelve.open("vmdbpy")

argc = len(sys.argv)

if argc < 2:
	print "Usage: %s (add|rm|run) <name> [cmdline] [executable]" % sys.argv[0]
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

telnet_port = 10000 + os.getpid()

#cmdline = "qemu-system-x86_64 " + cmdline + " -monitor telnet:localhost:%d,server" % telnet_port
cmdline = "qemu-system-x86_64 %s -monitor telnet:localhost:%d,server" % (cmdline, telnet_port)

print cmdline

if not os.fork():
	# child
	os.system(cmdline)
else:
	# parent
	time.sleep(1)

	mon = qemumonitor.QEMUMonitor("localhost", telnet_port)

	time.sleep(60)

	os.system("rdesktop -u Tamsyn -p - localhost -s \"%s\" -S standard -D" % sys.argv[3])

	mon.soft_poweroff("t4m5yn")

	os.wait()

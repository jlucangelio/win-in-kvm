import time
import telnetlib
import logging

class QEMUMonitor:
	def __init__(self, address, port):
		self.address	= address
		self.port	= port

		self.telnet_conn = telnetlib.Telnet(address, port)
		self.telnet_conn.read_until("(qemu) ")
		logging.info("Connected to %s:%d", address, port)

	def quit(self):
		self.telnet_conn.write("quit\n")
		self.close_conn()

	def eject_device(self, device, force):
		if force:
			cmd = "eject -f %s\n"
		else:
			cmd = "eject %s\n"

		self.telnet_conn.write(cmd % device)

	def change_device(self, device, filename):
		self.telnet_conn.write("change %s %s\n" % device, filename)

	def snapshot(self, action, tag): # load, save, del
		self.telnet_conn.write("%svm %s\n" % action, tag)

	def stop(self):
		self.telnet_conn.write("stop\n")

	def cont(self):
		self.telnet_conn.write("cont\n")

	def sendkey(self, key):
		self.telnet_conn.write("sendkey %s\n" % key)

	def sendword(self, word):
		for letter in word:
			key = ""

			if letter.isupper():
				key = "shift-" + letter.lower()
			else:
				key = letter

			self.sendkey(key)
			time.sleep(0.1)

	def soft_poweroff(self, username, password):
		self.sendkey("ctrl-alt-delete")

		time.sleep(0.1)

		self.sendkey("shift-tab")

		self.sendword(username)
		self.sendkey("tab")

		self.sendword(password)
		self.sendkey("ret")

		time.sleep(10)

		self.sendkey("ctrl-alt-delete")

		time.sleep(0.1)

		self.sendkey("alt-shift-s")

		time.sleep(0.1)

		for i in range(3):
			self.sendkey("tab")
			time.sleep(0.1)

		self.sendword("Hypervisor")
		
		self.sendkey("ret")
		
		self.close_conn()

	def hard_reboot(self): 
		self.telnet_conn.write("system_reset\n")
		self.close_conn()

	def hard_poweroff(self):
		self.telnet_conn.write("system_powerdown\n")
		self.close_conn()
	
	def close_conn(self):
		self.telnet_conn.close()

# help|? [cmd] -- show the help
# commit device|all -- commit changes to the disk images (if -snapshot is used) or backing files
# info subcommand -- show various information about the system state
# -q|quit  -- quit the emulator
# -eject [-f] device -- eject a removable media (use -f to force it)
# -change device filename -- change a removable media
# screendump filename -- save screen into PPM image 'filename'
# log item1[,...] -- activate logging of the specified items to '/tmp/qemu.log'
# -savevm tag|id -- save a VM snapshot. If no tag or id are provided, a new snapshot is created
# -loadvm tag|id -- restore a VM snapshot from its tag or id
# -delvm tag|id -- delete a VM snapshot from its tag or id
# -stop  -- stop emulation
# -c|cont  -- resume emulation
# gdbserver [port] -- start gdbserver session (default port=1234)
# x /fmt addr -- virtual memory dump starting at 'addr'
# xp /fmt addr -- physical memory dump starting at 'addr'
# p|print /fmt expr -- print expression value (use $reg for CPU register access)
# i /fmt addr -- I/O port read
# -sendkey keys -- send keys to the VM (e.g. 'sendkey ctrl-alt-f1')
# -system_reset  -- reset the system
# -system_powerdown  -- send system power down event
# sum addr size -- compute the checksum of a memory region
# usb_add device -- add USB device (e.g. 'host:bus.addr' or 'host:vendor_id:product_id')
# usb_del device -- remove USB device 'bus.addr'
# cpu index -- set the default CPU
# mouse_move dx dy [dz] -- send mouse move events
# mouse_button state -- change mouse button state (1=L, 2=M, 4=R)
# mouse_set index -- set which mouse device receives events
# wavcapture path [frequency bits channels] --
# 	capture audio to a wave file (default frequency=44100 bits=16 channels=2)
# stopcapture capture index -- stop capture
# memsave addr size file -- save to disk virtual memory dump starting at 'addr' of size 'size'
# read_disk_io hdx -- read disk I/O statistics (VMDK format)
# migrate [-d] command -- migrate the VM using command (use -d to not wait for command to complete)
# migrate_cancel  -- cancel the current VM migration
# migrate_set_speed value -- set maximum speed (in bytes) for migrations

#m = QEMUMonitor("localhost", 10000)
#m.quit()

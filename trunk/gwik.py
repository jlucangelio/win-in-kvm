#!/usr/bin/python

import os
import time
import subprocess
import shelve
import pygtk
pygtk.require('2.0')
import gtk

import qemumonitor

class GWiK:
    def callback_activate(self, status_icon, user_param1 = None):
        print 'Activated!'

    def callback_popup_menu(self, status_icon, button, activate_time, user_param1 = None):
        self.popup_menu.popup(None, None, None, button, activate_time)

    def callback_menu(self, widget, event):        
        if event == 'popup_quit':
            gtk.main_quit()
            self.vms.close()

        elif event == 'popup_add':
            add_dialog = gtk.Dialog('Add VM', None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    ('Add', 0, 'Cancel', 1))
            
            name_label = gtk.Label('Name')
            add_dialog.vbox.pack_start(name_label, True, True, 0)
            
            name_textbox = gtk.Entry()
            add_dialog.vbox.pack_start(name_textbox, True, True, 0)
        
            cmdline_label = gtk.Label('Command line')
            add_dialog.vbox.pack_start(cmdline_label, True, True, 0)
            
            cmdline_textbox = gtk.Entry()
            cmdline_textbox.set_max_length(1000)
            add_dialog.vbox.pack_start(cmdline_textbox, True, True, 0)
            
            name_label.show()
            name_textbox.show()
            cmdline_label.show()
            cmdline_textbox.show()
            add_dialog.show()
            res = add_dialog.run()
            add_dialog.hide()

            if res == 0:
                self.vms[name_textbox.get_text.strip()] = cmdline_textbox.get_text().strip()
                self.vms.sync()

        elif event == 'popup_launch':
            launch_dialog = gtk.Dialog('Launch VM', None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    ('Launch', 0, 'Cancel', 1))
            
            name_label = gtk.Label('Name')
            launch_dialog.vbox.pack_start(name_label, True, True, 0)
            
            name_textbox = gtk.Entry()
            launch_dialog.vbox.pack_start(name_textbox, True, True, 0)
        
            name_label.show()
            name_textbox.show()
            launch_dialog.show()
            res = launch_dialog.run()
            launch_dialog.hide()

            if res == 0:
                vmname = name_textbox.get_text().strip()

                if vmname in self.vms:
                    telnet_port = 10000 + os.getpid()

                    cmd = 'qemu-system-x86_64 %s' % self.vms[vmname] + \
                    ' -monitor telnet:localhost:%d,server,nowait -vnc :1' % telnet_port

                    cmd = cmd.split()
                    vm = subprocess.Popen(cmd)
                    time.sleep(1)
                    mon = qemumonitor.QEMUMonitor("localhost", telnet_port)
                    self.running_vms_lstore.append([vmname, vm, mon])
                else:
                    print '%s is not a known VM!' % vmname

        elif event == 'popup_active':
            vm_treeview = gtk.TreeView(self.running_vms_lstore)
            cr_text = gtk.CellRendererText()
            cr_togg = gtk.CellRendererToggle()
            cr_togg.set_property('activatable', True)
            cr_togg.set_property('active', True)
            vmname_col = gtk.TreeViewColumn("VM name", cr_text, text=0)
            vmstate_col = gtk.TreeViewColumn("Active", cr_togg)
            cr_togg.connect("toggled", self.callback_tv_toggle, (self.running_vms_lstore, vmstate_col))
            #vmname_column.add_attribute(cellr, "vm-name", 0)
            vm_treeview.append_column(vmname_col)
            vm_treeview.append_column(vmstate_col)

            launch_dialog = gtk.Dialog('Active VMs', None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    ('Close', 0))
            
            vm_treeview.show()
            launch_dialog.vbox.pack_start(vm_treeview)
            launch_dialog.show()
            launch_dialog.run()
            launch_dialog.hide()

        elif event == 'popup_run':
            run_dialog = gtk.Dialog('Run program', None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    ('Run', 0, 'Cancel', 1))
            
            username_label = gtk.Label('Username')
            run_dialog.vbox.pack_start(username_label, True, True, 0)
            
            username_textbox = gtk.Entry()
            run_dialog.vbox.pack_start(username_textbox, True, True, 0)
            
            password_label = gtk.Label('Password')
            run_dialog.vbox.pack_start(password_label, True, True, 0)
            
            password_textbox = gtk.Entry()
            password_textbox.set_visibility(False)
            run_dialog.vbox.pack_start(password_textbox, True, True, 0)
                        
            program_label = gtk.Label('Program')
            run_dialog.vbox.pack_start(program_label, True, True, 0)
            
            program_textbox = gtk.Entry()
            run_dialog.vbox.pack_start(program_textbox, True, True, 0)
            
            username_label.show()
            username_textbox.show()
            password_label.show()
            password_textbox.show()
            program_label.show()
            program_textbox.show()
            run_dialog.show()
            res = run_dialog.run()
            run_dialog.hide()

            program = program_textbox.get_text().strip()

            if res == 0:
                cmd = 'rdesktop -u %s -p %s -s %s -S standard -D localhost' \
                    % (username_textbox.get_text().strip(),
                       password_textbox.get_text().strip(),
                       program)
                
                rdp = subprocess.Popen(cmd, shell=True)
                self.running_rdps[program] = rdp

        elif event == 'popup_rm':
            pass

    def callback_tv_toggle(self, cellr, path, user_data):
      model, column = user_data
      
      mon = model[path][2]
      
      info_dialog = gtk.Dialog('Shutdown', None,
                              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                              ('OK', 0, 'Cancel', 1))
      
      username_label = gtk.Label('Username')
      info_dialog.vbox.pack_start(username_label, True, True, 0)
      
      username_textbox = gtk.Entry()
      info_dialog.vbox.pack_start(username_textbox, True, True, 0)
      
      password_label = gtk.Label('Password')
      info_dialog.vbox.pack_start(password_label, True, True, 0)
            
      password_textbox = gtk.Entry()
      password_textbox.set_visibility(False)
      info_dialog.vbox.pack_start(password_textbox, True, True, 0)

      username_label.show()
      username_textbox.show()
      password_label.show()
      password_textbox.show()
      info_dialog.show()
      res = info_dialog.run()
      info_dialog.hide()

      if res == 0:
          os.system('rdesktop -u %s -p %s -s "shutdown -f -p -d p:4:1" localhost' \
                        % (username_textbox.get_text().strip(),
                           password_textbox.get_text().strip()))

          del model[path]

    def __init__(self):
        self.vms = shelve.open('vmdbpy')
        self.running_rdps = {}

        self.running_vms_lstore = gtk.ListStore(str, object, object)

        # create the status icon
        self.status_icon = gtk.StatusIcon()
    
        #self.status_icon.set_from_file('wik_logo.png')
        self.status_icon.set_from_file('/home/tamsyn/stuff/wik/pengui_icon_128.png')
        self.status_icon.connect('activate', self.callback_activate)
        self.status_icon.connect('popup-menu', self.callback_popup_menu)

        # Create the menu
        self.popup_menu = gtk.Menu()

        # Create the menu items
        self.menu_items = {}

        self.menu_items['run'] = gtk.MenuItem('Run program')
        self.menu_items['add'] = gtk.MenuItem('Add VM')
        self.menu_items['launch'] = gtk.MenuItem('Launch VM')
        self.menu_items['active'] = gtk.MenuItem('Active VMs')
        self.menu_items['rm'] = gtk.MenuItem('Remove VM')
        self.menu_items['quit'] = gtk.MenuItem('Quit')

        # Add them to the menu and make them visible
        # Attach the callback functions to the activate signal
        self.popup_menu.append(self.menu_items['run'])
        self.popup_menu.append(self.menu_items['add'])
        self.popup_menu.append(self.menu_items['launch'])
        self.popup_menu.append(self.menu_items['active'])
        self.popup_menu.append(self.menu_items['rm'])
        self.popup_menu.append(self.menu_items['quit'])

        for name, item in self.menu_items.iteritems():
            item.show()
            item.connect('activate', self.callback_menu, 'popup_' + name)

        # show the status icon
        self.status_icon.set_visible(True)

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

if __name__ == "__main__":
    gwik = GWiK()
    gwik.main()

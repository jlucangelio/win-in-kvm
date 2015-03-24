# Introduction #

This short HOWTO explains how to use win-in-kvm to run Windows programs without having to stare at the Windows desktop.

Before anyone starts asking "Why don't you use WINE?", I can't. I can't use WINE with a 64-bit processor in 64-bit mode, OK?


# Details #

  * **First step**: download and install KVM:

kvm.qumranet.com

  * **Second step**: make sure there's a way to run KVM without having to be root:

http://kvm.qumranet.com/kvmwiki/FAQ#head-69bc2ce5da2f8fc4f1248afefd7bae00fa2dc277

  * **Third step**: install Windows 2003 Server or any Windows with decent Terminal Services support (**make sure you are able to run KVM without being root**):

> qemu-system-x86\_64 -cdrom 

<path\_to\_your\_iso>

 -m 512 -localtime 

<path\_to\_your\_image>

 -net nic,model=rtl8139 -net user

You can create your image using `qemu-img`:

> qemu-img create -f qcow2 

<image\_name>

 

<image\_size>



For example:

> qemu-img create -f qcow2 win2003server.img 10G

  * **Fourth step**: make sure you have either Remote Desktop or Terminal Services active:

Right click on 'My Computer' -> 'Remote' -> 'Enable Remote Desktop on this computer' -> 'Select remote users' -> Check if your user has permissions -> 'OK' -> 'OK'

  * **Fifth step**: make sure you have rdesktop installed!

  * **Sixth step**: use win-in-kvm!

> win-in-kvm.py add 

<name\_of\_vm>

 "-localtime 

<path\_to\_image>

 -m 512 -redir tcp:3389::3389 -redir udp:3389::3389 -net nic,model=rtl8139 -net user"

> win-in-kvm run 

<name\_of\_vm>

 notepad.exe


# TODO #

  * Further shield user from QEMU commandline (possibly using KVM Python script)

  * Check if the VM is already launched

  * Detect if VM has finished booting

  * Provide a known working directory in Windows accessible from Linux

  * Automate Windows install?
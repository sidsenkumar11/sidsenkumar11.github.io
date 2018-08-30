---
title: Arch Install
author: Siddarth Senthilkumar
comments: true
date: 2018-08-30 10:22:05
tags:
- Arch
- Linux
---

{% asset_img refind_bootmanager.bmp %}

After procrastinating for a year, I finally installed Arch Linux on my personal laptop. Unlike the Linux distros I had experience with in the past, Arch Linux is a very bare-bones distribution. While the Mint and Ubuntu installers take care of all the installation details with a nice GUI to guide you through the process, Arch just drops you with a shell and says "you're on your own". But as a reward for having so little assumed for you, you're given fine-grained control over your system and can set it up just the way you like it!

## Motivation
My main motivation in installing Arch was to learn how Linux and my computer worked more deeply. By arming myself with nothing but the Wiki and the Arch ISO, I figured I would learn a lot from performing the installation steps manually - and I was right!

Here are some of the notes I took during the installation procedures. While this little post is no replacement for the Arch Wiki, I wanted to document my steps so I can refer to them if I ever decide to migrate to a new computer.

## Cautions while Dual-Booting with Windows

### Set Windows to UTC Time
If you are dual-booting alongside Windows like me, you will want to set your Windows time to use UTC time instead of localtime. Linux treats the hardware clock as if it's UTC time and computes the localtime from that, but Windows treats the hardware clock as if it's localtime. Therefore, after installing Arch, you may notice that your Windows clock will be off by several hours.

See [https://wiki.archlinux.org/index.php/time#UTC_in_Windows](https://wiki.archlinux.org/index.php/time#UTC_in_Windows) to figure out how to fix this before it becomes a problem.

### Disable Fast Boot
Windows has a feature called Fast Start-Up that hibernates the computer instead of shutting it down to decrease the boot times. This can cause data corruption if you shutdown your Windows machine and boot your Linux machine, since the Linux machine will mount the hibernated file system.

See [https://wiki.archlinux.org/index.php/Dual_boot_with_Windows#Fast_Start-Up](https://wiki.archlinux.org/index.php/Dual_boot_with_Windows#Fast_Start-Up) to figure out how to disable fast boot before it becomes an issue.

### Secure Boot
Before starting the installer, you may wish to enter your BIOS menu (hit F12 during boot) and disable Secure Boot to make your installation simpler.

## Connect to Internet and Set Clock

This installation was done on a machine that supports UEFI, so these steps were written as such. For older BIOS machines, you will want to refer to the Arch wiki.

First, press F12 at the hardware vendor loading screen to load the BIOS settings.
Then, select `UEFI BOOT from USB` to boot from the USB that contains your Arch ISO.
You should see the operating system on your USB boot up, eventually dropping you into a root shell.

```sh
# --------------------------
# Confirm UEFI Mode
# --------------------------
# If this directory is populated, you're in UEFI.
ls /sys/firmware/efi/efivars

# --------------------------
# Change Keyboard Layout
# --------------------------
# The default keyboard layout is US.
# See Arch guide if you want to change it to something else.

# --------------------------
# Connect to Internet
# --------------------------
# If you have an Ethernet cable, you can plug it in for automatic internet.
# Otherwise, you can use wireless.
wifi-menu
ping google.com # Test connection

# --------------------------
# Update the System Clock
# --------------------------
timedatectl set-ntp true
timedatectl status # Check status
```

## Partitioning Disks

Before you install Arch somewhere, you will need to partition your hard disk into segments that hold different pieces of your operating system. How you decide to partition is a matter of preference, but there are some basic partitions that everyone should consider:

Partition | Notes
--- | ---
Root | Main partition that contains programs and files.
Boot | The EFI System partition. Typically ~512 MB but some OSes make it smaller (like Windows, which uses 99MB). You don't need to remake the EFI System partition if it already exists.
Swap | Should be your RAM + 3GB else hibernate may not work.
Shared | Optional: Windows can only read NTFS file systems, so it may help to set aside a partition as a shared drive between Linux and Windows.
Home | Optional: Can be used to share files between Linux distributions if you have more than one. Not recommended to make this a separate partition unless you know what you're doing.

In my case, I went with the first four. My machine supported GPT partitioning as opposed to the older MBR scheme, so I went with GPT.

```sh
# --------------------------
# Note Existing Drives and Partitions
# --------------------------
lsblk # Lists the block devices
fdisk -l  # Show parittions, sizes, and types

# --------------------------
# Partition the Drives
# --------------------------
# d deletes partitions.
# n adds new partitions.
# w writes table to disk.
fdisk /dev/sdx # Use for MBR
gdisk /dev/sdx # Use for GPT
```

After partitioning, you will want to format each partition with an appropriate file system. Here are a few choices:

File System | Notes
--- | ---
ext4 | Most stable.
btrfs | Unstable, but probably the future of file systems.
tmpfs | Good for storage of temporary files; is the default for /tmp in Arch.
ntfs | Windows readable.
FAT | Used for EFI System Partition.

I went with vanilla ext4 for my root partition.

```sh
# --------------------------
# Format Partitions
# --------------------------

# For each partition (root, home, etc.)
mkfs.ext4 /dev/sdxy

# For Swap
mkswap /dev/sdxy
swapon /dev/sdxy

# --------------------------
# Mount the root file system to /mnt
# --------------------------
mount /dev/sdxy /mnt

# --------------------------
# Mount any remaining partitions except swap.
# --------------------------
# With Windows, just mount EFI partition as /mnt/boot
mkdir -p /mnt/boot
mount /dev/sdxy /mnt/boot
```

Here is my final partition scheme.


FS Type | Code | SDA | Size | Name
--- | --- | --- | --- | ---
 | 2700 | 1 | 499 MB | Windows/OEM Dell Recovery Environment
FAT | EF00 | 2 | 99 MB | EFI System Partition (ESP)
 | 0C01 | 3 | 16 MB | MSR Partition
NTFS | 0700 | 4 | 456.1 GB | Windows C-Drive
NTFS | 0700 | 5 | 10 GB | Winshare
 | 8200 | 6 | 11 GB | Swap
ext4 | 8304 | 7 | 400 GB | Arch x86_64 root (/)
ext4 | 8304 | 8 | 53.8 GB | Unallocated

## Install

Now, we are ready to install the base packages.

```sh
# --------------------------
# Select a Mirror
# --------------------------
# Move a US mirror near the top to the very top of the mirror list.
vim /etc/pacman.d/mirrorlist

# --------------------------
# Install Packages
# --------------------------
# base is needed.
# base-devel is needed for building packages (useful for developers).
# Make sure this finishes without errors or the following steps may not work.
pacstrap /mnt base base-devel

# --------------------------
# Generate fstab file with UUIDs option
# --------------------------
genfstab -U /mnt >> /mnt/etc/fstab

# --------------------------
# Change root to new FS
# --------------------------
arch-chroot /mnt

# --------------------------
# Get vim ;)
# --------------------------
pacman -S vim

# --------------------------
# Set Timezone
# --------------------------
ln -sf /usr/share/zoneinfo/New_York /etc/localtime
hwclock --systohc

# --------------------------
# Generate Locales
# --------------------------
# Search and uncomment "en_US.UTF-8 UTF-8".
# Uncomment and any other localisations needed.
vim /etc/locale.gen
locale-gen
vim /etc/locale.conf # Enter LANG=en_US.UTF-8

# --------------------------
# Create Hostname File
# --------------------------
# Enter only one line, the hostname you want
# Ex. user@emerald -> emerald is the hostname
vim /etc/hostname
# Add hostname to hosts file.
# a. Add this line
# 127.0.1.1 	<myhostname>.localdomain	<myhostname>
# b. Put myhostname at the end of the other lines too
# 127.0.0.1 	... 	localhost	myhostname
# ::1 		... 	localhost	myhostname
vim /etc/hosts

# --------------------------
# Install Wireless Packages
# --------------------------
# You may need to install additional firmware packages to use wireless.
pacman -S iw wpa_supplicant dialog

# --------------------------
# Install Useful Software
# --------------------------
# net-tools give you ifconfig
pacman -S wget net-tools

# --------------------------
# Set Root Password
# --------------------------
passwd
```

## Boot Managers and Kernels

The base installation is complete. We now need a way to make sure we can boot into our new Linux system. I used the rEFInd boot manager with a custom theme to accomplish this, though you can use GRUB too.

```sh
# --------------------------
# Install intel-ucode for Intel Processors
# --------------------------
pacman -S intel-ucode

# --------------------------
# Install rEFInd
# --------------------------
pacman -S refind-efi
refind-install

# Note: You must adjust kernel options in /boot/refind-linux.conf manually.
# rEFInd cannot populate the proper boot entries while running refind-install from
# a bootable flash drive.

# --------------------------
# Get Root Partition's UUID
# --------------------------
ls -l /dev/disk/by-uuid

# --------------------------
# Create Arch Folder for Kernel
# --------------------------
# By making the parent directory of the kernel "arch", rEFInd will display
# an icon for Arch Linux on the boot screen.
cd /boot && mkdir arch
mv vmlinuz-linux intel-ucode.img refind_linux.conf initramfs-linux.img initramfs-linux-fallback.img arch

# --------------------------
# Update refind-linux.conf
# --------------------------
vim /boot/arch/refind-linux.conf

# Update config file:
# "Boot with standard options"  "root=UUID=<UUID_root> rw initrd=/boot/arch/intel-ucode.img initrd=/boot/arch/initramfs-linux.img quiet splash"

# NOTE 1: If /boot is on a different partition,
#         then instead of /boot/arch/intel-ucode.img, put arch/intel-ucode.img.
#         Same with anything found in the /boot partition (initramfs-linux.img).
# NOTE 2: intel-ucode must be before initramfs.
# NOTE 3: You can delete the other two boot options if you want
#         (the ones other than "Boot with standard options").
# NOTE 4: Here are some of the useful kernel parameters.
# quiet - Don't display every single systemd message on boot;
#         just important ones like errors and warnings.
# root=UUID=... - Tells kernel which partition has the root filesystem.
# initrd = ... - Loads these images, enables microcode updates.

# --------------------------
# Update refind.conf
# --------------------------
# Check saved settings on GitHub
vim /boot/EFI/refind/refind.conf

# --------------------------
# Download rEFInd Icons / Theme in /boot/EFI/refind
# --------------------------
# Replace icons directory with custom icons from GitHub
# Replace background.png, selection-big.png, selection-small.png

# --------------------------
# Exit and Reboot
# --------------------------
exit # Exits chroot environment
umount -R /mnt # Unmounts partitions
reboot # Reboots into actual system
```

## Results
Awesome! After the above steps, you should be able to see a boot manager like the one at the beginning of this article whenever you boot, allowing you to boot into your newly installed Arch or your existing Windows operating system. In my next post, I will discuss how you can set up and customize your new Arch Linux.

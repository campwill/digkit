# Registry Hive Collection via Live USB

During physical penetration testing engagements, gaining access to credentials stored on a target machine can be a critical step. This tool is a Live USB-based utility designed to collect Windows Registry hives from a powered-off or locked Windows system — even if it is protected by a login password.

This Live USB tool automates the process of mounting the target system's filesystem (in read-only mode) and extracting the following registry hives:

- SAM
- SYSTEM
- SECURITY
- SOFTWARE
- DEFAULT

These hives can then be analyzed offline using tools such as Impacket's secretsdump.py to extract:

- Local account password hashes (e.g., NTLM hashes)
- Cached domain credentials (if available)
- LSA secrets

## Compatability

The collection of Registry hives will work if even if the target Windows system is:

- Powered Off
- Locked (login screen or sleep mode)
- Offline (but physically accessible)

*It is important to note that this tool will not work on Windows computers that utilize BitLocker encryption.

## Setup

The USB drive is partitioned to support a bootable Debian Live environment with persistence and a dedicated space for saving registry hives. Below is the partition scheme for the USB drive.

| Partition   | Label         | Filesystem | Purpose                                              |
| ----------- | ------------- | ---------- | ---------------------------------------------------- |
| `/dev/sdX1` | `D-LIVE 12_6` | FAT32      | Bootable partition for Debian Live system            |
| `/dev/sdX2` | `persistence` | EXT4       | Persistent storage for the live environment          |
| `/dev/sdX3` | `REGSAVE`     | FAT32      | Writable partition to store extracted Registry hives |

For the live USB environment, I utilized the standard live version of [Debian](https://mirror.accum.se/mirror/cdimage/archive/12.6.0-live/amd64/iso-hybrid/), which I setup (along with the persistence partition) using [Rufus](https://rufus.ie/en/).

With the live USB built, configurations to the environment must be made:

1. Edit `/boot/grub/grub.cfg` on the bootable parition and add `timeout=0` to the top of the file to remove the boot menu delay.

2. Boot into the live USB environment and move the files in this repository to the following directories:
    - `registry_collector.sh` -> `/home/user/Scripts/registry_collector.sh`
    - `registry_collector.service` -> `/etc/systemd/system/registry_collector.service`
    - `Packages/*' -> `/home/user/Packages/*`

3. Run the following commands in the live USB environment:
    - `sudo chmod +x /usr/local/bin/myscript.sh`
    - `sudo dkpg -i /home/user/Packages/libntfs-3g89_2022.10.3-1+deb12u2_amd64.deb`
    - `sudo dkpg -i /home/user/Packages/libfuse3-3_3.14.0-4_amd64.deb`
    - `sudo dkpg -i /home/user/Packages/fuse3_3.14.0-4_amd64.deb`
    - `sudo dkpg -i /home/user/Packages/ntfs-3g_2022.10.3-1+deb12u2_amd64.deb`
    - `sudo systemctl daemon-reexec`
    - `sudo systemctl daemon-reload`
    - `sudo systemctl enable registry_collector.service`

4. Shutdown the live USB environment.

## Usage

1. First, confirm that the target Windows computer is powered off or locked with an unknown password. If not powered off, power down the computer.
2. Plug the live USB into an available USB port on the target Windows computer.
3. Power on the target Windows computer, access the boot menu (if available), and boot into the live USB environment.
4. Once the live USB environment boots, the Registry hives will be collected from the target Windows computer (if available).


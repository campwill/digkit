#!/bin/bash

clear

WIN_PART=""
WIN_MNT=$(mktemp -d)
REGSAVE_MNT=$(mktemp -d)

echo "[*] Searching for Windows partition..."

PARTS=$(lsblk -lnpo NAME,FSTYPE | grep -i ntfs | awk '{print $1}')

for dev in $PARTS; do
  echo "[*] Trying $dev..."
  if mount -o ro "$dev" "$WIN_MNT" &>/dev/null; then
    echo "  [+] Mounted $dev"
    if [ -d "$WIN_MNT/Windows/System32/config" ]; then
      WIN_PART=$dev
      echo "  [+] Found Windows registry folder in $WIN_PART"
      break
    else
      echo "  [-] No registry folder"
    fi
    umount "$WIN_MNT"
  else
    echo "  [-] Could not mount $dev"
  fi
done

if [ -z "$WIN_PART" ]; then
  echo "[-] No Windows partition found."
  rmdir "$WIN_MNT"
  exit 1
fi

echo "[*] Searching for REGSAVE partition..."

REGSAVE_PART=$(lsblk -lnpo NAME,FSTYPE,LABEL | grep vfat | grep REGSAVE | awk '{print $1}')

if [ -z "$REGSAVE_PART" ]; then
  echo "[-] No REGSAVE partition found."
  umount "$WIN_MNT"
  rmdir "$WIN_MNT"
  exit 1
fi

echo "[*] Mounting REGSAVE partition $REGSAVE_PART ..."
if mount "$REGSAVE_PART" "$REGSAVE_MNT"; then
  echo "[+] Mounted REGSAVE partition"
else
  echo "[-] Failed to mount REGSAVE partition"
  umount "$WIN_MNT"
  rmdir "$WIN_MNT"
  rmdir "$REGSAVE_MNT"
  exit 1
fi

SAVE_DIR="$REGSAVE_MNT/Collected Hives/registry_backups_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SAVE_DIR"

echo "[*] Copying registry hives to $SAVE_DIR..."
for hive in SYSTEM SOFTWARE SAM SECURITY DEFAULT; do
  if cp "$WIN_MNT/Windows/System32/config/$hive" "$SAVE_DIR/"; then
    echo "   [+] Copied $hive"
  else
    echo "[-] Failed to copy $hive"
  fi
done

umount "$WIN_MNT"
umount "$REGSAVE_MNT"
rmdir "$WIN_MNT"
rmdir "$REGSAVE_MNT"

echo "[*] Registry collection complete."
echo "[*] Powering off..."
poweroff -f &>/dev/null
exit 0

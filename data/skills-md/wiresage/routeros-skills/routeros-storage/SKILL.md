---
name: routeros-storage
description: Storage on MikroTik RouterOS 7. Covers drive detection and slot names, formatting (ext4, fat32, exfat, btrfs, xfs, wipe), mount points and templates, partitions, swap, tmpfs and ramdisk, mounting images, safe removal, check and repair, S.M.A.R.T., the Storage package (rose-storage) with RAID levels 0, 1, 4, 5, 6 and nested, Btrfs RAID, subvolumes and snapshots, dm-crypt and self-encrypting drives, network storage (SMB server and client, NFS v4, iSCSI, NVMe over TCP, SSHFS, rsync) and the DLNA media server. Use when adding or sharing a USB, SATA or NVMe disk, moving logs or caches off flash, building a RAID, or exporting storage to other devices.
---

# RouterOS storage

RouterOS detects USB, SATA, NVMe and microSD drives and mounts supported ones automatically. Everything lives in `/disk`; files appear in `/file`
under the mount point. The base system has the SMB server and DLNA media server; the **Storage package** (`rose-storage` in `/system/package/print`; arm, arm64,
x86 and tile) adds SMART, Btrfs and XFS, RAID, rsync, iSCSI, NVMe over TCP, NFS and the SMB client. Enable it with
`/system/package/enable rose-storage` then `/system/package/apply-changes` (reboots; `routeros-install-upgrade`). Drives with power loss protection are recommended for reliability.

## Disks

```ros
/disk/print                                                  # slot (usb1, sata1, nvme1), flags B block device, M mounted, E empty
/disk/format nvme9 file-system=ext4                          # destroys all data; label defaults to <slot>-fs
/disk/set nvme1 mount-point-template="[serial]"             # stable mount point; variables: slot model serial fw-version fs-label fs-uuid fs
/disk/add type=partition parent=nvme9 partition-size=4G     # GPT partitions: nvme9-part1, ...
/disk/eject usb1                                             # ALWAYS before unplugging
/disk/check nvme9-part1                                      # fsck for ext4, Btrfs, XFS; fails if the file system is in use
/disk/smart-info nvme1                                       # needs the Storage package
```

- File systems: `ext4` (default), `fat32` (4 GB file limit), `exfat`, `btrfs` and `xfs` (Storage package), `discard`/`discard-secure`, `wipe` (overwrites) and `wipe-quick`.
  `mbr-partition-table=yes` only when the target cannot read GPT.
- Swap is for containers only (container package): `/disk/set <partition> swap=yes` or a swap file `/disk/add type=file file-path=<disk>/swapfile file-size=512M swap=yes`;
  limit is 10 times the available RAM.
- Mount an `.iso` or `.squashfs` with `/disk/add type=file file-path=disk1/mycopy.iso`.
- Moving heavy writers off internal flash: logs (`/system/logging/action/set disk disk-file-name=disk1/log`, create the folder first), packet captures, the web proxy cache
  (`/ip/proxy/set cache-path=usb1/cache-n-db/proxy/`), the User Manager database, container storage. Logging topics such as firewall and web-proxy wear NAND quickly.
- RAM folders: `/disk/add type=tmpfs tmpfs-max-size=100M` (appears as `tmp1`, RAM used only by stored files, emptied at reboot) for captures and downloads.
  `/disk/add type=ramdisk ramdisk-size=500M` is a block device in RAM (package `rose-storage`), must be formatted after every reboot, can be a RAID member for tests.

## RAID, Btrfs, encryption

```ros
/disk/add type=raid slot=raid1 raid-type=1 raid-device-count=2
/disk/set nvme1 raid-master=raid1 raid-role=0
/disk/set nvme2 raid-master=raid1 raid-role=1
/disk/format raid1 file-system=btrfs
/disk/add type=crypted slot=crypted-usb1 crypted-backend=usb1 encryption-key="REPLACE-ME"
/disk/set sata1 self-encryption-password="REPLACE-ME"        # TCG-Opal drive, flag o becomes O
```

- RAID types 0, 1, 4, 5, 6, linear and nested; a replaced failed drive rebuilds automatically; hot spare and array moves have their own guides. Plan RAID
  as availability, not as backup.
- Btrfs: copy-on-write, subvolumes, snapshots, snapshot transfer (`/disk/btrfs/filesystem`, `subvolume`, `transfer`), RAID1/RAID10 with bitrot protection, periodic scrub and balance
  (maintenance guide). dm-crypt (`type=crypted`) can sit on a drive or a RAID and then be formatted. SED needs direct SATA or NVMe, not a USB bridge, and the drive locks
  at power loss. Encryption keys and passwords in commands end up in exports and history.

## Network storage

| Protocol | Server side | Client side | Port |
| --- | --- | --- | --- |
| SMB (SMB 2.1, 3.0, 3.1.1; no SMB1) | `/ip/smb/shares/add name=backup directory=backup`, `/ip/smb/users/add name=mtuser password=... read-only=no` | SMB client mounts remote shares as disks (Storage package) | TCP 445 |
| NFS v4 | `/disk/set <disk> nfs-sharing=yes` | `/disk/add type=nfs nfs-address=192.168.1.1` | TCP 2049 |
| iSCSI | `/disk/set <disk> iscsi-export=yes` | `/disk/add type=iscsi iscsi-address=192.168.1.1 iscsi-iqn=iqn.2000-02.com.mikrotik:<slot>` | TCP 3260 |
| NVMe over TCP | `/disk/set <disk> nvme-tcp-export=yes nvme-tcp-port=4420` | `/disk/add type=nvme-tcp nvme-tcp-address=192.168.1.1 nvme-tcp-name=<disk>` | TCP 4420 |
| SSHFS | any SSH server | `/disk/add type=sshfs sshfs-address=... sshfs-user=... sshfs-path=/srv/files` | TCP 22 |
| rsync | `/file/rsync-daemon/set enabled=yes` | `/file/sync/add local-path=... mode=upload remote-address=... remote-path=...` | TCP 873, with a password also UDP 500 and ESP |

- SMB: the server starts when the first share exists (`enabled=auto`); users are read-only by default and the `guest` user is disabled; use `valid-users`,
  `invalid-users` and `require-encryption` per share; not on SMIPS devices. Open these ports only to trusted networks in the input chain (`routeros-firewall`).
- A mount stuck in `mounting` or `making control connection` usually means a blocked port. NFS has no user authentication of its own: limit it by firewall.
- Storage exports and mounts use clear text unless the protocol encrypts (SSHFS does, rsync with a password uses dynamic IPsec).
- **DLNA**: `/ip/media/add friendly-name="Office media" interface=bridge path=usb1/media` shares video, music and pictures with players on that interface. Always set `path`
  (otherwise the whole file list is shared). `allowed-ip` or `allowed-hostname` (one of them) limit a server to one device; files need lower-case extensions. Disks can also create
  servers automatically (`/disk/set usb1 media-sharing=no` turns it off).

## Where to look

| Need | Open |
| --- | --- |
| Detection, format, partitions, swap, tmpfs, mount images, log and proxy on disk | `references/guides/hardware/disks.md` |
| SMART attributes | `references/guides/hardware/disks/smart.md` |
| Storage package overview | `references/guides/storage.md` |
| RAID, hot spare, moving an array | `references/guides/storage/raid.md`, `raid/` |
| Btrfs (RAID, snapshots, scrub, maintenance) | `references/guides/storage/btrfs.md`, `btrfs/` |
| Encryption | `.../encrypted-storage.md`, `.../self-encrypting-drives.md` |
| SMB, NFS, iSCSI, NVMe over TCP, SSHFS, rsync, DLNA | the matching file in `references/guides/storage/` |
| Properties | `references/cli/disk.md`, `references/cli/disk/btrfs/`, `references/cli/ip/smb/`, `references/cli/ip/media.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-containers` (container storage, swap), `routeros-system-utilities` (files, tmpfs), `routeros-diagnostics-monitoring` (logging to disk, sniffer files),
`routeros-hardware` (USB, ports), `routeros-install-upgrade` (packages), `routeros-users-aaa` (accounts).

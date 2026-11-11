---
name: storage-network-mounts
description: Set up, check and repair NFS and SMB/CIFS network mounts on Ubuntu — client packages, discovering exports and shares, testing a mount, persistent fstab or systemd automount entries that don't hang boot, credentials files, ownership mapping, and stale-handle recovery. Use when asked "mount the NAS", "add an NFS share", "mount a Samba/Windows share", "my network drive is not mounted", "stale file handle", "boot hangs on a network mount", or "check NFS mounts". Works on the local machine or a remote host over SSH.
---

# Network mounts (NFS and SMB)

## Target

Local by default. Remote: `ssh -t <host> 'sudo <cmd>'`. Placeholders: `<nas>` (server hostname), `<export>` / `<share>`, `<mnt>` (local mount point).

## 1. Check existing mounts

```bash
findmnt -t nfs,nfs4,cifs,smb3 -o TARGET,SOURCE,FSTYPE,OPTIONS
grep -E '\s(nfs4?|cifs)\s' /etc/fstab
systemctl list-units --type=mount,automount --all --no-pager | grep -iE 'nfs|cifs|mnt|media'
for m in $(findmnt -rn -t nfs,nfs4,cifs -o TARGET); do timeout 5 stat -t "$m" >/dev/null && echo "OK $m" || echo "HUNG/STALE $m"; done
```

Stale NFS handle → `sudo umount -f <mnt>` (or `-l` lazy) then remount. Hung CIFS mount → `sudo umount -l <mnt>`.

## 2. NFS

```bash
sudo apt install -y nfs-common
showmount -e <nas>                         # NFSv3 export list; NFSv4-only servers may not answer
sudo mkdir -p <mnt>
sudo mount -t nfs4 <nas>:/<export> <mnt>   # test first, by hand
ls <mnt> && touch <mnt>/.write-test && rm <mnt>/.write-test
```

Persistent entry (`/etc/fstab`):

```
<nas>:/<export>  <mnt>  nfs4  _netdev,nofail,x-systemd.automount,x-systemd.idle-timeout=600,noatime  0 0
```

UID/GID must match between client and server (NFS maps by number unless the server uses `all_squash`/`anonuid`).

## 3. SMB / CIFS

```bash
sudo apt install -y cifs-utils smbclient
smbclient -L //<nas> -U <user>               # list shares
sudo install -m 600 -o root -g root /dev/null /etc/samba/credentials-<nas>
sudoedit /etc/samba/credentials-<nas>        # username=…  password=…  domain=… (optional)
sudo mkdir -p <mnt>
sudo mount -t cifs //<nas>/<share> <mnt> -o credentials=/etc/samba/credentials-<nas>,uid=$(id -u),gid=$(id -g),vers=3.1.1
```

Persistent entry:

```
//<nas>/<share>  <mnt>  cifs  credentials=/etc/samba/credentials-<nas>,uid=1000,gid=1000,file_mode=0664,dir_mode=0775,vers=3.1.1,_netdev,nofail,x-systemd.automount  0 0
```

Drop to `vers=3.0` or `2.1` only if the server is old; never enable SMB1 (`vers=1.0`) without the user insisting.

## 4. Apply and verify

```bash
sudo findmnt --verify
sudo systemctl daemon-reload
sudo mount -a                       # or: sudo systemctl start <mnt-escaped>.automount
findmnt <mnt>
```

`systemd-escape -p --suffix=automount <mnt>` gives the unit name.

## Desktop vs server

- **Desktop**: for ad-hoc browsing, the file manager's `smb://<nas>/<share>` (GVfs/KIO) needs no fstab. Use fstab only when apps need a stable path. Wi-Fi laptops benefit most from `x-systemd.automount` + `nofail`.
- **Server**: services that depend on the mount should declare it: `RequiresMountsFor=<mnt>` in a unit drop-in, so they don't start writing into the empty mount point.

## Confirm before

- Editing `/etc/fstab` (back it up first: `sudo cp /etc/fstab /etc/fstab.$(date +%F)`).
- Writing a credentials file (the password is stored in plain text, root-only).
- Force/lazy unmounting a mount that processes may be using (`sudo fuser -vm <mnt>` first).

## Report

Mounts found with status (OK / stale / missing), what was added or changed, the exact fstab lines, and the verification result.

## Related

- `network-diagnose` — when `<nas>` is unreachable.
- `files-permissions` — ownership/permission errors on the mounted share.
- `storage-backup` — using a share as a backup target.

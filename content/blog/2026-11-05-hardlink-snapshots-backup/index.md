---
title: "One disk, three months: zero-cost snapshots with hardlinks"
date: 2026-11-05T18:00:00+01:00
draft: false
description: "How to keep a monthly history of a one-terabyte backup without duplicating a single byte. A hardlink is not a copy: it is another name for the same file. The only condition is never to write in place — and almost every backup does it wrong."
image: "figura-hardlinks.svg"
og_image: "figura-hardlinks.svg"
categories:
  - "Technical notes"
tags: ["backup", "hardlinks", "rsync", "ext4", "snapshots", "linux", "systems"]
---

*This is a working note, not an article. It was born while trying to solve a
concrete problem: a one-terabyte backup that needed a monthly history and could
not afford to duplicate it. The code lives in
[backup-remoto-snapshot](https://github.com/javi-jimenez/backup-remoto-snapshot).*

![A single inode at the centre, with two names pointing at it: the live file and the frozen snapshot. Atomic write by rename leaves it untouched; writing in place destroys everything.](figura-hardlinks.svg)

---

## The problem

I have a terabyte to back up. I want to know how it looked three months ago. And
I do not want three terabytes.

The obvious answer — *"make one copy per month"* — does not work at that scale.
Three copies of a terabyte are three disks, and by the third month you no longer
know what is where.

The fashionable answer — *"use btrfs or ZFS"* — works, but it changes the whole
filesystem, and on a machine that is already running that is a risk you cannot
always afford.

There is a third answer, an older one, that almost nobody uses because it has a
reputation for being fragile:

```
cp -al
```

Nine characters. It copies a directory **without copying the data**.

---

## What a hardlink really is

A file on a Unix system is not a name. It is an **inode**: a block of metadata
holding the owner, the permissions, the size, the dates and — the important
part — **the list of disk blocks where the content lives**.

What we call a "file name" is just an entry in a directory that points to an
inode. And **an inode can have several names**. All of them equally real. None of
them is "the original".

```
inode 24598
├── /srv/backup/current/f.txt      ← name 1
└── /srv/backup/202601/f.txt       ← name 2
```

Both take up the same space because **they are the same thing**. There is no
original and copy: there are two doors into the same room.

`cp -al` creates that second name. It walks the tree and, for each file, instead
of copying bytes it calls `link()`. With a terabyte of data it takes seconds and
consumes **zero bytes**.

The number that confirms it:

```bash
$ stat -c '%i %h %n' current/f.txt 202601/f.txt
24598 2 current/f.txt
24598 2 202601/f.txt
```

Same inode (`24598`), link count `2`. Two names, one content.

---

## The condition that breaks everything

Here is the part almost nobody explains, and the reason hardlink snapshots have
a bad reputation.

**Any in-place write to a file changes all of its names.** Not the previous
names: *all* of them, because the content is unique.

If tomorrow the backup opens `current/f.txt` and writes over it, `202601/f.txt`
changes too. The snapshot stops being a history and becomes an alias of the
present.

### The difference that saves it: `rename()`

When `rsync -a` detects that a file changed, it does not open it for writing. It
does this:

1. Copies the new content to `f.txt.a1B2c3` (a temporary file).
2. Calls `rename("f.txt.a1B2c3", "f.txt")`.

`rename()` is an **atomic** filesystem operation: either it happens entirely or
it does not happen. And when it happens, **what it replaces is the name, not the
inode**.

```
BEFORE:  current/f.txt ──→ inode 24598 ←── 202601/f.txt
AFTER:   current/f.txt ──→ inode 24604
         202601/f.txt  ──→ inode 24598   ← untouched
```

The old inode loses one name (`link count` drops from 2 to 1), but **nobody has
touched it**. The snapshot keeps exactly what it said.

Verified:

```bash
$ cat current/f.txt   →  V2-CHANGED
$ cat 202601/f.txt    →  V1            ← the history works
$ stat -c '%i %h %n' current/f.txt 202601/f.txt
24604 1 current/f.txt      ← new inode
24598 1 202601/f.txt       ← old inode, untouched
```

That is why `cp -al` is not fragile. **It is fragile if the client writes badly.**

---

## What corrupts, and what does not

| Write | What it does | Snapshots |
|:---|:---|:---|
| `rsync -a` | `.tmp` + `rename()` | ✅ untouched |
| `rsync --inplace` | writes onto the inode | ❌ **breaks all of them** |
| `rclone --inplace` | writes onto the inode | ❌ **breaks all of them** |
| `rclone sync` (same size) | rewrites in place | ❌ **breaks all of them** |
| `cp` without `-a` | truncates and writes | ❌ **breaks all of them** |
| `-L` / `--copy-links` | turns a link into a copy | ⚠️ breaks deduplication |

The last `rclone` row is the one that took me a while to understand. `rclone
sync` normally creates a new object and renames it, so in theory it is safe. But
**when the file size matches, it rewrites in place** even if you do not pass
`--inplace`. And that is enough to take the history with it.

Practical conclusion: **rclone is not suitable for this scheme.** You have to
use `rsync`.

---

## A failed attempt that taught something

At first I had the server script run `chown -R root` and `chmod -R a-w` on the
freshly created snapshot. The reasoning seemed sound: *"if it belongs to root and
has no write permission, an `--inplace` fails instead of corrupting"*.

It does not work. And the reason is the same one running through the whole
article: **the inode is shared**.

```
chown root 202601/f.txt   →  changes the owner of the inode
                          →  and current/f.txt is the same inode
                          →  now the client cannot write to its own destination
```

You break the destination in order to "protect" the copy. An inode cannot belong
to root in the snapshot and to another user in `current/`: it is the same object.

The lesson: **in a hardlink scheme you cannot have different permissions for the
copy and the original**, because they are not two things. The protection has to
come from the way you write, not from permissions.

---

## The complete system

Two scripts and two cron lines.

### Server

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE="${BACKUP_BASE:-/srv/backup}"
MONTH="$(date +%Y%m)"

[[ -e "$BASE/$MONTH" ]] && { echo "$BASE/$MONTH already exists."; exit 0; }
[[ -d "$BASE/current" ]] || { echo "current/ does not exist." >&2; exit 1; }
[[ "$(stat -c %d "$BASE")" == "$(stat -c %d "$BASE/current")" ]] \
  || { echo "Different filesystems." >&2; exit 1; }

cp -al "$BASE/current" "$BASE/$MONTH"
echo "Created $BASE/$MONTH ($(find "$BASE/$MONTH" -type f | wc -l) files, 0 bytes)"
```

Nothing else. No `chown`, no `chmod`, no deleting old snapshots.

### Client

`rsync -a --delete` with exclusions, a `flock` lock and a log. No `--inplace`, no
`-L`.

### Cron

**Server:** daily, not on the 1st.

```cron
30 3 * * * /usr/local/bin/snapshot-monthly.sh >> /var/log/snapshot-monthly.log 2>&1
```

The script exits as soon as it sees that the month's snapshot already exists, so
it only does work once a month. If the server was off on the 1st, the snapshot is
created on the first day it boots.

**Client:** `anacron`, not `cron`.

```
1  10  backup-client  /home/user/.local/bin/backup-client.sh
```

A normal `cron` only fires if the machine is on at that time. On a laptop, the
02:00 backup **never** happens: at 02:00 the laptop is closed. `anacron` records
when it was due and runs it at boot if the time has passed.

You switch the computer on in the morning and the backup that did not happen last
night runs on its own while you make your coffee.

Verified: the second month costs **0 bytes**.

---

## What this does not do

- **It does not backfill missed months.** If the machine was off from January to
  April, in April only `202604` is created. A snapshot's name is the date it was
  taken, not the date it should have had. A missing snapshot says something; a
  fake one does not.
- **It does not delete old snapshots.** That is your decision, not a script's
  `find -mtime`.
- **It does not encrypt.** That belongs to the transport (SSH) or to the volume.
- **It does not replace a 3-2-1 strategy.** This is *one* copy. A backup in the
  same building is not a backup.
- **It does not work on QNAP, FAT/exFAT or network mounts** without hardlink
  support. `cp -al` fails and the script exits with an error, which is the
  correct behaviour.

---

## Why this still matters

We live in a time when the answer to everything is "use ZFS" or "use btrfs". And
they are not wrong: they are better. They have native snapshots, checksums,
incremental send/receive and they do not depend on the client behaving well.

But they require changing the filesystem of a machine that works. And on a modest
server, on an external disk, or on a machine you cannot reinstall, that is
sometimes not an option.

`cp -al` needs nothing. It works on ext4, which is what everyone has. It takes
zero bytes. And if you respect a single rule — **never write in place** — it
preserves the history exactly like ZFS does.

The rule is not a detail: it is the whole system. A backup that writes in place
is not an incremental backup, it is a copy that believes itself.

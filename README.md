rsnapstats
==========

Prints out statistics from rsnapshot run. Based on rsnapreport.pl

Tested with rsnapshot 1.3.1 and rsync 3.1.0

Usage
==========
 1. In the rsnapshot.conf set verbose >= 4
 2. Also add --stats to rsync_long_args in the rsnapshot.conf
 3. To mail the stats to yourself setup crontab with:

      `rsnapshot daily 2>&1 | python /path/to/rsnapstats.py 2>&1 | mail -s"SUBJECT" backupadm@adm.com`

    Or to append the stats to the rsnapshot.log file setup crontab with:

      `rsnapshot daily 2>&1 | python /path/to/rsnapstats.py 2>&1 >> /var/log/rsnapshot.log`

    Setup the crontab with the lowest rsnapshot interval if 'daily' is not the lowest interval.
    Dont forget the 2>&1 or your errors will be lost to stderr

Example output
==========
Here is an example of the statistics printed by rsnapstats:
```
/etc
	 files backed-up: 2711 (4.65 MB)
	 files updated: 5 (44.74 kB)
	 sent/received: 98.53 kB / 8.36 kB
	 transfer rate: 42.76 kB/sec
	 speedup: 44.59
/usr/local
	 files backed-up: 999 (227.61 MB)
	 files updated: 0 (0.00 bytes)
	 sent/received: 25.37 kB / 3.19 kB
	 transfer rate: 19.04 kB/sec
	 speedup: 8161.92
/home
	 files backed-up: 165397 (145.15 GB)
	 files updated: 1791 (3.46 GB)
	 sent/received: 2.14 GB / 532.44 kB
	 transfer rate: 2.84 MB/sec
	 speedup: 67.73
server1:/home
	 files backed-up: 3035 (13.14 GB)
	 files updated: 8 (48.62 kB)
	 sent/received: 18.55 kB / 150.95 kB
	 transfer rate: 26.08 kB/sec
	 speedup: 81293.82
server2:/home
	 files backed-up: 63749 (96.26 GB)
	 files updated: 105 (626.81 MB)
	 sent/received: 205.28 kB / 575.51 MB
	 transfer rate: 466.59 kB/sec
	 speedup: 171.22
```

rsnapstats
==========

Prints out stats from rsnapshot run. Inspired by rsnapreport.pl
Tested with rsnapshot 1.3.1 and rsync 3.0.7

Usage
==========
 1. In the rsnapshot.conf set verbose >= 3
 2. Also add --stats to rsync_long_args in the rsnapshot.conf
 3. To mail the stats to yourself setup crontab with:

      rsnapshot daily 2>&1 | python /path/to/rsnapstats.py 2>&1 | mail -s"SUBJECT" backupadm@adm.com

    Or to append the stats to the rsnapshot.log file setup crontab with:

      rsnapshot daily 2>&1 | python /path/to/rsnapstats.py 2>&1 >> /var/log/rsnapshot.log

    Setup the crontab with the lowest rsnapshot interval if 'daily' is not the lowest interval.
    Dont forget the 2>&1 or your errors will be lost to stderr

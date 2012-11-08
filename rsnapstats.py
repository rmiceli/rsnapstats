# rsnapstats
# Prints out statistics from rsnapshot runs.
# Based on rsnapreport.pl by William Bear
#
# Copyright 2012 Rob Miceli
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys

def parseline(line):
  """
    Extracts the number (float or int) from the string 'line' and
    appends it as a float
  """
  dum = []
  words = line.split()
  for ii in words:
    if ii[0].isdigit():
      dum.append(float(ii))
  return dum

def humanize_bytes(bytes, precision=1):
  """
    Return a humanized string representation of a number of bytes
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
  """
  abbrevs = (
      (1<<50L, 'PB'),
      (1<<40L, 'TB'),
      (1<<30L, 'GB'),
      (1<<20L, 'MB'),
      (1<<10L, 'kB'),
      (1, 'bytes')
  )
  if bytes == 1:
      return '1 byte'
  for factor, suffix in abbrevs:
      if bytes >= factor:
          break
  return '%.*f %s' % (precision, bytes / factor, suffix)

def initStats():
  """
    Return a dict of all the stats that rsync outputs
  """
  return dict.fromkeys(['source', 'numFiles', 'numFilesTx', 'fileSize',
          'fileSizeTx', 'litData', 'matchedData', 'listSize', 'listGen',
          'listTx', 'bytesSent', 'bytesRec', 'txSpeed', 'speedup'])


def main():
  # initialize
  stats = []
  line = ''

  # get rsync stats
  for tmp in sys.stdin:
    # combine wrapped lines
    if tmp.strip().endswith('\\'):
      line = line + tmp.replace('\\','')
      continue
    else:
      line = line + tmp

    # sort through line by line
    if "/usr/bin/rsync" in line:
      stats_dict = initStats()
      #src is always second to last argument
      #then remove user name before @
      stats_dict['source'] = line.split()[-2].split('@')[-1]
    elif "rsync error" in line or "ERROR" in line:
      print line
    elif "Number of files:" in line:
      stats_dict['numFiles'] = parseline(line)
    elif "Number of files transferred:" in line:
      stats_dict['numFilesTx'] = parseline(line)
    elif "Total file size:" in line:
      stats_dict['fileSize'] = parseline(line)
    elif "Total transferred file size:" in line:
      stats_dict['fileSizeTx'] = parseline(line)
    elif "Literal data:" in line:
      stats_dict['litData'] = parseline(line)
    elif "Matched data:" in line:
      stats_dict['matchedData'] = parseline(line)
    elif "File list size:" in line:
      stats_dict['listSize'] = parseline(line)
    elif "File list generation time:" in line:
      stats_dict['listGen'] = parseline(line)
    elif "File list transfer time:" in line:
      stats_dict['listTx'] = parseline(line)
    elif "bytes/sec" in line:
      stats_dict['txSpeed'] = parseline(line)
    elif "Total bytes sent:" in line:
      stats_dict['bytesSent'] = parseline(line)
    elif "Total bytes received:" in line:
      stats_dict['bytesRec'] = parseline(line)
    elif "total size is" in line:
      stats_dict['speedup'] = parseline(line)
      stats.append(stats_dict)

    line = ''

  for idx,val in enumerate(stats):
    # print stats
    print stats[idx]['source'], "\n", \
      "\t files backed-up:", int(stats[idx]['numFiles'][0]), "("+humanize_bytes(stats[idx]['fileSize'][0],2)+")\n", \
      "\t files updated:", int(stats[idx]['numFilesTx'][0]), "("+humanize_bytes(stats[idx]['fileSizeTx'][0],2)+")\n", \
      "\t sent/received:", humanize_bytes(stats[idx]['bytesSent'][0],2), "/", humanize_bytes(stats[idx]['bytesRec'][0],2),"\n", \
      "\t transfer rate:", humanize_bytes(stats[idx]['txSpeed'][2],2)+"/sec\n", \
      "\t speedup:", stats[idx]['speedup'][1]

if __name__ == '__main__':
  main()

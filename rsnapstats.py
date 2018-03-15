'''
rsnapstats
Parses and prints statistics from rsnapshot backups
Based on rsnapreport.pl by William Bear

:author: Rob Miceli
:created: 2018 03 12
:copyright: 2018, Rob Miceli
:license: GPL 2.0, see COPYING for more details
'''

import sys

def parseline(line):
    '''
    Extracts the number (float or int) from a string and appends it as a float

    :param line: string of text
    :return: list of numbers contained in input
    '''
  return [float(s) for s in line.replace(',','').split() if s[-1].isdigit()]

def humanize_bytes(bytes, precision=1):
    '''
    Return a humanized string representation of a number of bytes
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'

    :param size_bytes: Size in bytes
    :param precision: Number of decimal places of output
    :return: A humanized string representation of a number of bytes
    '''
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
    '''
    Initialize stats dictionary

    :return: dict with keys for each stats that rsync outputs
    '''
  return dict.fromkeys(['source', 'numFiles', 'numFilesTx', 'fileSize',
          'fileSizeTx', 'litData', 'matchedData', 'listSize', 'listGen',
          'listTx', 'bytesSent', 'bytesRec', 'txSpeed', 'speedup'])

def rstats(object):
  def __init__(self):
    self.source = ''
    self.numFiles = 0
    self.fileSize = 0
    self.fileSizeTx = 0
    self.litData = 0
    self.matchedData = 0
    self.listSize = 0
    self.listGen = 0
    self.listTx = 0
    self.bytesSent = 0
    self.bytesRec = 0
    self.txSpeed = 0
    self.speedup = 0

  def __str__(self,param):
    return humanize_bytes(self.param,2)

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
    if "rsync error" in line or "ERROR" in line or "rsync warning" in line:
      print line
    elif "/usr/bin/rsync" in line and len(line.split()) > 1:
      stats_dict = initStats()
      #src is always second to last argument
      #then remove user name before @
      stats_dict['source'] = line.split()[-2].split('@')[-1]
    elif "Number of files:" in line:
      stats_dict['numFiles'] = parseline(line)[0]
    elif "Number of regular files transferred:" in line:
      stats_dict['numFilesTx'] = parseline(line)[0]
    elif "Total file size:" in line:
      stats_dict['fileSize'] = parseline(line)[0]
    elif "Total transferred file size:" in line:
      stats_dict['fileSizeTx'] = parseline(line)[0]
    elif "Literal data:" in line:
      stats_dict['litData'] = parseline(line)[0]
    elif "Matched data:" in line:
      stats_dict['matchedData'] = parseline(line)[0]
    elif "File list size:" in line:
      stats_dict['listSize'] = parseline(line)[0]
    elif "File list generation time:" in line:
      stats_dict['listGen'] = parseline(line)[0]
    elif "File list transfer time:" in line:
      stats_dict['listTx'] = parseline(line)[0]
    elif "Total bytes sent:" in line:
      stats_dict['bytesSent'] = parseline(line)[0]
    elif "Total bytes received:" in line:
      stats_dict['bytesRec'] = parseline(line)[0]
    elif "bytes/sec" in line:
      stats_dict['txSpeed'] = parseline(line)[2]
    elif "total size is" in line:
      stats_dict['speedup'] = parseline(line)[1]
      stats.append(stats_dict)

    line = ''

  for idx,val in enumerate(stats):
    # print stats
    print stats[idx]['source'], "\n", \
      "\t files backed-up:", int(stats[idx]['numFiles']), "("+humanize_bytes(stats[idx]['fileSize'],2)+")\n", \
      "\t files updated:", int(stats[idx]['numFilesTx']), "("+humanize_bytes(stats[idx]['fileSizeTx'],2)+")\n", \
      "\t sent/received:", humanize_bytes(stats[idx]['bytesSent'],2), "/", humanize_bytes(stats[idx]['bytesRec'],2),"\n", \
      "\t transfer rate:", humanize_bytes(stats[idx]['txSpeed'],2)+"/sec\n", \
      "\t speedup:", stats[idx]['speedup']

if __name__ == '__main__':
  main()

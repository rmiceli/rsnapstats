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

def stats_dictionary(data):
  """
    Return a dict of all the stats that rsync outputs
  """
  stats_dict = {'source':data[0],'numFiles':data[1],'numFilesTx':data[2], \
      'fileSize':data[3],'fileSizeTx':data[4],'litData':data[5], \
      'matchedData':data[6],'listSize':data[7],'listGen':data[8], \
      'listTx':data[9],'bytesSent':data[10], 'bytesRec':data[11], \
      'txSpeed':data[12],'speedup':data[13]}

  return stats_dict

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

    # sort through line by line. if/elif order matters here
    if "/usr/bin/rsync" in line:
      data = []
      #src is always second to last argument
      #then remove user name before @
      data.append(line.split()[-2].split('@')[-1])
    elif "rsync error" in line or "ERROR" in line:
      print line
    elif "Number of files" in line:
      data.append(parseline(line))
    elif "Number of files transferred" in line:
      data.append(parseline(line))
    elif "Total file size" in line:
      data.append(parseline(line))
    elif "Total transferred file size" in line:
      data.append(parseline(line))
    elif "Literal data" in line:
      data.append(parseline(line))
    elif "Matched data" in line:
      data.append(parseline(line))
    elif "File list size" in line:
      data.append(parseline(line))
    elif "File list generation time" in line:
      data.append(parseline(line))
    elif "File list transfer time" in line:
      data.append(parseline(line))
    elif "bytes/sec" in line:
      data.append(parseline(line))
    elif "Total bytes sent" in line:
      data.append(parseline(line))
    elif "Total bytes received" in line:
      data.append(parseline(line))
    elif "total size is" in line:
      data.append(parseline(line))
      stats.append(stats_dictionary(data))
    line = ''

  for idx,val in enumerate(stats):
    # print stats
    print stats[idx]['source'], "\n", \
      "\t files backed-up:", int(stats[idx]['numFiles'][0]), "("+humanize_bytes(stats[idx]['fileSize'][0],2)+")\n", \
      "\t files updated:", int(stats[idx]['numFilesTx'][0]), "("+humanize_bytes(stats[idx]['fileSizeTx'][0],2)+")\n", \
      "\t sent/received:", humanize_bytes(stats[idx]['bytesSent'][0],2), "/", humanize_bytes(stats[idx]['bytesRec'][0],2),"\n", \
      "\t speedup:", stats[idx]['speedup'][1]

if __name__ == '__main__':
  main()

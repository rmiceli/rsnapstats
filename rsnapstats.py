import sys

def parseline(line,listvar):
  dum = []
  words = line.split()
  for ii in words:
    if ii[0].isdigit():
      dum.append(float(ii))
  return dum

def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.
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

# initialize
numFiles,fileSize,numFilesTx,fileSizeTx, \
  bytesSent,bytesRec,totalSize,source = ([] for i in range(8))
line = ''

# get rsync stats
for tmp in sys.stdin:
  # combine wrapped lines
  if tmp.strip().endswith('\\'):
    line = line + tmp.replace('\\','')
    continue
  else:
    line = line + tmp

  if "Number of files transferred" in line:
    numFilesTx.append(parseline(line,numFilesTx))
  elif "Number of files" in line:
    numFiles.append(parseline(line,numFiles))
  elif "Total file size" in line:
    fileSize.append(parseline(line,fileSize))
  elif "Total transferred file size" in line:
    fileSizeTx.append(parseline(line,fileSizeTx))
  elif "Total bytes sent" in line:
    bytesSent.append(parseline(line,bytesSent))
  elif "Total bytes received" in line:
    bytesRec.append(parseline(line,bytesRec))
  elif "total size is" in line:
    totalSize.append(parseline(line,totalSize))
  elif "/usr/bin/rsync" in line:
    #src is always second to last argument
    #then remove user name before @
    source.append(line.split()[-2].split('@')[-1])
  line = ''

# print stats
for idx,val in enumerate(numFilesTx):
  print source[idx], "\n", \
    "\t files backed-up:", int(numFiles[idx][0]), "("+humanize_bytes(fileSize[idx][0],2)+")\n", \
    "\t files updated:", int(numFilesTx[idx][0]), "("+humanize_bytes(fileSizeTx[idx][0],2)+")\n", \
    "\t sent/received:", humanize_bytes(bytesSent[idx][0],2), "/", humanize_bytes(bytesRec[idx][0],2),"\n", \
    "\t speedup:", totalSize[idx][1]


import subprocess
import shlex
import time
from nbstreamreader import NonBlockingStreamReader as NBSR

cmd = "/home/lotus/leela-zero-0.15/src/leelaz -w /home/lotus/leela-zero-0.15/best-network --gpu 4"
args  = shlex.split(cmd)
p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)

nbsr = NBSR(p.stdout)
colors = 'bw'
while p.poll() is None:
    output = nbsr.readline(3)
    if not output:

        color = colors[0]
        print('No more data')
        # p.stdin.write('genmove black'.encode('utf-8'))
        p.stdin.write(('genmove {}\n'.format(color)).encode('utf-8'))
        p.stdin.flush()
        colors = colors[::-1]

        # p.stdout.flush()
    print(output)

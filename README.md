loremlogsum
===========
Generate mock logdata to stdout or via http get, for a configurable time.
Defaults to sending at a steady per-second rate. If --spike is set, rate
becomes an approximate floor (randomized per second +/- a factor of --variance)
with a 1:variance chance of bursting to --rate * 10 in any given second.

## Usage
```
loremlogsum.py --time=5 --length=200 > testlog
```
Generates 200 character log lines for 5 seconds to the file testlog.

```
$ ./loremlogsum.py --help
usage: loremlogsum.py [-h] [--time seconds] [--length characters]
                      [--rate lines/sec attempted] [--module writer]
                      [--endpoint http://logs.to/here] [--key api_key]
                      [--burst] [--variance 0.2]

Generate test log data

optional arguments:
  -h, --help            show this help message and exit
  --time seconds        time to run in seconds (default 5)
  --length characters   max number of characters per log line (default 120)
  --rate lines/sec attempted
                        max lines/sec to attempt writing (default 8192)
  --module writer       set log sending module [stdout, http] (default stdout
  --endpoint http://logs.to/here
                        where to send logs if module != stdout
  --key api_key         api key, required for network modules
  --burst               randomize base rate around variance, with random
                        bursts to 10 * rate
  --variance 0.2        variance when using --burst, where base log rate will
                        randomly vary between rate * (1-variance) and rate *
                        (1+variance)
```

## Example
```
$ time python loremlogsum.py --time=10 --length=100 --rate=500 --burst --variance=0.26 > out
real    0m10.121s
user    0m1.008s
sys 0m0.036s

$ awk '{print $1}' out | uniq -c
 413 1406994187
 417 1406994188
 556 1406994189
5000 1406994190
 516 1406994191
 545 1406994192
 421 1406994193
 612 1406994194
 545 1406994195
5000 1406994196
```

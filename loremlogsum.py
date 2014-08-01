#!/usr/bin/env python
#

import time
import string
import random
import argparse
import loremlogsum_http
import loremlogsum_stdout

def make_logs(timestamp, size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + ' '):
    return timestamp + ' ' + ''.join(random.choice(chars) for i in range(size))

def main():
    parser = argparse.ArgumentParser(description="Generate test log data")
    parser.add_argument("--time", metavar="seconds", required=False, default=20,
                        type=int, help="time to run in seconds (default 20)")
    parser.add_argument("--length", metavar="characters", default=120,
                        type=int, help="max number of characters per log line (default 120)")
    parser.add_argument("--rate", metavar="lines/sec attempted", default=8192,
                        type=int, help="max lines/sec to attempt writing (default 120)")
    parser.add_argument("--module", metavar="writer", default='stdout',
                        type=str, help="set log sending module i.e. stdout, http")
    parser.add_argument("--endpoint", metavar="http://logs.to/here", type=str,
                        help="where to send logs if module != stdout")
    parser.add_argument("--key", metavar="api_key", type=str,
                        help="api key, required for network (http, etc) mode")
    parser.add_argument("--spike", default=False, action='store_true',
                        help="steady at rate, with bursts")
    args = parser.parse_args()

    variance = 0.2 # TODO: make a param

    if args.module == 'http':
        logger = loremlogsum_http.loremlogsum_http(args.key, args.endpoint)
    elif args.module == 'stdout':
        logger = loremlogsum_stdout.loremlogsum_stdout()

    start = int(time.time())
    now = int(time.time())

    while start + args.time > now:
        throttle = time.time()

        if args.spike:
            if random.choice(range(0, 100)) < 100 * variance:
                rate = args.rate * 10
            else:
                rate = random.choice(range(int(args.rate * (1 - variance)), int(args.rate * (1 + variance))))

        else:
            rate = args.rate
        for i in range(0,rate):
            logger.send(make_logs(str(now), args.length))
        if time.time() < throttle + 1:
            time.sleep(throttle + 1 - time.time())
        now = int(time.time())

if __name__ == "__main__":
    main()

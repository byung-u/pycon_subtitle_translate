#!/usr/bin/env python3.5
import re
import sys
from time import gmtime, strftime

def remove_time(file_name, out_file_name, p):
    fw = open(out_file_name, 'w')
    with open(file_name) as f:
        for line in f:
            m = p.match(line)
            if m is None:
                fw.write(line)
    f.closed
    fw.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s FILE', sys.argv[0], file=sys.stderr)
        sys.exit(2)

    file_name = sys.argv[1]
    out_file_name = '%s.%s' % (file_name, strftime("%Y%m%d%H%M%S", gmtime()))

    # TODO: get option by command line

    # 00:37:24.250--> 00:37:30.160
    time_record = re.compile(r'\d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+\ -\-\>\ \d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+')
    remove_time(file_name, out_file_name, time_record)

    sys.exit(0)

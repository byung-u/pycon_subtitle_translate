#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import argparse
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


def remove_white_space_time(file_name, out_file_name, tr, tr1, tr2, tr3):
    fw = open(out_file_name, 'w')
    with open(file_name) as f:
        for line in f:
            m1 = tr1.match(line)  # 00 : 37 : 24.250 -> 00 : 37 : 30.160
            m2 = tr2.match(line)  # 00 : 37 : 24.250-> 00 : 37 : 30.160
            m3 = tr3.match(line)  # 00 : 37 : 24,250 -> 00 : 37 : 30.160
            if m1 is not None:
                fw.write('\n')
                fw.write(line.replace(' : ', ':').replace('->', '-->'))
            elif m2 is not None:
                fw.write('\n')
                fw.write(line.replace(' : ', ':').replace('->', ' -->'))
            elif m3 is not None:
                fw.write('\n')
                fw.write(line.replace(' : ', ':').replace(',', '.').replace('->', '-->'))
            else:
                fw.write(line)
    f.closed
    fw.close()


def merge_english_lines(file_name, out_file_name, p):
    fw = open(out_file_name, 'w')
    with open(file_name) as f:
        for line in f:
            m = p.match(line)
            if m is None:
                fw.write(line.rstrip('\n'))
                fw.write(' ')
            else:
                fw.write('\n')
                fw.write(line)
    f.closed
    fw.close()


def insert_korean_lines(file1, file2, out_file_name):
    f1 = open(file1, "r")
    f2 = open(file2, "r")

    fw = open(out_file_name, 'w')
# TODO : It will not working.. n.n
    for line in f1:
        fw.write('\n' + line.rstrip() + '\n' + f2.readline().strip())

    f1.close()
    f2.close()
    fw.close()


def main():
    if len(sys.argv) < 2:
        print("\nMUST use f option like, %s -f $file_path" % sys.argv[0])
        sys.exit(2)

    file_name = ""
    out_file_name = ""
    # Make the help output a little less jarring.
    help_factory = (lambda prog: argparse.RawDescriptionHelpFormatter(
        prog=prog, max_help_position=28))

    parser = argparse.ArgumentParser(prog='subtitle_edit',
                                     fromfile_prefix_chars='@',
                                     formatter_class=help_factory)
    parser.add_argument(
            "-f", "--file", metavar='PATH',
            nargs=1, help="[mandatory] file path")
    parser.add_argument(
            "-r", "--remove-time-record",
            help="remove time record in subtitle", action="store_true",
            dest="remove_time_record")
    parser.add_argument(
            "-m", "--merge-en-lines",
            help="merge english subtitle in 1 line", action="store_true",
            dest="merge_en_lines")
    parser.add_argument(
            "-t", "--remove-space-time",
            help="remove any useless white space in time record",
            action="store_true", dest="remove_space_time")
    parser.add_argument(
            "-i", "--inert-ko-lines",
            help="mix en and 1st translate ko subtitle", action="store_true",
            dest="insert_ko_lines")

    # 00:37:24.250 --> 00:37:30.160
    time_record = re.compile(r'\d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+\ -\-\>\ \d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+')

    # 00 : 37 : 24.250 -> 00 : 37 : 30.160
    tr1 = re.compile(r'\d+\d+\ :\ \d+\d+\ :\ \d+\d+\.\d+\d+\d+\ \-\>\ \d+\d+\ :\ \d+\d+\ :\ \d+\d+\.\d+\d+\d+')
    # 00 : 37 : 24.250-> 00 : 37 : 30.160
    tr2 = re.compile(r'\d+\d+\ :\ \d+\d+\ :\ \d+\d+\.\d+\d+\d+\-\>\ \d+\d+\ :\ \d+\d+\ :\ \d+\d+\.\d+\d+\d+')
    # 00 : 28 : 17,740 -> 00 : 28 : 20.559
    tr3 = re.compile(r'\d+\d+\ :\ \d+\d+\ :\ \d+\d+\,\d+\d+\d+\ \-\>\ \d+\d+\ :\ \d+\d+\ :\ \d+\d+\.\d+\d+\d+')

    args = parser.parse_args()
    # print(args)
    if args.file:
        file_name = args.file[0]
        out_file_name = '%s.%s' % (
                file_name, strftime("%Y%m%d%H%M%S", gmtime()))
    else:
        print(args.help)

    if len(file_name) == 0:
        print("Error, MUST need to input file path")
        print(args.help)
        sys.exit(0)

    if args.remove_time_record:
        print("[remove time record]: ", out_file_name)
        out_file_name = '%s.rm_time' % (out_file_name)
        remove_time(file_name, out_file_name, time_record)

    if args.merge_en_lines:
        print("[merge english lines]: ", file_name)
        out_file_name = '%s.merge.txt' % (out_file_name)
        merge_english_lines(file_name, out_file_name, time_record)

    if args.remove_space_time:
        print("[remove useless whitespace]: ", out_file_name)
        out_file_name = '%s.fix_time' % (out_file_name)
        remove_white_space_time(
                file_name, out_file_name, time_record, tr1, tr2, tr3)

    if args.insert_ko_lines:
        print("[insert korean lines]: ", file_name)
        out_file_name = '%s.mix' % (out_file_name)
        insert_korean_lines(file_name, out_file_name)
        # TODO: remove_dup_time

    sys.exit(0)


if __name__ == '__main__':
    main()

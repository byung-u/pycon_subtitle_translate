#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import re
import subprocess
import sys
from googletrans import Translator
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


# def insert_korean_lines(en, ko, output, p):
#     f1 = open(en, "r")
#     f2 = open(ko, "r")
#
#     #fw = open(out_file_name, 'w')
# # TODO : It will not working.. n.n
#     for l1, l2 in f1, f2:
#         m = p.match(line)
#         if m is not None:
#             print('[EN]', l1)
#             print('[KO]', l2)
#         #fw.write('\n' + line.rstrip() + '\n' + f2.readline().strip())
#
#     f1.close()
#     f2.close()
#     #fw.close()
#
def subtitle_translate(file_name, fw, t):
    with open(file_name) as f:
        for idx, line in enumerate(f):
            if idx < 3:
                fw.write(line)
                continue
            line = line.replace('\"', '\'')
            result = t.translate(line, dest='ko')
            print(result.text)
            fw.write(result.text)
            fw.write('\n')
    t = None
    f.closed


def run_split_command(file_name):
    command = 'split -l 500 -a 2 "./%s" "%s_"' % (file_name, file_name)  # by line
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode != 0:
        print('[ERR]', command)
        raise RuntimeError


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
    parser.add_argument("-f", "--file", metavar='PATH', nargs=1,
                        help="[mandatory] file path")
    parser.add_argument("-r", "--remove-time-record",
                        help="remove time record in subtitle",
                        action="store_true", dest="remove_time_record")
    parser.add_argument("-m", "--merge-en-lines",
                        help="merge english subtitle in 1 line",
                        action="store_true", dest="merge_en_lines")
    parser.add_argument('--remove-space-time', action='store_true')
    parser.add_argument('--translate', action='store_true')

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
        out_file_name = '%s.%s' % (file_name,
                                   strftime("%Y%m%d%H%M%S", gmtime()))
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
        remove_white_space_time(file_name, out_file_name, time_record,
                                tr1, tr2, tr3)

    if args.translate:
        file_size = os.path.getsize(file_name)
        out_file_name = '%s.translated' % (out_file_name)
        fw = open(out_file_name, 'w')
        if file_size < 15 * 1024:  # max 15K byte
            subtitle_translate(file_name, fw, Translator())
        else:
            run_split_command(file_name)  # split flie by max limit size
            glob_file_name = './%s_*' % file_name
            entries = glob.glob(glob_file_name)
            for split_file_name in entries:
                t = Translator()
                print(split_file_name)
                subtitle_translate(split_file_name, fw, t)

        fw.close()


if __name__ == '__main__':
    main()

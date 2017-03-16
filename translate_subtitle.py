#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
import subprocess
import sys

from googletrans import Translator


def merge_english_lines(file_name, out_file_name, time_record):
    fw = open(out_file_name, 'w')
    with open(file_name) as f:
        for idx, line in enumerate(f):
            if idx < 3:
                fw.write(line)
                continue
            m = time_record.match(line)
            if m is None:
                fw.write(line.rstrip('\n'))
                fw.write(' ')
            else:
                fw.write('\n')
                fw.write('\n')
                fw.write(line)
    f.closed
    fw.close()


def subtitle_translate(file_name, fw, t):
    with open(file_name) as f:
        for idx, line in enumerate(f):
            if idx < 3:
                fw.write(line)
                continue
            line = line.replace('\"', '\'').replace('à', 'a')
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

    # 00:37:24.250 --> 00:37:30.160
    time_record = re.compile(r'\d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+\ -\-\>\ \d+\d+:\d+\d+:\d+\d+\.\d+\d+\d+')

    all_files = glob.glob('./PyconSubtitle/*')
    for idx, each_file in enumerate(all_files):
        # print('{}[INFO] {}'.format(idx, each_file))
        merged_file = '%s.merge' % (each_file)
        merge_english_lines(each_file, merged_file, time_record)

        file_size = os.path.getsize(merged_file)
        out_file_name = each_file.replace('.en.vtt', '.ko.vtt')
        fw = open(out_file_name, 'w')
        if file_size < 15 * 1024:  # max 15K byte
            subtitle_translate(merged_file, fw, Translator())
        else:
            run_split_command(merged_file)  # split flie by max limit size
            glob_merge_file = '%s_*' % merged_file
            entries = glob.glob(glob_merge_file)
            for split_file in entries:
                t = Translator()
                # print('{}[INFO] {}'.format(idx, split_file))
                subtitle_translate(split_file, fw, t)

        fw.close()


if __name__ == '__main__':
    main()
    sys.exit(0)

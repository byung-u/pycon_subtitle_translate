#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
from unidecode import unidecode
import subprocess
import sys

from googletrans import Translator


def merge_english_lines(file_name, out_file_name, time_record):
    fw = open(out_file_name, 'w')
    with open(file_name) as f:
        for idx, line in enumerate(f):
            if idx < 3:
                line = line.replace('Language: en', 'Language: ko')
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


def subtitle_translate(file_name, time_record, fw, t):
    with open(file_name) as f:
        for idx, line in enumerate(f):
            if idx < 3:
                fw.write(line)
                continue
            m = time_record.match(line)
            if m is not None:
                fw.write(line)
                print(line)
                continue
            line = line.rstrip()
            line = unidecode(line)         # unicode to ascii
            line = line.replace('.', '')   # some dot causes translate error
            line = line.replace(',', '')   # some comma causes translate error
            line = line.replace('\"', '')  # double quot causes translate error
            if (line == 'problem'):  # only 'problem' keyword causes error
                line = line.replace('problem', 'problems')
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
    all_files = glob.glob('./Subtitles/*')
    for idx, each_file in enumerate(all_files):
        #if idx < 4:
        #    continue
        print('{}[INFO] {}'.format(idx, each_file))
        if (each_file.find('.ko.vtt') != -1) or (each_file.find('.vtt.merge') != -1):  # it's already translated.
            continue
        merged_file = '%s.merge' % (each_file)
        merge_english_lines(each_file, merged_file, time_record)

        file_size = os.path.getsize(merged_file)
        out_file_name = each_file.replace('.en.vtt', '.ko.vtt')
        fw = open(out_file_name, 'w')
        if file_size < 15 * 1024:  # max 15K byte
            subtitle_translate(merged_file, time_record, fw, Translator())
        else:
            run_split_command(merged_file)  # split flie by max limit size
            glob_merge_file = '%s_*' % merged_file
            entries = glob.glob(glob_merge_file)
            for split_file in entries:
                print('{}[INFO] {}'.format(idx, split_file))
                subtitle_translate(split_file, time_record, fw, Translator())
        fw.close()


if __name__ == '__main__':
    main()
    sys.exit(0)

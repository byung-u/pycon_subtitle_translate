#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import json
import os
import re
import urllib.request
import subprocess
import sys
import ssl
from unidecode import unidecode
# from googletrans import Translator
from google_trans_new import google_translator


ssl._create_default_https_context = ssl._create_unverified_context


def naver_papago_nmt(subtitle):
    # naver_cid = os.environ.get('NAVER_TRANSLATE_CLIENT_ID')
    # naver_csec = os.environ.get('NAVER_TRANSLATE_CLIENT_SECRET')
    naver_cid = os.environ.get('NAVER_BLOG_CLIENT_ID')
    naver_csec = os.environ.get('NAVER_BLOG_CLIENT_SECRET')
    enc_text = urllib.parse.quote(subtitle)
    data = 'source=en&target=ko&text=' + enc_text
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    request = urllib.request.Request(url)
    print(str(naver_cid))
    print((naver_cid))
    request.add_header('X-Naver-Client-Id', str(naver_cid))
    request.add_header('X-Naver-Client-Secret', str(naver_csec))
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    print(rescode)
    if(rescode == 200):
        response_body = response.read()
        translated = json.loads(response_body.decode('utf-8'))
        return (translated['message']['result']['translatedText'])
    else:
        print('Error Code:' + rescode)
        return ' '


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
            if (line == 'run'):  # only 'run' keyword causes error
                line = line.replace('run', 'runs')
            if (line == 'incentive'):  # only 'incentive' keyword causes error
                line = line.replace('incentive', 'incentives')
            result = t.translate(line, lang_tgt='ko')
            print(result)
            fw.write(result)
            fw.write('\n')
    t = None
    f.closed


def subtitle_translate_papago(file_name, time_record, fw):
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
            if len(line) < 1:
                print(line)
                fw.write("\n")
                continue
            line = unidecode(line)         # unicode to ascii
            line = line.replace('.', '')   # some dot causes translate error
            line = line.replace(',', '')   # some comma causes translate error
            line = line.replace('\"', '')  # double quot causes translate error
            result = naver_papago_nmt(line)
            print(result)
            fw.write(result)
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

    translator = google_translator()
    #all_files = glob.glob('./PyconSubtitle/*')
    all_files = glob.glob('./Subtitles/*')
    for idx, each_file in enumerate(all_files):
        if each_file.find('`'):
            new_each_file = each_file.replace('`', '')
            os.rename(each_file, new_each_file)
            each_file = new_each_file

        print('{}[INFO] {}'.format(idx, each_file))
        if (each_file.find('.ko.vtt') != -1) or (each_file.find('.vtt.merge') != -1):  # it's already translated.
            continue
        merged_file = '%s.merge' % (each_file)
        merge_english_lines(each_file, merged_file, time_record)

        file_size = os.path.getsize(merged_file)
        out_file_name = each_file.replace('.en.vtt', '.ko.vtt')
        fw = open(out_file_name, 'w')
        if file_size < 15 * 1024:  # max 15K byte
            subtitle_translate(merged_file, time_record, fw, translator)
            # subtitle_translate_papago(merged_file, time_record, fw)
        else:
            run_split_command(merged_file)  # split flie by max limit size
            glob_merge_file = '%s_*' % merged_file
            entries = glob.glob(glob_merge_file)
            for split_file in entries:
                print('{}[INFO] {}'.format(idx, split_file))
                subtitle_translate(merged_file, time_record, fw, translator)
                # subtitle_translate_papago(merged_file, time_record, fw)
        fw.close()


if __name__ == '__main__':
    main()
    sys.exit(0)

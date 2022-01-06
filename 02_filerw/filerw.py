#!/usr/bin/env python3
#
# Copyright (C) 2021 alson <tx_danyang@163.com>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import os
import sys
import argparse
import string

def paras_analysis():
    parser = argparse.ArgumentParser(description='read files in binary mode')
    parser.add_argument('-ifile', default='', help='input file name')
    parser.add_argument('-ofile', default='', help='output file name')
    parser.add_argument('-start_address', default=0, help='start address')
    parser.add_argument('-len', default=0, help='length')
    args = parser.parse_args()
    return args

def out_file_generate(in_file_name, out_file_name, start_address, len):
    if not os.path.exists(in_file_name):
        print(f"input file does not exist")
        return False

    if os.path.exists(out_file_name):
        print(f"output file exists")
        return False

    file_size = os.path.getsize(in_file_name)
    if start_address >= file_size:
        print(f"start_address exceeds input file size")
        return False

    if start_address + len >= file_size:
        len = file_size - start_address

    file_read = open(in_file_name, 'rb')
    file_write = open(out_file_name, 'wb')

    file_read.seek(start_address)

    for i in range(0, len):
        byte = file_read.read(1)
        file_write.write(byte)

    file_read.close()
    file_write.close()

    return True

def digit_parameters_convert(parameter):
    if str(parameter).isdigit():
        return int(parameter, 10)
    else:
        return int(parameter[2:], 16)

def digit_parameters_check(digit_parameter):
    if str(digit_parameter).isdigit():
        return True
    elif len(str(digit_parameter)) >= 3 and str(digit_parameter).startswith('0X') and all(c in string.hexdigits for c in str(digit_parameter)[2:]):
        return True
    else:
        return False

if __name__ == '__main__':
    args = paras_analysis()

    in_file_name = str(args.ifile)
    out_file_name = str(args.ofile)
    start_address_str = str(args.start_address).upper()
    len_str = str(args.len).upper()

    if not digit_parameters_check(start_address_str):
        print(f"please enter the correct start_address value")
        sys.exit(-1)

    if not digit_parameters_check(len_str):
        print(f"please enter the correct len value")
        sys.exit(-1)    

    start_address = digit_parameters_convert(start_address_str)
    len = digit_parameters_convert(len_str)

    out_file_generate(in_file_name, out_file_name, start_address, len)

    sys.exit(0)

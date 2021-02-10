import os
import sys
import struct
import random
from enum import Enum

CMD_HELP_PARAM_NUMS = 2
CMD_EXEC_PARAM_NUMS = 4

class CMD(Enum):
    CMD_INVALID = 0
    CMD_HELP = 1
    CMD_EXEC = 2

def help_info_display(help_param_str):
    help_param_str = str(help_param_str)

    if help_param_str != '-help' and help_param_str != '-h':
        print('unknown option:' + help_param_str)
    else:
        print('usage: gbin [-of] [-unit] [-count]')
        print('generate a bin file of the specified size')
        print('')
        print('-of=FILE        output file name')
        print('-unit=UNIT      unit, can only be B or K or M')
        print('-count=COUNT    copy only N input blocks')
        print('')
        print('example: the generated file name is test.bin and the bin file size is 1024 bytes')
        print('python3 gbin.py -of=test.bin -unit=1B -count=1024')

def file_create(cmd_info):
    file = open('./' + cmd_info['file_name'], 'wb')
    file.close()

def file_exists_check(file_name):
    return os.path.exists('./' + file_name)

def file_write(cmd_info):
    file = open('./' + cmd_info['file_name'], 'wb')

    i = 0
    len = cmd_info['unit'] * cmd_info['count']

    while(i < len):
        random_byte = struct.pack('B', random.randint(0, 255))
        file.write(random_byte)
        i = i + 1

    file.close()

def count_get(count_param_str, cmd_info):
    count_param_str = str(count_param_str)

    cmd_str = count_param_str[:count_param_str.find('=')]
    if cmd_str != '-count':
        print('the third parameter is -count=')
        return False

    count_str = count_param_str[count_param_str.find('=') + 1:]
    count = int(count_str)

    cmd_info['count'] = count

    return True

def unit_get(unit_param_str, cmd_info):
    unit_param_str = str(unit_param_str)

    cmd_str = unit_param_str[:unit_param_str.find('=')]
    if cmd_str != '-unit':
        print('the second parameter is -unit=')
        return False

    unit_char = unit_param_str[-1]
    unit_capacity = 0
    if unit_char == 'b' or unit_char == 'B':
        unit_capacity = 1
    elif unit_char == 'k' or unit_char == 'K':
        unit_capacity = 1024
    elif unit_char == 'm' or unit_char == 'M':
        unit_capacity = 1024 * 1024
    else:
        print('capacity unit error, the unit of capacity can only be B or K or M')
        return False

    unit_str = unit_param_str[unit_param_str.find('=') + 1:-1]
    unit_num = int(unit_str)
    unit = unit_num * unit_capacity

    cmd_info['unit'] = unit

    return True

def file_name_get(first_name_param_str, cmd_info):
    first_name_param_str = str(first_name_param_str)

    cmd_str = first_name_param_str[:first_name_param_str.find('=')]
    if cmd_str != '-of':
        print('the first parameter is -of=')
        return False

    file_name_str = first_name_param_str[first_name_param_str.find('=') + 1:]
    cmd_info['file_name'] = file_name_str
    return True
    
def param_nums_check(param_nums):
    if param_nums == CMD_HELP_PARAM_NUMS:
        return CMD.CMD_HELP
    elif param_nums == CMD_EXEC_PARAM_NUMS:
        return CMD.CMD_EXEC
    else:
        return CMD.CMD_INVALID
    
if __name__ == '__main__':
    param_nums = len(sys.argv)

    ret = param_nums_check(param_nums)
    if ret == CMD.CMD_INVALID:
        print('please check the number of enter parameters')
    elif ret == CMD.CMD_EXEC:
        cmd_info = {'file_name' : '', 'unit' : 0, 'count' : 0}

        first_name_param_str = sys.argv[1]
        if file_name_get(first_name_param_str, cmd_info) == True:
            if file_exists_check(cmd_info['file_name']) == True:
                print('file already exists')
                sys.exit(0)
            else:
                file_create(cmd_info)
        else:
            print('output file name resolution failed')
            sys.exit(1)

        unit_param_str = sys.argv[2]
        if unit_get(unit_param_str, cmd_info) == False:
            print('unit resolution failed')
            sys.exit(1)

        count_param_str = sys.argv[3]
        if count_get(count_param_str, cmd_info) == False:
            print('count resolution failed')
            sys.exit(1)

        file_write(cmd_info)
        sys.exit(0)
    else:
        help_param_str = sys.argv[1]
        help_info_display(help_param_str)
        sys.exit(0)
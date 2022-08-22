#!/usr/bin/env python3
#
# Copyright (C) 2021 alson <tx_danyang@163.com>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

from distutils.log import debug
import sys
import os
import getopt
import logging
import requests
import zipfile
import serial
import serial.tools.list_ports
from tqdm import tqdm
from gitdownload import GitDownload

def get_bin_path(file_name):
    file_path = ""

    if not os.path.exists(file_name):
        logging.error(f"no specified file found")
        return file_path

    ret = zipfile.is_zipfile(file_name)
    if not ret:
        logging.error(f"no specified format (zip) found")
        return file_path
    else:
        if not os.path.exists(file_name[0:-4]):
            fz = zipfile.ZipFile(file_name, 'r')
            for file in fz.namelist():
                fz.extract(file, file_name[0:-4])

        for root, dirs, files in os.walk(file_name[0:-4]):
            if root.split('/')[-1] == "factory":
                for file in files:
                    if file.split('.')[-1] == "bin":
                        file_path = os.path.join(root, file)

    return file_path

def get_serial_ports_list():
    serial_ports_dict = {}

    serial_ports_list = list(serial.tools.list_ports.comports())
    index = 0
    if len(serial_ports_list):
        for port_name in list(serial_ports_list):
            serial_ports_dict[index] = port_name[0]
            index += 1

    return serial_ports_dict

def download_firmware(url):
    download = requests.head(url, allow_redirects=True)
    header = download.headers

    file_size = int(header.get('Content-Length'))
    logging.info(f"file_size is {file_size}")

    file_name = (header.get('Content-Disposition')).split('=')[-1]
    logging.info(f"file_name is {file_name}")
    if os.path.exists(file_name):
        logging.info(f"{file_name} already exists")
        return file_name

    pbar = tqdm(desc = "downloaded: ", total=file_size, unit='B', unit_scale=True)
    download = requests.get(url, stream=True)
    downloaded_size = 0
    with open(file_name, "wb") as fb:
        for size in download.iter_content(1024):
            if size:
                fb.write(size)
                downloaded_size += len(size)
                percent = int((downloaded_size / file_size) * 100)
                pbar.update(len(size))
    pbar.close()

    return file_name

if __name__ == '__main__':
    opts,args = getopt.getopt(sys.argv[1:], '-h -d:',['help', 'debug='])

    for arg_name, arg_value in opts:
        if arg_name in ('-d', '--debug'):
            if arg_value in ("debug", "info", "warning", "error", "critical"):
                if arg_value == "debug":
                    logging.basicConfig(level=logging.DEBUG)
                elif arg_value == "info":
                    logging.basicConfig(level=logging.INFO)
                elif arg_value == "warning":
                    logging.basicConfig(level=logging.WARNING)
                elif arg_value == "error":
                    logging.basicConfig(level=logging.ERROR)
                else:
                    logging.basicConfig(level=logging.CRITICAL)
            else:
                logging.error("debug arg must be in {\"debug\", \"info\", \"warning\", \"error\", \"critical\"}")
                sys.exit(-1)
        if arg_name in ('-h', '--help'):
            print(f"usage: download.py [-h][-d {{debug, info, warning, error, critical}}]")
            sys.exit(0)

    # get release information
    # token please refer to you GitHuh account Setting -> Developer settings -> Personal access tokens
    git_download = GitDownload("espressif", "esp-at", "Alson-tang", "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    release_info = git_download.get_release_info()
    if not len(release_info):
        logging.error(f"no release info found")
        sys.exit(-1)
    logging.debug(f"{release_info}")

    # get release version
    release_ver = git_download.get_release_version()
    if len(release_ver):
        for key, value in release_ver.items():
            print(f"{key}: {value}")
        version_index = input("please enter the version index:")
        version = release_ver.get(int(version_index))
    else:
        logging.error(f"no release version found")
        sys.exit(-1)

    # get modules under the specified version
    release_modules = git_download.get_release_modules(version)
    if len(release_modules):
        for key, value in release_modules.items():
            print(f"{key}: {value}")

        module_index = input("please enter the module index: ")
        module = release_modules.get(int(module_index))
    else:
        logging.error(f"no release module found")
        sys.exit(-1)

    # get the firmware download address of the specified version and the specified module
    url = git_download.get_spec_release_module_download_url(version, module)
    logging.info(f"url is {url}")

    download_file_name = download_firmware(url)
    logging.info(f"download file name is {download_file_name}")

    # traverse the directory to find the bin file
    bin_file_path = get_bin_path(download_file_name)
    if bin_file_path == "":
        logging.error(f"no bin file found")
        sys.exit(-1)
    logging.info(f"bin path is {bin_file_path}")

    # get available serial ports
    serial_ports = get_serial_ports_list()
    if len(serial_ports):
        for key, value in serial_ports.items():
            print(f"{key}: {value}")

        serial_port_index = input("please enter the serial port index: ")
        serial_port = serial_ports.get(int(serial_port_index))
    else:
        logging.error(f"no available serial port")
        sys.exit(-1)

    # call esptool.py to download firmware
    if module.split('-')[1] == "C3":
        chip_module = "esp32c3"
    else:
        chip_module = "esp32"

    command = "esptool.py -p {0} -b 921600 --before default_reset --after hard_reset --chip {1} write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x0 {2}".format(serial_port, chip_module, bin_file_path)
    logging.info(f"{command}")
    os.system(command)

    sys.exit(0)
"""github download class"""

import requests
import json
import string
import re

class GitDownload:
    """
    github download class
    """
    pass

    def __init__(self, owner, repository, user_name, token):
        self.owner = owner
        self.repository = repository
        self.rest_url = "https://api.github.com/repos"
        self.separator = "/"
        self.username = user_name
        self.token = token

        self.branch = {}
        self.release_info = {}
        self.release_ver = {}
        self.release_modules = {}
        self.release_module_download_url = {}

        self.session = requests.session()
        self.session.auth = (self.username, self.token)


    def get_branch(self):
        url = self.rest_url + self.separator + self.owner + self.separator + self.repository + self.separator + "branches"
        response = self.session.get(url)
        if response.status_code == 200:
            branch_info = json.loads(response.text)
            branch_num = len(branch_info)
            if branch_num:
                self.branch = {}
                for i in range(0, branch_num):
                    self.branch[i] = branch_info[i].get("name")
        return self.branch


    def get_release_info(self):
        self.release_info.clear()

        url = "{0}/{1}/{2}/releases".format(self.rest_url, self.owner, self.repository)
        response = self.session.get(url)

        status_code = response.status_code
        if status_code == 200:
            # convert JSON data to Python object, here is list
            release_info = json.loads(response.text)

            # get each firmware information corresponding to each release
            release_num = len(release_info)
            if release_num:
                for i in range(0, release_num):
                    firmware_info = re.findall(r'\[ESP.*?zip\)', release_info[i].get("body"))
                    self.release_info[release_info[i].get("name")] = firmware_info
        else:
            print(f"get release info failed, error:{status_code}")

        return self.release_info

    def get_release_version(self):
        self.release_ver.clear()

        # first check self.release_info
        if len(self.release_info):
            index = 0
            for key, value in self.release_info.items():    # key is release version here
                self.release_ver[index] = key
                index = index + 1
        else:
            url = "{0}/{1}/{2}/releases".format(self.rest_url, self.owner, self.repository)
            response = self.session.get(url)

            status_code = response.status_code
            if status_code == 200:
                # convert JSON data to Python list, here is list
                release_info = json.loads(response.text)
                release_num = len(release_info)
                if release_num:
                    for i in range(0, release_num):
                        # each element in the list is a dictionary
                        self.release_ver[i] = release_info[i].get("name")

            else:
                print(f"get release version failed, error:{status_code}")

        return self.release_ver

    def get_release_modules(self, version):
        self.release_modules.clear()

        for release_version in self.release_ver.values():
            if release_version == version:
                release_modules_info = self.release_info.get(version)
  
                # resolves supported modules from a list of specified version information
                # the content of the list are as follows:
                # ['[ESP32-C3-MINI-1_AT_Bin_V2.4.1.0.zip](https://github.com/espressif/esp-at/files/9289473/ESP32-C3-MINI-1_AT_Bin_V2.4.1.0.zip)']
                for i in range(0, len(release_modules_info)):
                    module = re.findall(r'(?<=\[).*?(?=_AT)', release_modules_info[i])
                    self.release_modules[i] = module[0]

        return self.release_modules

    def get_release_module_download_url(self, version):
        self.release_module_download_url.clear()

        for release_version in self.release_ver.values():
            if release_version == version:
                release_modules_info = self.release_info.get(version)

                # resolves supported modules from a list of specified version information
                # the content of the list are as follows:
                # ['[ESP32-C3-MINI-1_AT_Bin_V2.4.1.0.zip](https://github.com/espressif/esp-at/files/9289473/ESP32-C3-MINI-1_AT_Bin_V2.4.1.0.zip)']
                # in the dictionary, the key is module and the value is URL, the content of the dictionary are as follows:
                # {'ESP32-C3-MINI-1': 'https://github.com/espressif/esp-at/files/9289473/ESP32-C3-MINI-1_AT_Bin_V2.4.1.0.zip'}
                for i in range(0, len(release_modules_info)):
                    name = re.findall(r'(?<=\[).*?(?=_AT)', release_modules_info[i])
                    url = re.findall(r'https.*?(?=\))', release_modules_info[i])
                    self.release_module_download_url[name[0]] = url[0]

        return self.release_module_download_url

    def get_spec_release_module_download_url(self, version, module_name):
        self.get_release_module_download_url(version)
        return self.release_module_download_url.get(module_name)


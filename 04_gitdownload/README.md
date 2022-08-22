# INTRODUCTION

This is a simple python script, which used to download the version firmware released by the specified repository. Take the [esp-at](https://github.com/espressif/esp-at) repository under [Espressif](https://github.com/espressif) as an example to demonstrate how to use the GitHub [REST API](https://docs.github.com/en/rest) to download the released firmware.

**NOTE:**

- The script recommends **python3** version.
- The script is only for `ESP32` and `ESP32-C3`, not verified for `ESP8266`
- The script is only available for `Linux`
- The script needs to add [esptool](https://github.com/espressif/esptool) to the environment variables

## Getting Started

- Install python packets.

    ```
    python -r requirements.txt
    ```

- Connect an [Espressif chip](https://www.espressif.com/en/products/devkits) to your computer.

- Replace actual `personal access tokens` (account Setting -> Developer settings -> Personal access tokens) in `download.py` source files.

    ```
    # get release information
    # token please refer to you GitHuh account Setting -> Developer settings -> Personal access tokens
    git_download = GitDownload("espressif", "esp-at", "Alson-tang", "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    ```

- Run `download.py`.

    ```
    python download.py
    ```

## Basic Options

You can use `-d` option to enable different log levels. like `-d info`. You can use `-h` to see the log level.

    ```
    python download.py -d info
    ```

## License

This document and the attached source code are released as Free Software under Apache License Version 2 or later. See the accompanying LICENSE file for a copy.

## Output

1. Enter the version that you want to download: (All versions released by `esp-at` will be listed here. Assuming you enter `0`, the version you want to download is `v2.4.1.0`)

    ```
    0: v2.4.1.0
    1: v2.4.0.0
    2: v2.3.0.0_esp32c3
    3: v2.2.1.0_esp8266
    4: v2.2.0.0_esp32
    5: v2.2.0.0_esp8266
    6: v2.2.0.0_esp32c3
    7: v2.1.0.0_esp32s2
    8: v2.1.0.0_esp8266
    9: v2.1.0.0_esp32
    10: v2.1.0.0-rc2_esp32
    11: v2.1.0.0-rc1_esp8266
    12: v2.1.0.0-rc1_esp32
    13: v2.0.0.0_esp32
    14: v2.0.0.0_esp8266
    15: v1.2.0.0
    16: v1.1.3.0
    17: v1.1.2.0
    18: v1.1.1.0
    19: v1.1.0.0
    20: v1.0.0.0
    21: v0.10.0.0
    please enter the version index:
    ```

2. Enter the module that you want to download: (All modules under the  `v2.4.1.0` will be listed here. This version only corresponds to one module, enter `0` here)

    ```
    0: ESP32-C3-MINI-1
    please enter the module index:
    ```

3. Start to download the corresponding firmware. If the firmware to be downloaded is already in the current directory, skip it.

4. Enter the serial port.

    ```
    0: /dev/ttyS0
    1: /dev/ttyUSB1
    2: /dev/ttyUSB0
    please enter the serial port index:
    ```

5. Start to download the firmware to the device.

    ```
    esptool.py v3.1-dev
    Serial port /dev/ttyUSB0
    Connecting....
    WARNING: This chip doesn't appear to be a ESP32-C3 (chip magic value 0x1b31506f). Probably it is unsupported by this version of esptool.
    Chip is unknown ESP32-C3 (revision 3)
    Features: Wi-Fi
    Crystal is 40MHz
    MAC: 84:f7:03:09:17:f4
    Uploading stub...
    Running stub...
    Stub running...
    Changing baud rate to 921600
    Changed.
    Configuring flash size...
    Auto-detected Flash size: 4MB
    Compressed 4194304 bytes to 878431...
    Writing at 0x000fa2d8... (40 %)
    ```
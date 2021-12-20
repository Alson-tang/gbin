# INTRODUCTION

This is a simple python script, which can generate **a BIN file of a specified size in the current directory**. The most typical application of this script is to test FLASH download.

# Getting Started

The script recommends **python3** version. 

You can run the following command to see the usage of the script

```
python3 gbin.py --h
```

The command needs to specify three parameters:

```
gbin.py [-h] [-of OF] [-unit UNIT] [-count COUNT]
```

If you want to generate a file with a size of 1024 and the file name is test.bin, you can run the following command:

```
python3 gbin.py -of=test.bin -unit=B -count=1024
```

# License

This document and the attached source code are released as Free Software under Apache License Version 2 or later. See the accompanying LICENSE file for a copy.

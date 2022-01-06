# INTRODUCTION

This is a simple python script, which can generate **read the contents of the file in binary mode (specify the start address, specify the read length)**.

# Getting Started

The script recommends **python3** version. 

You can run the following command to see the usage of the script

```
python3 filerw.py --h
```

The command needs to specify three parameters:

```
filerw.py [-h] [-ifile IFILE] [-ofile OFILE] [-start_address START_ADDRESS] [-len LEN]
```

If you want to read 3072 bytes of data at the start address of 0x8000 in the file, you can run the following command:

```
python3 filerw.py -ifile=input.bin -ofile=output.bin -start_address=0x8000 -len=3072
```

# License

This document and the attached source code are released as Free Software under Apache License Version 2 or later. See the accompanying LICENSE file for a copy.

# fivebit
* Fivebit is a Python library for compressing short strings. 
* If only lowercase latin characters are used, it will compress strings by 37.5%, more if a dictionary is used
* English/Dutch dictionary included, additional ones can be created easily

Fivebit can also be executed from the command line to compress files. Compressed files will be created with the '.5b' extension

CLI Usage:
- Compress a bunch of textfiles

./fivebit c *.txt

- Decompress a file

./fivebit e somefile.5b

Module usage:

import fivebit
a = fivebit.compress("Your string to be compressed")
print(fivebit.decompress(a))

# acasearch
usage: gen_readme.py [-h] {conferences,authors} ...

positional arguments:
  {conferences,authors}

optional arguments:
  -h, --help            show this help message and exit

## acasearch authors
usage: gen_readme.py [-h] [-o OUTPUT]
                     [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     authors_file

positional arguments:
  authors_file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}

## acasearch conferences
usage: gen_readme.py [-h] {search,get} ...

positional arguments:
  {search,get}

optional arguments:
  -h, --help    show this help message and exit

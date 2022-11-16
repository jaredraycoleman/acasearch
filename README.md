# CoSeTo
Conference Search Tool (CoSeTo) is a command-line tool for searching academic venues and authors

## Installation
```bash
pip install -e ./coseto # -e flag is optional - it installs the package in editable mode
```

## Usage
```bash
coseto --help
```
## Examples
```bash
# search for conferences which have either blockchain or distributed ledger and either iot or internet of things in their call-for-papers
coseto conferences search --upcoming "blockchain,distributed ledger;iot" > report.txt

# get information on a specific conference
coseto conferences get ISAAC

# get author publication venues
coseto authors ./examples/authors_input.yml -o ./examples/authors_output.yml
```
## CLI Documentation
### coseto
usage: coseto [-h] {conferences,authors} ...

positional arguments:
  {conferences,authors}

optional arguments:
  -h, --help            show this help message and exit

#### coseto conferences
usage: coseto conferences [-h] {search,get} ...

positional arguments:
  {search,get}

optional arguments:
  -h, --help    show this help message and exit

##### coseto conferences search
usage: coseto conferences search [-h] [--upcoming] [query]

positional arguments:
  query       Semi-colon seperated AND clauses of comma-seperated OR keywords

optional arguments:
  -h, --help  show this help message and exit
  --upcoming  If set, sort by upcoming deadline before ranking

##### coseto conferences get
usage: coseto conferences get [-h] CONFERENCE ABBREVIATION [ATTRIBUTE]

positional arguments:
  CONFERENCE ABBREVIATION
                        Conference to get data for - one of: [ISAAC, CoopIS,
                        AAMAS, DARS, PODC, ICDCS, SIROCCO, WALCOM, ICDCN,
                        ICALP, LATIN, ALGOSENSORS, CIAC, SOFSEM, FUN, WAOA,
                        SPAA, DCOSS, ITSC, IROS, MASS, SENSYS, MSWIM, CDC,
                        ADHOC-NOW, PERCOM, ICBC, COMSNETS, ICCCN, PAAMS,
                        MOBIQUITOUS, NDSS, BLOCKCHAIN, ESORICS, BLOCKSYS,
                        HPCC, IOTDI, IPDPS, EUROPAR, INFOCOM, FAB, SECON,
                        GLOBECOM, IPSN, HSCC, RTAS, ICCPS, PRIMA, CLUSTER,
                        ICCS, OPODIS, DISC, ICARA, AAAI, GAMESEC, COMPASS,
                        ICLR, AINA, UAI, COCOA, WG, MFCS, ESA, WOWMOM,
                        MOBICOM, SRDS, ICPADS, MOBIHOC, IJCAI, STACS, TAMC,
                        ICTCS, SMC, RSS, STOC, CONCUR, SAGT, IWOCA, ISNCC,
                        CCECE, IWCMC, ASONAM, FCT, FOCS, WADS, SWAT, SIGCOMM,
                        IPCO, ITCS, PDPTA, CONTROLO, SSS, NEURIPS, RTSS, SODA,
                        SoCG, CCCG, ICEBE, MOBISYS, ANTS, ICC, CIKM, ROBIO,
                        ICWSM/A, ICWSM/B, ICWSM/C, eScience, AISI, AICCSA,
                        BDIoT, ISCC, HPCS, ICBTA, DAIS, ICICT, COCOON,
                        COORDINATION, FORTE, ICORES, ICCI, ICSOFT, ICBDA,
                        BIGDATA, CRYPTO, EUROCRYPT, ICASSP, INTERSPEECH, ICIP,
                        ICRA, IGARSS, ISIT, BRAIN]
  ATTRIBUTE             Conference attribute to get - one of: [conference,
                        h5_index, core_rank, era_rank, qualis_rank,
                        last_deadline, name, topics, None]

optional arguments:
  -h, --help            show this help message and exit

#### coseto authors
usage: coseto authors [-h] [-o OUTPUT]
                             [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                             authors_file

positional arguments:
  authors_file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}

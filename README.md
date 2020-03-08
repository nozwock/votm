# VOTM: Voting Manager
---------
####
[![version](https://img.shields.io/github/release/sgrkmr/votm.svg?style=flat-square)](https://GitHub.com/sgrkmr/votm/releases/)
[![downloads](https://img.shields.io/github/downloads/sgrkmr/votm/total.svg?style=flat-square)](https://GitHub.com/sgrkmr/votm/releases/)
![commit](https://img.shields.io/github/last-commit/sgrkmr/votm?style=flat-square)
[![contributors](https://img.shields.io/github/contributors/sgrkmr/votm.svg?style=flat-square)](https://GitHub.com/sgrkmr/votm/graphs/contributors/)
![license](https://img.shields.io/github/license/sgrkmr/votm.svg?style=flat-square)

<img align="left" src="/res/logo.png" width="40"/>
VOTM is a full-featured voting manager desktop app which is also my first project, originally developed to automate the labrous procedure of voting which happens once a year in schools for some specific posts which are appointed to those students with most votes in their respective posts, earlier this was done through ballot box system which tooks a lot of time and work to yield results contrary to what votm can provide.

# Screenshots
<img src="/scrn_a.png" width="100%" />
<img src="/scrn_b.png" width="100%" />

## Download
You can manually download the latest release [here](https://github.com/sgrkmr/votm/releases).</br>
**Note:** binaries are only available for the Windows platform.

## Dependencies
Modules:
  * tabulate
  * pycrypto
  * tkinter
  * xlsxwriter
  * sqlite3
  
## Development
 * Clone the repo, and checkout to `./votm`
 ```sh
 $ git clone https://github.com/sgrkmr/votm.git
 $ cd votm
 ```
 * Install dependencies.
 ```sh
 $ pip install -r requirements.txt
 ```
 **Note:** run `votm_edt.py` to configure the voting session for the first time and run `votm_vte.py` for voting.

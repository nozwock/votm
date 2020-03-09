<p align="center"><img src="https://user-images.githubusercontent.com/57829219/76256135-6d241b80-6275-11ea-96dc-f512f4a0c91a.png")</p>
<p align="center">
 <a href="https://GitHub.com/sgrkmr/votm/releases/", alt="version">
  <img src="https://img.shields.io/github/release/sgrkmr/votm.svg?style=flat-square&color=blueviolet", alt="version"></a>
 <a href="https://GitHub.com/sgrkmr/votm/releases/", alt="downloads"><img src="https://img.shields.io/github/downloads/sgrkmr/votm/total.svg?style=flat-square", alt="downloads"></a>
 <a href="https://github.com/sgrkmr/votm/commits/master", alt="commit"><img src="https://img.shields.io/github/last-commit/sgrkmr/votm?style=flat-square", alt="commit"></a>
 <img src="https://img.shields.io/badge/Python-3.7-blue?style=flat-square", alt="python3">
 <a href="https://GitHub.com/sgrkmr/votm/graphs/contributors/", alt="contributors"><img src="https://img.shields.io/github/contributors/sgrkmr/votm.svg?style=flat-square", alt="contributors"></a>
 <img src="https://img.shields.io/github/license/sgrkmr/votm.svg?style=flat-square", alt="license">
</p>

VOTM is a full-featured voting manager desktop app which is also my first project, It's developed to automate the labrous procedure of voting which happens once a year in schools for some specific posts which are appointed to those students with most votes in their respective posts, earlier this was done through ballot box system which tooks a lot of time and work to yield results contrary to what votm can provide.

# Screenshots
![scrn_a](https://user-images.githubusercontent.com/57829219/76254956-57155b80-6273-11ea-82ec-984872c89c4a.png)
![scrn_b](https://user-images.githubusercontent.com/57829219/76254969-5f6d9680-6273-11ea-9eb9-6dee2628f1f0.png)

## Download
You can manually download the latest release [here](https://github.com/sgrkmr/votm/releases).</br>
>**Note:** binaries are only available for the Windows platform.

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
 >**Note:** run `votm_edt.py` to configure the voting session for the first time and run `votm_vte.py` for voting.
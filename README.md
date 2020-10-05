<p align="center">
    <a href="https://github.com/sgrkmr/votm", alt="votm">
        <img src="https://user-images.githubusercontent.com/57829219/76256135-6d241b80-6275-11ea-96dc-f512f4a0c91a.png", alt="votm">
    </a>
</p>
<p align="center">
    <a href="https://GitHub.com/sgrkmr/votm/releases/", alt="version">
        <img src="https://img.shields.io/github/release/sgrkmr/votm.svg?style=flat-square&color=blueviolet", alt="version">
    </a>
    <a href="https://GitHub.com/sgrkmr/votm/releases/", alt="downloads">
        <img src="https://img.shields.io/github/downloads/sgrkmr/votm/total.svg?style=flat-square", alt="downloads">
    </a>
    <a href="https://github.com/sgrkmr/votm/commits/master", alt="commit">
        <img src="https://img.shields.io/github/last-commit/sgrkmr/votm?style=flat-square", alt="commit">
    </a>
    <a href="https://www.python.org/downloads/release/python-374/", alt="python3">
        <img src="https://img.shields.io/badge/Python-3.7-blue?style=flat-square", alt="python3">
    </a>
    <a href="https://GitHub.com/sgrkmr/votm/graphs/contributors/", alt="contributors">
        <img src="https://img.shields.io/github/contributors/sgrkmr/votm.svg?style=flat-square", alt="contributors">
    </a>
    <a href="https://opensource.org/licenses/GPL-3.0", alt="license">
        <img src="https://img.shields.io/github/license/sgrkmr/votm.svg?style=flat-square", alt="license">
    </a>
</p>

<p align="center">
    <b><code>VOTM</code> is a full-featured voting manager desktop app for school use</b><br/>
    <sub>
        It also happens to be my first project to ever work on, It's developed to automate the laborious procedure of voting which happens once every year in schools (at least in my school) for some specific posts (for eg. let's say for selection of Student Council, HeadBoy/Girl, etc.) which are appointed to those students with the most votes attained in the respective posts they're competing for, earlier this was used to be done through the ballot box system which used to take a lot of time and effort of the school staff to yield the results which would normally take weeks, contrary to what <code>VOTM</code> or automation can offer with ease.
    </sub>
</p>
<p align="center">
    <a href="https://github.com/sgrkmr/votm/issues/new/choose">Report Bug</a> · <a href="https://github.com/sgrkmr/votm/issues/new/choose">Request Feature</a>
</p>
<p align="center">
    <sub>
        <code>Sorry for the terrible grammer, I guess?</code>
    </sub>
</p>

# Screenshots
![scrn_a](https://user-images.githubusercontent.com/57829219/76254956-57155b80-6273-11ea-82ec-984872c89c4a.png)
![scrn_b](https://user-images.githubusercontent.com/57829219/76254969-5f6d9680-6273-11ea-9eb9-6dee2628f1f0.png)

## Download
You can manually download the latest release here: <kbd><a href="https://github.com/sgrkmr/votm/releases">Download</a></kbd></br>
>**NOTE:** `bins` are only available for the `windows` platform.

## Prerequisites
* Packages:
    * tabulate`>=0.8.3`
    * pycrypt`>=2.6.1`
    * xlsxwriter`>=1.2.1`
  
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
 >**NOTE:** run `app-manage.py` to configure the voting session for the first time and run `app-vote.py` for voting.

## License
Licensed under [GPLv3+](https://opensource.org/licenses/GPL-3.0).

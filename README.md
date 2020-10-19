<p align="center">
<a href="https://github.com/sgrkmr/votm"><img alt="votm" src="https://user-images.githubusercontent.com/57829219/76256135-6d241b80-6275-11ea-96dc-f512f4a0c91a.png"></a>
</p>

<p align="center">
<a href="https://GitHub.com/sgrkmr/votm/releases/"><img alt="Version" src="https://img.shields.io/github/release/sgrkmr/votm.svg?style=flat-square&color=blueviolet"></a>
<a href="https://GitHub.com/sgrkmr/votm/releases/"><img alt="Downloads" src="https://img.shields.io/github/downloads/sgrkmr/votm/total.svg?style=flat-square"></a>
<a href="https://github.com/sgrkmr/votm/commits/master"><img alt="Commits" src="https://img.shields.io/github/last-commit/sgrkmr/votm?style=flat-square"></a>
<a href="https://www.python.org/downloads/release/python-373/"><img alt="python3" src="https://img.shields.io/badge/Python-3.7.3-blue?style=flat-square"></a>
<!--<a href="https://GitHub.com/sgrkmr/votm/graphs/contributors/"><img alt="Contributors" src="https://img.shields.io/github/contributors/sgrkmr/votm.svg?style=flat-square"></a>-->
<a href="https://opensource.org/licenses/GPL-3.0"><img alt="License: GPL-3.0" src="https://img.shields.io/github/license/sgrkmr/votm.svg?style=flat-square"></a>
<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>
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
<sub><code>Sorry for the terrible grammer, I guess?</code></sub>
</p>

---

# Preview

![scrn_a](https://user-images.githubusercontent.com/57829219/76254956-57155b80-6273-11ea-82ec-984872c89c4a.png)
![scrn_b](https://user-images.githubusercontent.com/57829219/76254969-5f6d9680-6273-11ea-9eb9-6dee2628f1f0.png)

## Download


| Platform | Version | Download |
| :-: | :-: | :-: |
| Windows_x86 | `1.3.2` | <kbd><a href="https://github.com/sgrkmr/votm/releases/download/1.3.2/votm_x86_32_1.3.2.exe">Download</a></kbd></br> |

## Development

- Clone the repo, and checkout to `./votm`:

```console
$ git clone https://github.com/sgrkmr/votm.git
$ cd votm
```

- To install dependencies, use:

```console
$ pip install -r requirements.txt
```

### Usage

#### Configuration

Run `manage.py` for configuration (such as Candidate Names, Tokens generation, etc.), using:

`python -m votm.manage` **or** `python manage.py`

#### Voting

Now, you may run `vote.py` to start voting, using:

`python -m votm.vote` **or** `python vote.py`

## License

Licensed under [GPLv3+](https://opensource.org/licenses/GPL-3.0).

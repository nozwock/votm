<img src="https://user-images.githubusercontent.com/57829219/154505391-b8b8d7d4-7e0a-4e80-a5bf-87f91b90cd24.png" align="left" height="107px" hspace="0px" vspace="20px">

# VOTM

**A full-featured Voting Manager**, Desktop App for School use.

<!--
<p align="center">
<a href="https://github.com/sgrkmr/votm"><img alt="votm" src="https://user-images.githubusercontent.com/57829219/76256135-6d241b80-6275-11ea-96dc-f512f4a0c91a.png"></a>
</p>
-->

<!--<p align="center">-->
![Maintenance](https://img.shields.io/maintenance/no/2021.svg?color=red&style=flat-square)
[![Version](https://img.shields.io/github/v/tag/sgrkmr/votm.svg?label=version&style=flat-square&color=blueviolet)](https://GitHub.com/sgrkmr/votm/releases/)
[![Downloads](https://img.shields.io/github/downloads/sgrkmr/votm/total.svg?style=flat-square)](https://GitHub.com/sgrkmr/votm/releases/)
<img alt="python3" src="https://img.shields.io/badge/Python-3.7 | 3.10-blue?style=flat-square">
<!--<a href="https://github.com/sgrkmr/votm/commits/master"><img alt="Commits" src="https://img.shields.io/github/last-commit/sgrkmr/votm?style=flat-square"></a>-->
<!--<a href="https://GitHub.com/sgrkmr/votm/graphs/contributors/"><img alt="Contributors" src="https://img.shields.io/github/contributors/sgrkmr/votm.svg?style=flat-square"></a>-->
<!--<a href="https://opensource.org/licenses/GPL-3.0"><img alt="License: GPL-3.0" src="https://img.shields.io/github/license/sgrkmr/votm.svg?style=flat-square"></a>-->
<!--<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>-->
<!--</p>-->

<p align="center">
It was developed to automate the laborious procedure of voting which happens once every year in schools (at least in my school) for some posts (for eg. let's say for selection of Student Council, Head-boy/girl, etc.), earlier this was used to be done through the ballot box system which used to take a lot of time and effort of the school staff to yield the results which would normally take weeks, contrary to what <i>VOTM</i> or automation can offer with ease. It also happens to be my first project to ever work on, so yay! 🎉.
</p>

<p align="center">
<a href="https://github.com/sgrkmr/votm/issues/new/choose">Report Bug</a> · <a href="https://github.com/sgrkmr/votm/issues/new/choose">Request Feature</a>
</p>

<p align="center">
<sub><code>Sorry for the terrible grammer, I guess?</code></sub>
</p>

---


## 🖼️ Preview

![scrn_a](https://user-images.githubusercontent.com/57829219/76254956-57155b80-6273-11ea-82ec-984872c89c4a.png)
![scrn_b](https://user-images.githubusercontent.com/57829219/76254969-5f6d9680-6273-11ea-9eb9-6dee2628f1f0.png)


## 😕 It Doesn't Work
There are many possibilities on why it may not be working. You may not have the runtime requirements mentioned below installed (if you're doing it from source). Other than that some known reasons for issues you might've encountered might be:
- due to incompatibility between the dependencies & python version.
- due to incompatibile version of python; This has been tested only on Python 3.7 & 3.10


## 📥 Download Binaries

⚠️ **Not recommended; Outdated binary** ⚠️

| Platform | Version | Download |
| :-: | :-: | :-: |
| Windows_x86 | `1.3.2` | <kbd><a href="https://github.com/sgrkmr/votm/releases/download/1.3.2/votm_x86_32_1.3.2.exe">Download</a></kbd></br> |


## 📚 Usage

### ⚙️ Configuration

Run the `manage` app for configuration (such as Candidate Names, Tokens generation, etc).

or run `manage.py`, via:

`python -m votm.manage` **or** `python manage.py`

### 📄 Voting

Now, you may run the `vote` app to start voting.

or run `vote.py`, via:

`python -m votm.vote` **or** `python vote.py`


## 🏗️ Get it from Source

1. Clone the repository, and checkout to `./votm`:

```sh
git clone https://github.com/nozwock/votm.git
cd votm
```

### 📋 Runtime Requirements

2. To setup a virtual environment, do:
```sh
python -m venv venv
source venv/Scripts/activate
```

**Note:** It's `venv/bin/activate` on Linux/MacOS

3. To install prerequisites, do:

```sh
pip install .
```

**Or** you could just use `poetry` instead via:

```sh
poetry install
```

**Note:** ⚠️ ~~Dependency management with `poetry` seems to have issues~~(fixed)


## License

Licensed under [GPLv3+](https://opensource.org/licenses/GPL-3.0).

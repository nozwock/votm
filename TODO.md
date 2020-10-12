# *votm* What's Next?

### Structural changes:

```text
votm
├── __init__.py
├── assets
├── core
│   ├── __init__.py
│   ├── _config.py
│   ├── db.py
│   └── ui.py
├── locations.py
├── manage.py
├── utils
│   ├── __init__.py
│   ├── extras.py
│   └── helpers.py
└── vote.py
```

- [X] `refactor:` <kbd>1.1.0</kbd>
  - **changes:**
    - split relevant part of `model.py` to -> `_config.py`, `utils/helpers.py`
    - `etc.py` ->` votm/__init__.py`
    - `tools.py` & `model.py` -> `extras.py`

### Todo

- [X] move `wrt` method for config from `vtom/manage.py` -> `config/_config.py`
- [X] `fix:` cleanup string related issues in `db.py` <kbd>~~1.1.2~~</kbd>
- [ ] ~~move on to `cryptography`~~ <kbd>~~1.3.0~~</kbd>
- [ ] `feat:` remove encryption, instead just hash the password in the config file and encode merge files with base64 to avoid causal tempering and make data less obvious <kbd>1.2.0</kbd>
  - [ ] which in turn means depreciation of `Reg` as password will no more be stored in an enviroment variable, so remove `Reg` too
  - [ ] handle **config and merge files** read/write code accordingly after removing encryption system. Also maybe use toml or other config format for merge files too.
- [ ] `feat:` make config interface better with toml `config.toml` (all config in a single toml file, password too) <kbd>1.3.0</kbd>
- [ ] add these features: <kbd>1.4.0</kbd>
  - [ ] a `combobox` for selection of the database in which the data of the voting session will be stored, at the start screen. Maybe a dialog box to type a custom name for the database too?
  - [ ] make `token` & `password` system optional by adding checkbox's maybe? Might as well put all the password management into a new  popup window?
- [ ] support for linux <kbd>1.5.0</kbd>
  - [ ] path related issues
  - [ ] `.ico` (icon) issue
  - [ ] removal of windows sepcific `Reg`
  - [ ] handle some winapi stuff
- [ ] use abstract class in `manage.py` for result frame

<!--common.py-->

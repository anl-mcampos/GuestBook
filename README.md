# GuestBook Pro

### Requirements
  - python
  - pip

### How to Use
```sh
$ pip install guestbook-pro
$ guestbook-pro
```

### Updating Packages
```sh
  (.venv)$ virtualenv --clear .venv
  (.venv)$ pip install -r requirements.txt
```

### Uploading PyPI
```sh
  $ python setup.py register
  $ python setup.py sdist upload
```

### Alias
```sh
  $ python setup.py alias release register sdist upload
  $ python setup.py release # uploading with just one arg!
```

### Version
1.0.0

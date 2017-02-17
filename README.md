imdea-control-python
====================

 [![license](https://img.shields.io/github/license/scmanjarrez/imdea-control-python.svg)](https://travis-ci.org/scmanjarrez/imdea-control-python(LICENSE.md)


Status Travis CI
----------------
| Branch | Status |
| :-: | :-: |
| `master` | [![Travis branch](https://travis-ci.org/scmanjarrez/imdea-control-python.svg?branch=master)](https://travis-ci.org/scmanjarrez/imdea-control-python) |
| `dev` | [![Travis branch](https://travis-ci.org/scmanjarrez/imdea-control-python.svg?branch=dev)](https://travis-ci.org/scmanjarrez/imdea-control-python) |



A script to control the room blinds, temperature, lights and door at the [IMDEA Software Institute].


Dependencies
------------
You do not worry about this, only run `install.sh` script.

* Python 2.7
  * See [requeriments.txt]
* An account and office at the [IMDEA Software Institute].


Installation
------------
1. Clone the project.
```shell
$ git clone https://travis-ci.org/scmanjarrez/imdea-control-python
```
1. Change to the folder.
```shell
$ cd imdea-control-python
```
1. Give execute permission to `install.sh`.
```shell
$ chmod +x install.sh
```
1. Run install script.
  * Install python, pip, and [requeriments.txt]
  * This will create an alias in `~/.aliases` to run the script in any location.
```shell
$ ./install.sh
```
1. Create the configuration file, `.credentials` from template.
```shell
$ cp .credentials.template .credentials
```
1. Edit the `.credentials` with your IMDEA Software information.
```
username: USERNAME
password: PASSWORD
room_no: ROOM
```


Authors
-------

* [Sergio]()
* [Sergio Valverde](https://github.com/svg153)


License
-------
[![license](https://img.shields.io/github/license/scmanjarrez/imdea-control-python.svg)](https://travis-ci.org/scmanjarrez/imdea-control-python(LICENSE.md)


Credits
-------
* [Michael Emmi](https://github.com/michael-emmi) for his [imdea-controls script].
* [Sergio Valverde](https://github.com/svg153) for [improving](https://github.com/svg153/imdea-controls) the Michael Emmi [imdea-controls script].


[IMDEA Software Institute]:http://www.software.imdea.org
[imdea-control-python]:https://github.com/scmanjarrez/imdea-control-python
[imdea-controls script]:https://github.com/michael-emmi/imdea-controls
[requeriments.txt]:https://github.com/scmanjarrez/imdea-control-python

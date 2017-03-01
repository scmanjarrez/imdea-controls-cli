imdea-controls-cli [![Release]](https://github.com/scmanjarrez/imdea-controls-cli/releases/tag/1.0)
====================
[![License]](LICENSE)

A script to control the room blinds, temperature, lights and door at the [IMDEA Software Institute].

Status Travis CI
----------------
| Branch | Status |
| :-: | :-: |
| [`master`] | [![Travis branch master]](https://travis-ci.org/scmanjarrez/imdea-controls-cli) |
| [`dev`] | [![Travis branch dev]](https://travis-ci.org/scmanjarrez/imdea-controls-cli) |


Dependencies
------------
You do not have to worry about this, only run [`install.sh`] script.

* Python 2.7
  * See [requeriments.txt]
* An account and office at the [IMDEA Software Institute].


Installation
------------

1. Clone the project.

   ```shell
   $ git clone https://github.com/scmanjarrez/imdea-controls-cli.git
   ```

2. Change to the folder.

   ```shell
   $ cd imdea-controls-cli
   ```

3. Give execute permission to install script, [`install.sh`].

   ```shell
   $ chmod +x install.sh
   ```

4. Run install script.
  * Install python, pip, and [requeriments.txt]
  * This will create an alias in `~/.aliases` to run the python script at any location.

  ```shell
  $ ./install.sh
  ```

5. Create the configuration file, `.credentials` from template, [`.credentials.template`].

   ```shell
   $ cp .credentials.template .credentials
   ```

6. Edit the `.credentials` with your [IMDEA Software Institute] information.

   ```
   [credentials]
   user = Your_IMDEA-Software_User
   pass = Your_IMDEA-Software_Pass
   room = Your_IMDEA-Software_Room_to_modify
   ```

7. Change permissions to file:
    ```
    $ chmod 600 .credentials
    ```


Authors
-------

* [Sergio Chica](https://github.com/scmanjarrez)
* [Sergio Valverde](https://github.com/svg153)


Licensing
---------
[![License]](LICENSE)

[imdea-controls-cli] is licensed under Apache 2.0. See [LICENSE](LICENSE) for the full license text.




Credits
-------
* [Michael Emmi](https://github.com/michael-emmi) for his [imdea-controls script].
* [Sergio Valverde](https://github.com/svg153) for [improving](https://github.com/svg153/imdea-controls) the Michael Emmi [imdea-controls script].


Contributing
------------
See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for more info.





[IMDEA Software Institute]:http://www.software.imdea.org (http://www.software.imdea.org)
[imdea-controls-cli]:https://github.com/scmanjarrez/imdea-controls-cli
[imdea-controls script]:https://github.com/michael-emmi/imdea-controls (original imdea-controls)
[requeriments.txt]:requeriments.txt
[License]:https://img.shields.io/badge/License-Apache%202.0-blue.svg (LICENSE)
[Release]:https://img.shields.io/github/release/scmanjarrez/imdea-controls-cli.svg
[`master`]:https://github.com/scmanjarrez/imdea-controls-cli (Branch master)
[`dev`]:https://github.com/scmanjarrez/imdea-controls-cli/tree/dev (Branch dev)
[`install.sh`]:install.sh (installation script)
[`.credentials.template`]:.credentials.template (.credentials template file)
[Travis branch master]:https://travis-ci.org/scmanjarrez/imdea-controls-cli.svg?branch=master (Travis branch master)
[Travis branch dev]:https://travis-ci.org/scmanjarrez/imdea-controls-cli.svg?branch=dev (Travis branch dev)

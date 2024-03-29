# nginx-lm

nginx-lm is command line app written in python that helps you publish and manage apps with nginx, focusing on publishing them _locally_.

In a nutshell, it is a tool to generate nginx config files for you, specially for internal personal projects.

# why

Because writing config files is a repetitive task, so we should automate it.

# how

nginx-lm works on "templates". your project structure should follow that template, and nginx-lm will generate a corresponding nginx config, put it at the appropriate location and reload nginx. quite simple.

for a list of built-in templates, see the app/src/templates directory, and their README files.

# customizing

You can write your own templates for nginx-lm and put them in the `/templates` directory of the source and re-install. Soon, nginx-lm will provide a way to dynamically install custom templates from the CLI.

# installation

Please make sure you have `python3-setuptools` and `unzip` installed. If you get an error stating `ImportError`, then you need to install `python3-setuptools`. If an error saying `unzip: Command not found`, then please install `unzip`. After that, run:

```
curl https://raw.githubusercontent.com/awalGarg/nginx-lm/master/install.sh | sudo bash
```

This will install the package, and make the `nlm` binary available globally.

# usage

```
nlm --help
```
Example: [![asciicast](https://asciinema.org/a/27698.png)](https://asciinema.org/a/27698)

Note: nginx-lm requires root access for most of the commands since it has to write config files to `/etc/nginx/` etc. and issue commands like `service nginx reload` which are restricted to the super user.

# requirements

i don't know the lowest requirements, but I do have *suggested* requirements. having them will ensure that nginx-lm works as described.

- python 3.4.0
- nginx 1.9.5
- any recent Linux distribution, I have only tested on Ubuntu 14.04 though

Windows and OSX are not supported. nginx-lm might or might not work with them, nobody cares.

root access is required for stuff like writing config files, issuing `service nginx reload` etc.

**Note**:

nginx-lm currently assumes that in the directory where nginx config is stored, there exists either a single `conf.d` directory meant to be holding config files with the `.conf` extension referenced in the `nginx.conf` file, OR a `sites-available` and `sites-enabled` directory with `nginx.conf` including all files from `sites-enabled` with whatever extension.

One of these is the default directory structure verified on the following distros:

 - Mint
 - Debian
 - Ubuntu
 - openSUSE
 - Fedora
 - CentOS

Please do not change that structure, it can break nginx-lm.

**Arch Linux users**:

Arch's default nginx config provides only a barebones config structure, and you must manually execute the instructions provided at [the official Arch wiki](https://wiki.archlinux.org/index.php/Nginx#Managing_server_entries), replacing `servers` with `sites` in the directory names.

# stability status

pretty stable. need to write a heck ton of more templates to increase usability, that shall be easy. or so I hope.
should be done soon

and to the python programmers who like to dwell on the source and hack their way around, tis my humble request to treat me with leniency. I have tried to comply with the shitty PEP-8, but lemme know in the issues if I committed any sins anywhere.

# license

WTFPL

# author

Awal Garg aka Rash (awalgarg@gmail.com)

# project structure

TBD

# working

TBD

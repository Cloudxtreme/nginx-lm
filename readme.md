# nginx-lm

nginx-lm is command line app written in python that helps you publish and manage apps with nginx, focusing on publishing them _locally_.

in a nutshell, it is a tool to generate nginx config files for you, specially for internal personal projects.

# why

writing config files is a repetitive task, so we should automate it. because i say so.

# how

nginx-lm works on "templates". your project structure should follow that template, and nginx-lm will generate a corresponding nginx config, put it at the appropriate location and reload nginx. quite simple.

for a list of built-in templates, see the app/src/templates directory, and their README files.

# stuff

- you can write your own templates

# usage

TBD. for now, see `--help`'s output

# installation

TBD

# requirements

i don't know the lowest requirements, but I do have *suggested* requirements. having them will ensure that nginx-lm works as described.

- python 3.4.0
- nginx 1.9.5
- any recent Linux distribution, I have only tested on Ubuntu 14.04 though

Windows and OSX are not supported. nginx-lm might or might not work with them, nobody cares.

root access is required for stuff like writing config files, issuing `service nginx reload` etc.

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

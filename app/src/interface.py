from argparse import ArgumentParser
import os


CWD = os.getcwd()

parser = ArgumentParser(
    prog='nginx-lm',
    description='''

    tool for local management with nginx

''',
    epilog='''
    Attention, thy religious users of the holy piece of webserver

    ...NGINX!

    err, pronounce it as "Engine-X" alright?
        And don't ask me why is that.

    So... anyways
    nginx configs are pretty cool, but writing them is kind of a...
    "repetitive" task. specifically for the religious cruel users

    who use nginx for everything

    say... local management. err, I dunno what that means.

    anyways, I will write this later, and you will deal with it.

    Because, I am The Dark Lord Awal Garg aka Rash
    Accept me as your hero and have the most fantastic day of your life

'''
)

parser.add_argument(
    '-d', '--directory',
    help='set directory for current project, defaults to current working dir',
    default=CWD
)

parser.add_argument(
    '--debug',
    action="store_true", default=0,
    help='enable verbose logging'
)

parser.add_argument(
    "-r", "--no-auto-reload",
    action="store_true", default=False,
    help="just mutate the config files\
    do not issue `service nginx reload`"
)

parser.add_argument(
    "-n", "--project-name",
    help="set name of project, must be system wide unique\
    defaults to current directory name",
    default=os.path.basename(os.path.normpath(CWD))
)

# subparsers, for sub commands
subparser = parser.add_subparsers(help="One of the actions to take place")

# command: info, and insta exit
p_info = subparser.add_parser(
    'info',
    help='prints current system info including inferred nginx details'
)
p_info.set_defaults(module='info', no_auto_reload=True)

# command: install
p_install = subparser.add_parser(
    'install',
    aliases=['in'],
    help='install current project'
)

p_install.add_argument(
    "-t", "--template",
    help="set value of template to parse current app as",
    default=None
)
p_install.add_argument(
    "-p", "--port",
    help="port to service current project on, default 80",
    default=80,
    type=int
)
p_install.add_argument(
    "--host",
    help="set hostname for project, defaults to $CWD.dev",
    default=("%s.dev" % os.path.basename(os.path.normpath(CWD)))
)
p_install.add_argument(
    "--access-log",
    help="set access log file, defaults to $CWD/nlm-access.log",
    default=("%s/nlm-access.log" % CWD)
)
p_install.add_argument(
    "--error-log",
    help="set error log file, defaults to access log file itself",
    default=("%s/nlm-access.log" % CWD)
)

p_install.set_defaults(module='install')


# command: enable
p_enable = subparser.add_parser(
    'enable',
    aliases=['en'],
    help='enable current project'
)
p_enable.set_defaults(module='enable')


# command: disable
p_disable = subparser.add_parser(
    'disable',
    aliases=['di'],
    help='disable current project'
)
p_disable.set_defaults(module='disable')


# command: remove
p_remove = subparser.add_parser(
    'remove',
    aliases=['re'],
    help='remove current project'
)
p_remove.set_defaults(module='remove')


# command: status
p_status = subparser.add_parser(
    'status',
    aliases=['st'],
    help='get status of current project'
)
p_status.set_defaults(module='status')
p_status.set_defaults(no_auto_reload=True)


# command: logs
p_logs = subparser.add_parser(
    'logs',
    aliases=['lo'],
    help='tail logs of current project to stdout'
)
p_logs.add_argument(
    '-e', '--ignore-errors',
    action="store_true", default=False,
    help="Ignore all error logs, only show access logs"
)
p_logs.add_argument(
    '-a', '--ignore-access',
    action="store_true", default=False,
    help="Ignore all access logs, only show error logs"
)
p_logs.set_defaults(module='logs')
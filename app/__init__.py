from importlib import import_module
import logging
import subprocess

from app.src import interface

name = 'nginx-lm'
version = '0.0.1'
authors = ('Awal Garg aka Rash <awalgarg@gmail.com>')


def run():
    args = interface.parser.parse_args()
    args_module = getattr(args, 'module', None)

    if not args_module:
        interface.parser.parse_args(['-h'])
    else:
        mod = import_module('app.src.commands.%s' % args_module)
        if args.debug:
            logger = setup_custom_logger(name + '_logger', logging.DEBUG)
        mod.main(args)
        if not args.no_auto_reload:
            print(subprocess.getoutput('service nginx reload'))


def setup_custom_logger(name, level=logging.WARNING):
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(log_format)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(log_handler)
    return logger

logger = setup_custom_logger(name + '_logger')

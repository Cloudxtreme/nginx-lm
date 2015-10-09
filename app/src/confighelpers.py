"""
this module provides helper methods
to write, read and generate
nginx config files
"""

from pathlib import Path
from argparse import ArgumentParser
import subprocess
from pprint import pprint
from collections import namedtuple
import os
import json

from app.src.constants import Nginx_Dir_Type, Config_Status

Environment_Details = namedtuple(
    'Nginx_Environment_Details',
    'version args dir_type'
)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_config_dir(etc_path):
    ETC_PATH = Path(etc_path)
    confd = ETC_PATH.joinpath('conf.d')
    assert(confd.is_dir())  # if this fails, nginx is malformed
    sites_enabled = ETC_PATH.joinpath('sites-enabled')
    sites_available = ETC_PATH.joinpath('sites-available')
    if (sites_available.is_dir() and sites_enabled.is_dir()):
        return Nginx_Dir_Type.full
    else:
        return Nginx_Dir_Type.light


def parse_argline(argline):
    parser = ArgumentParser()

    # arg
    # example value

    parser.add_argument('--prefix')
    # /etc/nginx
    parser.add_argument('--sbin-path')
    # /usr/sbin/nginx
    parser.add_argument('--conf-path')
    # /etc/nginx/nginx.conf
    parser.add_argument('--error-log-path')
    # /var/log/nginx/error.log
    parser.add_argument('--http-log-path')
    # /var/log/nginx/access.log
    parser.add_argument('--pid-path')
    # /var/run/nginx.pid
    parser.add_argument('--lock-path')
    # /var/run/nginx.lock
    parser.add_argument('--user')
    # nginx
    parser.add_argument('--group')
    # nginx

    parser.add_argument(
        '--with-http_auth_request_module', action="store_true", default=False
    )
    parser.add_argument(
        '--with-mail', action="store_true", default=False
    )
    parser.add_argument(
        '--with-mail_ssl_module', action="store_true", default=False
    )
    parser.add_argument(
        '--with-http_v2_module', action="store_true", default=False
    )
    parser.add_argument(
        '--with-ipv6', action="store_true", default=False
    )

    ns, _ = parser.parse_known_args(argline.split(' '))

    return ns


def get_nginx_details():
    ver_id = 'nginx version: nginx/'
    args_id = 'configure arguments: '

    version = ''
    argline = ''

    config = subprocess.getoutput('nginx -V').split('\n')

    for conf in config:

        if conf.strip().startswith(ver_id):
            version = conf.replace(ver_id, '').strip()

        elif conf.strip().startswith(args_id):
            argline = conf.strip().replace(args_id, '').strip()

    args = parse_argline(argline)
    return Environment_Details(version, args, get_config_dir(args.prefix))


def write_state(state, args=None):
    f = open('%s/.nginx-lm-state' % args.directory, 'w')
    json.dump(state, f, indent=4)
    f.close()


def read_state(args=None):
    f = open('%s/.nginx-lm-state' % args.directory, 'r')
    ret = json.load(f)
    f.close()
    return ret


def erase_state(args):
    Path('%s/.nginx-lm-state' % args.directory).unlink()


def enable_config(id):
    """
        if nginx flavor is light and dir is conf.d
            mv $dir/$ID.conf.disabled $DIR/$ID.conf
        else if nginx flavor is everything and dir is sites-available
            symlink $dir/$ID.conf to $dir/..sites-enabled/$ID.conf
        else
            Raise TypeError
    """
    assert(config_status(id) == Config_Status.disabled)
    if env.dir_type == Nginx_Dir_Type.full:
        try:
            prefix_path.joinpath(
                "sites-available/%s.lm.conf" % id
            ).symlink_to(
                "%ssites-enabled/%s.lm.conf" % (env.config.prefix, id)
            )
        except Exception as e:
            raise e
    elif env.dir_type == Nginx_Dir_Type.light:
        try:
            os.rename(
                "%s/conf.d/%s.lm.conf.disabled" % (env.args.prefix, id),
                "%s/conf.d/%s.lm.conf" % (env.args.prefix, id)
            )
        except Exception as e:
            raise e


def disable_config(id):
    assert(config_status(id) == Config_Status.enabled)
    if env.dir_type == Nginx_Dir_Type.full:
        try:
            prefix_path.joinpath(
                "sites-enabled/%s.lm.conf" % id
            ).unlink()
        except Exception as e:
            raise e
    elif env.dir_type == Nginx_Dir_Type.light:
        try:
            os.rename(
                "%s/conf.d/%s.lm.conf" % (env.args.prefix, id),
                "%s/conf.d/%s.lm.conf.disabled" % (env.args.prefix, id)
            )
        except Exception as e:
            raise e


def toggle_config(id):
    status = config_status(id)
    if env.dir_type == Nginx_Dir_Type.full:
        try:
            if status == Config_Status.enabled:
                disable_config(id)
                return False
            elif status == Config_Status.disabled:
                enable_config(id)
                return True
            else:
                raise RuntimeError("%s is not a registered config file!" % id)
        except Exception as e:
            raise e
    elif env.dir_type == Nginx_Dir_Type.light:
        try:
            if status == Config_Status.enabled:
                disable_config(id)
                return False
            elif status == Config_Status.disabled:
                enable_config(id)
                return True
            else:
                raise RuntimeError("%s is not a registered config file!" % id)
        except Exception as e:
            raise e


def uninstall_config(id):
    assert(config_status(id) == Config_Status.disabled)
    conf_path = get_conf_path(id)
    conf_path.unlink()


def config_status(id):
    if env.dir_type == Nginx_Dir_Type.full:
        try:
            if prefix_path.joinpath(
                "sites-enabled/%s.lm.conf" % id
            ).is_symlink():
                return Config_Status.enabled
            elif prefix_path.joinpath(
                "sites-available/%s.lm.conf" % id
            ).is_file():
                return Config_Status.disabled
            else:
                return Config_Status.not_found
        except Exception as e:
            raise e
    elif env.dir_type == Nginx_Dir_Type.light:
        try:
            if prefix_path.joinpath(
                "conf.d/%s.lm.conf" % id
            ).is_file():
                return Config_Status.enabled
            elif prefix_path.joinpath(
                "conf.d/%s.lm.conf.disabled" % id
            ).is_file():
                return Config_Status.disabled
            else:
                return Config_Status.not_found
        except Exception as e:
            raise e


def install_config(id):
    assert(config_status(id) == Config_Status.not_found)
    if env.dir_type == Nginx_Dir_Type.full:
        try:
            prefix_path.joinpath(
                "sites-available/%s.lm.conf" % id
            ).touch(exist_ok=False)
        except Exception as e:
            raise e
    elif env.dir_type == Nginx_Dir_Type.light:
        try:
            prefix_path.joinpath(
                "conf.d/%s.lm.conf.disabled" % id
            ).touch(exist_ok=False)
        except Exception as e:
            raise e


def get_conf_path(id):
    status = config_status(id)
    assert(status != Config_Status.not_found)
    if env.dir_type == Nginx_Dir_Type.full:
        return prefix_path.joinpath(
            "sites-available/%s.lm.conf" % id
        )
    elif env.dir_type == Nginx_Dir_Type.light:
        if status == Config_Status.enabled:
            return prefix_path.joinpath(
                "conf.d/%s.lm.conf" % id
            )
        elif status == Config_Status.disabled:
            return prefix_path.joinpath(
                "conf.d/%s.lm.conf.disabled" % id
            )


def set_config(id, config_text):
    assert(config_status(id) != Config_Status.not_found)
    try:
        conf_path = get_conf_path(id)
        conf_file = open(str(conf_path), 'w')
        conf_file.write(config_text)
        conf_file.close()
    except Exception as e:
        raise e


def hosts_add(host):
    return subprocess.check_output(
        'echo "127.0.0.1 %s" >> /etc/hosts' % host,
        shell=True
    )


def hosts_remove(host):
    return subprocess.check_output(
        'sed -ibak \'/^127\\.0\\.0\\.1[[:space:]]%s/d\'\
 /etc/hosts' % host,
        shell=True
    )


env = get_nginx_details()
prefix_path = Path(env.args.prefix)

if __name__ == "__main__":
    print(
        """
        Running this script directly gives a real quick demo
        of nginx-lm basics. If you are running this script
        for the first time, we will see if a test script
        is already registered or not.

        If not, we register it, and your server lives!

        Else, we disable the previously registered script.
        """
    )
    test_conf_status = config_status('test')
    if test_conf_status == Config_Status.not_found:
        print('Registering new config!')
        register_config('test')
        set_config('test', """
server {
    listen 8080;
    root %s;
    server_name localhost;
    index index.html index.htm index.php;
    autoindex on;
}
        """ % os.path.dirname(os.path.realpath(__file__)))
        enable_config('test')
    elif test_conf_status == Config_Status.enabled:
        print('Disabling previously registed config')
        disable_config('test')
    elif test_conf_status == Config_Status.disabled:
        print('Uninstalling the disabled script!')
        uninstall_config('test')
    print(subprocess.getoutput('service nginx reload'))

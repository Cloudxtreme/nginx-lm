import json
import subprocess
from glob import glob

import app
from app.src import confighelpers as Configurer
from app.src.constants import Nginx_Dir_Type


def main(args=None):
    n_version, n_args, n_dir_type = Configurer.get_nginx_details()
    if n_dir_type == Nginx_Dir_Type.light:
        n_dir = "%s/conf.d" % n_args.prefix
    else:
        n_dir = "%s/sites-available" % n_args.prefix

    registered_configs = json.dumps(
        glob("%s/*.lm.conf*" % n_dir),
        indent=4,
        sort_keys=True
    )

    print(
        '''
%s: %s

Registered configs:
%s

Environment details:
%s
''' % (
            app.name,
            app.version,
            registered_configs,
            json.dumps((n_version, vars(n_args)), indent=4, sort_keys=True)
        )
    )

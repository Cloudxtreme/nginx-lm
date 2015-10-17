from app.src import template as Template
from app.src.constants import Template_Score, Template_Type
from app.src import confighelpers as Configurer

TEMPLATE_TYPE = Template_Type.managed


def predict_score(args=None, shelf=None):
    return Template_Score.unsure


def construct_config(args=None, shelf=None):
    main_config = '''
    listen {port};
    server_name {host};
    root {directory};
    autoindex on;
    access_log {access_log};
    error_log {error_log};
'''.format(**vars(args))

    if args.cors:
        main_config = main_config + '''
    add_header 'Access-Control-Allow-Origin' '*';
    add_header 'Access-Control-Allow-Credentials' 'true';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
'''

    return "server {\n%s\n}" % main_config


def post_install(args=None, shelf=None):
    return Configurer.hosts_add(args.host)


def rollback(args=None, shelf=None):
    return Configurer.hosts_remove(args.host)

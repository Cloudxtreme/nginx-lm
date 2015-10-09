from app.src import template as Template
from app.src.constants import Template_Score, Template_Type
from app.src import confighelpers as Configurer

TEMPLATE_TYPE = Template_Type.managed


def predict_score(args=None):
    return Template_Score.unsure


def construct_config(args=None):
    return '''
server {{
    listen {port};
    server_name {host};
    root {directory};
    autoindex on;
    access_log {access_log};
    error_log {error_log};
}}
'''.format(**vars(args))


def post_install(args=None):
    return Configurer.hosts_add(args.host)


def rollback(args=None):
    return Configurer.hosts_remove(args.host)

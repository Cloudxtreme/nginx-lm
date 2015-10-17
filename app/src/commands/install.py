import os
import re
from itertools import chain
from pathlib import Path
from importlib import import_module
import time

from app.config import TEMPLATE_STORE_LOCATION
from app.src.constants import Template_Score, Template_Type
from app.src import confighelpers as Configurer
from app.src.commands.config import shelf


def get_available_templates():
    for path in chain(*next(os.walk(TEMPLATE_STORE_LOCATION))[1:]):
        path_obj = Path(TEMPLATE_STORE_LOCATION).joinpath(path)
        if path.endswith('.py') and path_obj.is_file():
            yield re.sub(r'.py$', '', path)
        elif path_obj.is_dir() and path_obj.joinpath('__init__.py').is_file():
            yield path


def load_template(name):
    return import_module('app.templates.%s' % name)


def find_suitable_template(templates, *control):
    lastPotentialMatch = None  # this shall be returned if no perfect template
    lastPotentialMatchName = ''
    for template_name in templates:
        template = load_template(template_name)
        matching_score = template.predict_score(*control)
        if matching_score == Template_Score.perfect_match:
            return matching_score, template_name, template  # return 1st match
        elif matching_score == Template_Score.unsure:
            if lastPotentialMatch is None:  # to not return last unsure match
                lastPotentialMatch = template
                lastPotentialMatchName = template_name
    if lastPotentialMatch is None:
        raise RuntimeError("No suitable template found!")
    return Template_Score.unsure, lastPotentialMatchName, lastPotentialMatch


def install_with_template(args, name, template):
    state = {
        'ts': time.time(),
        'status': 'enabled',
        'template_name': name,
        'args': vars(args)
    }
    print("Preparing to initialize template, host is %s" % args.host)
    if template.TEMPLATE_TYPE == Template_Type.managed:
        state['template_type'] = 'managed'
        config = template.construct_config(args, shelf)
        Configurer.install_config(args.project_name)
        Configurer.set_config(args.project_name, config)
        Configurer.enable_config(args.project_name)
    elif template.TEMPLATE_TYPE == Template_Type.unmanaged:
        state['template_type'] = 'unmanaged'
        template.initialize(args, shelf)
    else:
        raise RuntimeError('Malformed template!')

    if getattr(template, 'post_install', None):
        state['has_post_install'] = True
        template.post_install(args, shelf)

    Configurer.write_state(state, args)
    shelf.sync()


def main(args):
    if not args.template:
        print("No default template passed, finding a suitable match...")
        score, template_name, template = find_suitable_template(
            get_available_templates()
        )
        if score == Template_Score.unsure:
            check = input(
                "No perfectly matching module was found,\
 go with unsure match %s? (y/n)"
                % template_name
            )
            if not check.startswith('y'):
                print("Aborting... (user canceled operation)")
                return
        else:
            print("Detected template: %s" % template_name)
    else:
        score, template_name, template = (
            Template_Score.perfect_match,
            args.template,
            load_template(args.template)
        )

    print("Intitializing templated configuration agent: %s" % template_name)
    install_with_template(args, template_name, template)
    print("All done, hopefully!")

from importlib import import_module

from app.src import confighelpers as Configurer
from app.src.commands import disable
from app.src.constants import Config_Status


def main(args=None):
    state = Configurer.read_state(args)
    if state['status'] == 'enabled':
        print("Gracefully disabling config...")
        disable.main(args)
    c_args = Configurer.Struct(**state.get('args', args))
    if state.get('has_post_install'):
        print("Rolling back changes")
        import_module(
            'app.templates.%s' % state['template_name']
        ).rollback(c_args)
    Configurer.uninstall_config(c_args.project_name)
    Configurer.erase_state(c_args)
    print('Aww! That was pretty sad, but we removed all traces...')

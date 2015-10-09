import json

from app.src import confighelpers as Configurer


def main(args=None):
    print("Project state:")
    state = Configurer.read_state(args)
    c_args = Configurer.Struct(**state.get('args', args))
    print(json.dumps(state, indent=4, sort_keys=True))
    status = Configurer.config_status(c_args.project_name)
    print("Config status: %s" % status)

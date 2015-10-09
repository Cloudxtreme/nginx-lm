from app.src import confighelpers as Configurer


def main(args=None):
    state = Configurer.read_state(args)
    c_args = Configurer.Struct(**state.get('args', args))
    Configurer.enable_config(c_args.project_name)
    state['status'] = 'enabled'
    Configurer.write_state(state, c_args)
    pass

import subprocess
import time
import select
import sys

from app.src import confighelpers as Configurer


def tail(*paths):
    args = ['tail']
    for path in set(paths):
        args.append('-F')
        args.append(path)

    f = subprocess.Popen(
        args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    p = select.poll()
    p.register(f.stdout)

    try:
        while True:
            if p.poll(1):
                print(f.stdout.readline().decode())
            time.sleep(1)
    except KeyboardInterrupt:
        print('Aborted...')
        sys.exit(0)


def main(args):
    state = Configurer.read_state(args)
    c_args = Configurer.Struct(**state.get('args'))
    tail(c_args.access_log, c_args.error_log)
    pass

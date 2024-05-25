import subprocess, sys
from abc import ABC
from dataclasses import dataclass
from shell.util import print_flush, resolve_path

@dataclass
class Command(ABC):
    name: str
    args: str

    @staticmethod
    def parse(raw: str) -> 'Command':
        name, _, args = raw.partition(' ')
        match name.lower():
            case 'echo'                  : return CommandEcho(name, args)
            case 'exit'                  : return CommandExit(name, args)
            case 'type'                  : return CommandType(name, args)
            case _ if resolve_path(name) : return CommandRun(name, args)
            case _                       : return CommandNotFound(name, args)

class CommandEcho(Command):
    def __call__(self):
        print_flush(self.args)

class CommandExit(Command):
    def __call__(self, code = 0):
        if len(self.args):
            code = int(self.args)
        sys.exit(code)

class CommandRun(Command):
    def __call__(self):
        path = resolve_path(self.name)
        result = subprocess.run([path, self.args], capture_output=True)
        print_flush(result.stdout.decode(), end='')

class CommandType(Command):
    def __call__(self):
        BUILTINS = ['echo', 'exit', 'type']

        if self.args.lower() in BUILTINS:
            print_flush(f'{self.args} is a shell builtin')
        elif path := resolve_path(self.args):
            print_flush(f'{self.args} is {path}')
        else:        
            print_flush(f'{self.args} not found')

class CommandNotFound(Command):
    def __call__(self):
        print_flush(f'{self.name}: command not found')
        
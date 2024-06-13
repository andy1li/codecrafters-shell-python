import os, subprocess, sys
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
            case 'cd'                    : return CommandCd(name, args)
            case 'echo'                  : return CommandEcho(name, args)
            case 'exit'                  : return CommandExit(name, args)
            case 'pwd'                   : return CommandPwd(name, args)
            case 'type'                  : return CommandType(name, args)
            case _ if resolve_path(name) : return CommandRun(name, args)
            case _                       : return CommandNotFound(name, args)

class CommandCd(Command):
    def __call__(self):
        try:
            os.chdir(os.path.expanduser(self.args))
        except FileNotFoundError:
            print_flush(f'cd: {self.args}: No such file or directory')

class CommandEcho(Command):
    def __call__(self):
        print_flush(self.args)

class CommandExit(Command):
    def __call__(self, code = 0):
        if len(self.args):
            code = int(self.args)
        sys.exit(code)

class CommandPwd(Command):
    def __call__(self):
        print_flush(os.getcwd())

class CommandRun(Command):
    def __call__(self):
        path = resolve_path(self.name)
        result = subprocess.run([path, self.args], capture_output=True)
        print_flush(result.stdout.decode(), end='')

class CommandType(Command):
    def __call__(self):
        builtins = [
            repr(sub)
                .removeprefix("<class 'shell.command.Command")
                .removesuffix("'>")
                .lower()
            for sub in Command.__subclasses__()
        ]
        builtins.remove('notfound')
        builtins.remove('run')

        if self.args in builtins:
            print_flush(f'{self.args} is a shell builtin')
        elif path := resolve_path(self.args):
            print_flush(f'{self.args} is {path}')
        else:        
            print_flush(f'{self.args}: not found')

class CommandNotFound(Command):
    def __call__(self):
        print_flush(f'{self.name}: command not found')
        
from shell.command import Command
from shell.util import print_flush

def main():
    while True:
        print_flush('$ ', end='')
        command = Command.parse(input())
        command()

if __name__ == "__main__":
    main()

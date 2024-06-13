from shell.command import Command

if __name__ == "__main__":
    while True:
        command = Command.parse(input('$ '))
        command()

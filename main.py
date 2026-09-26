import sys


def main():
    """Entrypoint function for the program"""
    args = sys.argv
    if len(args) == 1:
        import gui

        gui.App()
    elif len(args) and args[1] == "--cli":
        import cli

        menu = cli.CliMenu()
        menu.main_cli()
        print("CLI")
    else:
        print("Unknown arguments, use --cli for cli mode or nothing for gui mode")


if __name__ == "__main__":
    main()

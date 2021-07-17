#! /usr/bin/python3
"""
Implement `cat` command with python code.
"""

import click


@click.command()
@click.argument('files', type=click.File('r'), nargs=-1)
@click.option('-n', '--number', is_flag=True, help="number all output lines")
def cat_cmd(files, number):
    """
    cat - concatenate files and print on the standard output
    """
    line_count = 1
    for _file in files:
        for line in _file:
            show_line = line_count if number else ""
            click.echo(f"{show_line:<5}  {line}", nl=False)
            line_count += 1


if __name__ == "__main__":
    cat_cmd()

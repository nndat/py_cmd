#! /usr/bin/python3
"""
Implement `wc` command with python code.
"""

import click


def _get_file_stat(file):
    words, lines, chars = 0, 0, 0

    for line in file.readlines():
        chars += len(line)
        lines += 1
        words += len(line.split())

    stat = {
        'lines': lines,
        'words': words,
        'chars': chars,
    }
    return stat


def _display(
    stats,
    filename,
    show_header=False
):
    cols = [f'{col:<5}' for col in stats.keys()]
    values = [f'{val:<5}' for val in stats.values()]
    cols.append("Filename")
    values.append(filename)
    if show_header:
        click.echo(' '.join(cols))
    click.echo(' '.join(values))


@click.command()
@click.argument('files', type=click.File('rb'), nargs=-1)
@click.option('-w', '--word', is_flag=True, default=True)
@click.option('-l', '--line', is_flag=True)
@click.option('-c', '--char', is_flag=True)
def wc_cmd(files, *args, **kwargs):
    show_header = True
    for file in files:
        stat = _get_file_stat(file)
        _display(stat, file.name, show_header=show_header)
        show_header = False


if __name__ == "__main__":
    wc_cmd()

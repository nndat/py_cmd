#! /usr/bin/python3
"""
Implement ls command with python code.
"""

import click
from pathlib import Path
from datetime import datetime, timezone


def _in_dir(dirpath=".", recursive=False):
    """
    List all file and directory in dirpath (default is current directory)
    """
    directory = Path(dirpath)
    if not directory.exists():
        raise FileNotFoundError("No such file or directory")
    
    for child in directory.iterdir():
        if child.is_dir() and recursive:
            child_path = str(child.absolute())
            return _in_dir(child_path)
        yield child


def _show_detail(dir_infos):
    """
    Display childrent in directory with detail infos.
    """
    detail_template = "{name:<30}{size:<10}{owner:<10}{group:<10}{last_modificated:<10}"
    header = detail_template.format(name="Name", size="Size", owner="Owner", group="Group", last_modificated="Last Modificated")

    print(header)
    for child in dir_infos:
        stat = child.stat()
        display_infos = {
            'name': child.name,
            'size': stat.st_size,
            'group': child.group(),
            'owner': child.owner(),
            'last_modificated': datetime.fromtimestamp(
                stat.st_mtime,
                tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
        }
        print(detail_template.format(**display_infos))


def _show_simple(dir_infos):
    """
    Just display name of children in directory.
    """
    for child in dir_infos:
        print(child.name)


def _display_dir_infos(dir_infos, show_detail=True):
    """
    Display childrent in directory
    """
    if show_detail:
        _show_detail(dir_infos)
    _show_simple(dir_infos)


@click.command()
@click.argument('dirpath', default=".", type=str)
@click.option('-l', '--detail', is_flag=True)
def ls_command(dirpath, detail, *args, **kwargs):
    """
    List information about the dirpath (the current directory by default).
    """
    try:
        dir_infos = _in_dir(dirpath)
        _display_dir_infos(dir_infos, show_detail=detail)
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    ls_command()

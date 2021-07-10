#! /usr/bin/python3
"""
Implement ls command with python code.
"""

from pathlib import Path
from datetime import datetime
from datetime import timezone
import click


def _in_dir(dirpath=".", recursive=False, include_hidden=False):
    """
    List all file and directory in dirpath (default is current directory)
    """
    directory = Path(dirpath)
    if not directory.exists():
        raise FileNotFoundError("No such file or directory")

    if directory.is_file():
        yield directory
    else:
        for child in directory.iterdir():
            if child.name.startswith('.') and not include_hidden:
                continue

            if child.is_dir() and recursive:
                child_path = str(child.absolute())
                return _in_dir(child_path)
            yield child
    return None


def _show_detail(dir_infos):
    """
    Display childrent in directory with detail infos.
    """
    detail_template = \
        "{name:<30}{size:<10}{owner:<10}{group:<10}{last_modificated:<10}"

    header = detail_template.format(
        name="Name",
        size="Size",
        owner="Owner",
        group="Group",
        last_modificated="Last Modificated"
    )

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
@click.option('-a', '--all', is_flag=True)
def ls_command(dirpath, *args, **kwargs):
    """
    List information about the dirpath (the current directory by default).
    """
    try:
        detail = kwargs.get('detail')
        include_hidden = kwargs.get('all')
        dir_infos = _in_dir(dirpath, include_hidden=include_hidden)
        _display_dir_infos(dir_infos, show_detail=detail)
    except FileNotFoundError as message:
        print(message)


if __name__ == '__main__':
    ls_command()

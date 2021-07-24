import click


def sort(files, **kwargs):
    reverse = kwargs.get('reverse', False)
    lines = (line for file in files for line in file.readlines())
    return sorted(lines, reverse=reverse)


@click.command()
@click.argument("files", type=click.File('r'), nargs=-1)
@click.option('-r', '--reverse', is_flag=True, default=False)
@click.option('-n', '--line', is_flag=True, default=False)
def sort_cmd(files, reverse, line):
    for index, content in enumerate(sort(files, reverse=reverse), start=1):
        line_index = index if line else ""
        print(f"{line_index:>3} {content}", end="")


if __name__ == "__main__":
    sort_cmd()

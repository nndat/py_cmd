from datetime import datetime
import calendar

import click


@click.command()
@click.option('-y', '--year', type=int, default=datetime.today().year)
@click.option('-m', '--month', type=int, default=datetime.today().month)
def cal_cmd(year, month):
    calendar.prmonth(year, month)


if __name__ == "__main__":
    cal_cmd()

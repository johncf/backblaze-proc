#!env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as grid
from   matplotlib.ticker import FuncFormatter
import csv

def date_format(x, pos=None):
    xd = dates.num2date(x)
    fmt = '%Y' if xd.month == 1 else '%b'
    return xd.strftime(fmt)

def read_csv(csvfile):
    xs, dc, fc = [], [], []
    with open(csvfile, 'r') as file_:
        reader = csv.reader(file_, delimiter=',')
        for row in reader:
            xs.append(dates.datestr2num(row[0]))
            dc.append(int(row[1]))
            fc.append(int(row[2]))
    return xs, dc, fc

# psql backblaze -c "COPY (SELECT datestamp, SUM(1) AS dcount, SUM(CAST(failed AS INT)) AS fcount FROM raw_logs WHERE model='ST3000DM001' GROUP BY datestamp ORDER BY datestamp) TO STDOUT WITH DELIMITER ','" > processed/daily-stats-10.csv
# ./daily-stats-plot.py processed/daily-stats-10.csv plots/daily-stats-10.svg "Model: Seagate ST3000DM001"

def main(infile, outfile, title):
    xs, dct, fct = read_csv(infile)

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]},
                                   figsize=(7, 6), sharex=True)
    st = fig.suptitle(title)
    fig.tight_layout()
    st.set_y(0.95)
    fig.subplots_adjust(top=0.9)

    ax1.set_ylim(0, 50);
    ax1.set_ylabel("# failures per day")
    ax1.set_xlim(dates.datestr2num('2014-01-01'), dates.datestr2num('2015-01-01'));

    ax2.set_ylim(0, 12500);
    ax2.set_ylabel("# disks deployed")
    ax2.xaxis.set_major_locator(dates.MonthLocator(bymonth=[1, 5, 9]))
    ax2.xaxis.set_minor_locator(dates.MonthLocator())
    ax2.xaxis.set_major_formatter(FuncFormatter(date_format))

    ax1.vlines(xs, 0, fct, colors='#cc7777')
    ax2.plot(xs, dct)
    fig.savefig(outfile, bbox_inches='tight')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Compute basic statistics from failure and observation data.')
    parser.add_argument('infile', help='daily logs summary (csv file)')
    parser.add_argument('outfile', help='path to save plot (image file)')
    parser.add_argument('title', help='plot title')
    args = parser.parse_args()
    main(args.infile, args.outfile, args.title)

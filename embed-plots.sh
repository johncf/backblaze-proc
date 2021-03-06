#!/bin/bash
set -e
cat plot-metadata | while read line
do
    IFS='|' read -r -a array <<< "$line"
    model=${array[3]}
    plot=${array[0]}
    fails=${array[1]}
    obsct=${array[2]}

    statsstr=$(./failysis/fail-stats.py -m $fails $obsct)
    IFS=' ' read -r -a stats <<< "$statsstr"

    echo "### $model"
    echo
    echo "**Total disk-years observed:** ${stats[0]} <br>"
    echo "**Total failures observed:** ${stats[1]} <br>"
    echo "**Mean failure rate:** ${stats[2]} per year"
    echo
    echo "**Useful power-on span of observation:** ${stats[3]} years <br>"
    echo "**Mean number of disks over useful span:** ${stats[4]} disks <br>"
    echo "**Window size:** "
    echo
    echo "![$model failure rate plot]({attach}$plot)"
    echo
done

#!/usr/bin/env bash
# Recreate the public daily dataset used by the owner-protocol tests. Usage: research/fetch_data.sh <data_dir>
set -euo pipefail
D=${1:?data dir}; mkdir -p "$D"; NOW=$(date +%s)
fred() { curl -sf -m 60 -o "$D/$2.csv" "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$1&cosd=$3"; }
yh() { curl -sf -m 60 -A "Mozilla/5.0" -o "$D/$2.json" "https://query1.finance.yahoo.com/v8/finance/chart/$1?period1=$3&period2=$NOW&interval=1d&includeAdjustedClose=true&events=div%2Csplit"; }
fred DFII10 DFII10 2019-01-01; fred DFF DFF 2017-01-01; fred DFF DFF07 2007-01-01
for s in GVZCLS VXNCLS VIXCLS VXVCLS; do fred $s $s 2018-01-01; done
fred VIXCLS VIXCLS07 2007-01-01; fred VXVCLS VXVCLS07 2007-01-01
for p in GLD:GLD SLV:SLV GC=F:GCF SI=F:SIF; do yh "${p%%:*}" "${p##*:}" 1546300800; done
for p in GLD:GLD18 GC=F:GCF18 %5ENDX:NDX %5EGSPC:GSPC; do yh "${p%%:*}" "${p##*:}" 1514764800; done
for p in IEF:IEF07 QQQ:QQQ07 SPY:SPY07 %5ENDX:NDX07 %5EGSPC:GSPC07; do yh "${p%%:*}" "${p##*:}" 1167609600; done
echo "done: $(ls "$D" | wc -l) files in $D"

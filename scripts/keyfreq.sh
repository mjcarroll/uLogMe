#!/bin/bash
# keyfreq.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# Logs the key press frequency over 10 second window.
# Logs are written in logs/keyfreqX.txt every 10 seconds, where X is unix timestamp of 7am of the recording day.

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f ~/.color.sh ] && . ~/.color.sh
[ -f color.sh ] && . color.sh

LANGUAGE=en
LANG=en_US.utf8

helperfile="../logs/keyfreqraw.txt"  # temporary helper file

mkdir -p ../logs

while true; do
    # Thanks to https://github.com/Naereen/ulogme/pull/5/
    showkey | tr -d '0-9' &> "$helperfile" &
    # PID=$!

    # work in windows of 10 seconds
    sleep 10

    # XXX Find a safer and better way to kill the process
    # kill $PID
    kill "$(jobs -rp)" 2>/dev/null
    wait "$(jobs -rp)" 2>/dev/null

    # count number of key release events
    num=$(grep -c release "$helperfile")

    # append unix time stamp and the number into file
    logfile="../logs/keyfreq_$(python rewind7am.py).txt"
    echo "$(date +%s) $num"  >> "$logfile"
    # only print if $num > 0
    if [ "$num" -gt 0 ]; then
        echo -e "Logged ${yellow}key frequency${white}: ${magenta}$(date)${white} ${green}${num}${white} release events detected into '${black}${logfile}${white}'"
    fi
done


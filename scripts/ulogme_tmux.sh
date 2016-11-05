#!/bin/bash
# ulogme_tmux.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# Experimental script to start a new tab in a tmux session, launching the data collection on the right & and Python web server on the left.

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

echo -e "${yellow}Starting '${black}ulogme_tmux.sh'${white} ..."

if [ -L "${BASH_SOURCE[0]}" ]; then
    # We have a symlink... how to deal with it?
    cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )"
else
    cd "$( dirname "${BASH_SOURCE[0]}" )"
fi;

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "${red}This script ${black}${0}${red} has to be run inside a tmux session.${white}"
    exit 1
fi

port="${1:-8443}"  # Default is port=8124
IP="${2:-localhost}"
protocol="${3:-https}"

# Reference tmux man page (eg. https://linux.die.net/man/1/tmux)
# start a new window,
# name it ulogme
tmux new-window -n 'uLogMe' "./ulogme_data.sh | tee /tmp/ulogme_data_$$.log"
# launch './ulogme_data.sh' in first one

# split it half
# launch './ulogme_serve.sh' in first one
tmux split-window -d "./ulogme_serve.sh ${port} ${IP} ${protocol} | tee /tmp/ulogme_serve_$$.log"
# tmux rename-window 'uLogMe Server'

sleep 12
# return to current tab at the end
tmux last-window

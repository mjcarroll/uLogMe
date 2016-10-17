#!/bin/bash
# ulogme_tmux.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# Experimental script to start a new tab in a tmux session, launching the data collection on the right & and Python web server on the left.

echo "Starting 'ulogme_tmux.sh' ..."

# FIXED no need to adapt this to the path where you stored ulogme.git/
# cd ~/.local/share/ulogme/scripts/  # XXX change according to your installation
if [ -L "${BASH_SOURCE[0]}" ]; then
    # We have a symlink... how to deal with it?
    cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )"
else
    cd "$( dirname "${BASH_SOURCE[0]}" )"
fi;

# pwd  # DEBUG
# echo "[Enter]"  # DEBUG
# read  # DEBUG

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "This script has to be run inside a tmux session."
    exit 1
fi

port="${1:-8124}"

# Reference https://linux.die.net/man/1/tmux
# start a new window,
# name it ulogme
tmux new-window -n 'uLogMe' ./ulogme_serve.sh "${port}"

# launch './ulogme_serve.sh' in second one
# split it half
# tmux split-window -h ./ulogme_serve.sh
tmux split-window -h ./ulogme_data.sh
# tmux rename-window 'uLogMe Server'

# launch './ulogme.sh' in first one
# tmux select-pane -L
# tmux rename-window 'uLogMe Data'
# tmux run-shell ./ulogme.sh

sleep 12
# return to current tab ?
tmux last-window

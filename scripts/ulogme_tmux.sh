#!/bin/bash
# Experimental script to start a new tab in a tmux session, launching the data collection on the right & and Python web server on the left.
# https://github.com/Naereen/ulogme/

# oldpwd="$(pwd)"
echo "Calling 'ulogme_tmux.sh' ..."

cd ~/.local/share/ulogme/  # XXX change according to your installation

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "This script has to be run inside a tmux session."
    exit 1
fi

port=${1:-8124}

# Reference https://linux.die.net/man/1/tmux
# start a new window,
# name it ulogme
tmux new-window -n 'uLogMe' ulogme_serve.sh ${port}

# launch 'ulogme_serve.sh' in second one
# split it half
# tmux split-window -h ulogme_serve.sh
tmux split-window -h ulogme_data.sh
# tmux rename-window 'uLogMe Server'

# launch 'ulogme.sh' in first one
# tmux select-pane -L
# tmux rename-window 'uLogMe Data'
# tmux run-shell ulogme.sh

sleep 10
# return to current tab ?
tmux last-window
# cd "${oldpwd}"  # DEBUG ?

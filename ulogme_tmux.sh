#!/bin/bash
oldpwd="$(pwd)"
echo "Calling 'ulogme_tmux.sh' ..."

cd ~/.local/share/ulogme/

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "This script has to be run inside a tmux session."
    exit 1
fi

# Reference https://linux.die.net/man/1/tmux
# start a new window,
# name it ulogme
tmux new-window -n 'uLogMe' 'ulogme_serve.sh'

# launch 'ulogme_serve.sh' in second one
# split it half
# tmux split-window -h 'ulogme_serve.sh'
tmux split-window -h 'ulogme.sh'
# tmux rename-window 'uLogMe Server'

# launch 'ulogme.sh' in first one
# tmux select-pane -L
# tmux rename-window 'uLogMe Data'
# tmux run-shell ulogme.sh

# return to current tab ?
tmux last-window

cd "${oldpwd}"

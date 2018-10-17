#!/bin/bash
# note.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# allows the user to simply record a note, saves it together with unix time in ../logs/notes_...
# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

cd "$( dirname "${BASH_SOURCE[0]}" )"

mkdir -p ../logs/

read -r -p "Enter note: " n

if [ -z "$1" ]; then
    T="$(date +%s)" # default to current time
else
    T="$1"  # argument was provided, use it!
fi

logfile="../logs/notes_$(python3 ./rewind7am.py "$T").txt"
echo "$T $n" >> "$logfile"
echo -e "Logged ${yellow}note${reset}: ${magenta}$T${reset} ${green}$n${reset} into '${black}$logfile${reset}'"

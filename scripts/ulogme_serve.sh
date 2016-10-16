#!/bin/bash
# ulogme_serve.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

echo "Starting 'ulogme_serve.sh' ..."

# FIXED no need to adapt this to the path where you stored ulogme.git/
# cd ~/.local/share/ulogme/scripts/  # XXX change according to your installation
cd "$( dirname "${BASH_SOURCE[0]}" )"

port="${1:-8124}"

if pidof firefox >/dev/null; then
	echo -e "Opening 'http://localhost:${port}/' in Firefox ..."
	firefox -new-tab "http://localhost:${port}"/ &
	# xdg-open "http://localhost:${port}"/ &
else
	echo -e "Firefox is not running, by default the uLogMe page will not be opened ..."
	echo -e "('http://localhost:${port}/' is only opened in a new tab if your Firefox is already running)."
fi

echo -e "Calling 'python ulogme_serve.py ${port}' ..."
python ./ulogme_serve.py "${port}"

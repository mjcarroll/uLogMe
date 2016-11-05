#!/bin/bash
# ulogme_serve.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

echo -e "${yellow}Starting '${black}ulogme_serve.sh${white}' ..."

cd "$( dirname "${BASH_SOURCE[0]}" )"

port="${1:-8124}"  # Default is port=8124

if pidof firefox >/dev/null; then
	echo -e "${yellow}Opening${white} '${black}http://localhost:${port}/${white}'' in your favorite browser ..."
	firefox -new-tab "http://localhost:${port}"/ &
    # xdg-open "http://localhost:${port}"/ &  # Generic on Linux
	# open "http://localhost:${port}"/ &      # Generic on Mac
    # XXX this should be a better and cross-platform way to do it
    # python -m webbrowser -t "http://localhost:${port}"/
else
	echo -e "${red}Firefox is not running${white}, by default the uLogMe page will not be opened ...${white}"
	echo -e "('${black}http://localhost:${port}/${white}' is only opened in a new tab if your Firefox is already running)."
fi

echo -e "${green}Calling${white} '${blackwhite}python3 ulogme_serve.py ${port}${white}' ..."
python3 ./ulogme_serve.py "${port}"

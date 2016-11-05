#!/bin/bash
# ulogme_serve.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

echo -e "${yellow}Starting '${black}ulogme_serve.sh${white}' ..."

cd "$( dirname "${BASH_SOURCE[0]}" )"

# Options
port="${1:-8443}"  # Default is port=8124
IP="${2:-localhost}"
protocol="${3:-https}"

url=${protocol}://${IP}:${port}/


if pidof firefox >/dev/null; then
	echo -e "${yellow}Opening${white} '${black}${url}${white}'' in your favorite browser ..."
	firefox -new-tab "${url}" &
    # xdg-open "${url}" &  # Generic on Linux
	# open "${url}" &      # Generic on Mac
    # XXX this should be a better and cross-platform way to do it
    # python -m webbrowser -t "${url}"
else
	echo -e "${red}Firefox is not running${white}, by default the uLogMe page will not be opened ...${white}"
	echo -e "('${black}${url}${white}' is only opened in a new tab if your Firefox is already running)."
fi


if [ X"$protocol" = X"https" ]; then
    echo -e "${green}Calling${white} '${black}python3 ulogme_serve_https.py ${port} ${IP}${white}' ..."
    python3 ./ulogme_serve_https.py "${port}" "${IP}"
else
    echo -e "${green}Calling${white} '${black}python3 ulogme_serve.py ${port} ${IP}${white}' ..."
    python3 ./ulogme_serve.py "${port}" "${IP}"
fi

#!/bin/bash
# ulogme_data.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
echo "WARNING If you don't see colors correctly, remove the 'color.sh' file in 'uLogMe/scripts' to remove the colors, or modify it to suit your need (if you have a light background for instance)."  # See https://github.com/Naereen/uLogMe/issues/17
[ -f color.sh ] && . color.sh

cd "$( dirname "${BASH_SOURCE[0]}" )"

# echo -e "${red}Password is needed please${reset}, to run '${black}keyfreq.sh${reset}' with sudo ..."
# sudo echo -n ""

# sudo ./keyfreq.sh &
./keyfreq.sh &

./logactivewin.sh

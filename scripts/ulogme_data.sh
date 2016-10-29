#!/bin/bash
# ulogme_data.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f ~/.color.sh ] && . ~/.color.sh
[ -f color.sh ] && . color.sh

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo -e "${red}Password is needed please${white}, to run '${black}keyfreq.sh${white}' with sudo ..."
sudo echo -n ""

sudo ./keyfreq.sh &
./logactivewin.sh

#!/bin/bash
# ulogme_data.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/

# FIXED no need to adapt this to the path where you stored ulogme.git/
# cd ~/.local/share/ulogme/scripts/  # XXX change according to your installation
cd "$( dirname "${BASH_SOURCE[0]}" )"

# Assume Linux
echo "Password is needed please, to run 'keyfreq.sh' as sudo"
sudo echo -n ""
sudo ./keyfreq.sh &
./logactivewin.sh

#!/bin/bash

cd ~/.local/share/ulogme/
echo "Starting 'ulogme.sh' ..."

if [ "$(uname)" == "Darwin" ]; then
    # This is a Mac
    ./osx/run_ulogme_osx.sh
else
    # Assume Linux
    echo "Password is needed please, to run 'keyfreq.sh' as sudo"
    sudo echo -n ""
    sudo ./keyfreq.sh &
    ./logactivewin.sh
fi

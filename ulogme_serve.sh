#!/bin/bash

cd ~/.local/share/ulogme/
echo "Calling 'ulogme_serve.sh' ..."

port=${1:-8124}

echo -e "Opening 'http://localhost:${port}/' in Firefox ..."
firefox -new-tab "http://localhost:${port}"/ &
# xdg-open "http://localhost:${port}"/ &

echo -e "Calling 'python ulogme_serve.py ${port}' ..."
python ulogme_serve.py "${port}"

#!/bin/bash
# logdesktop.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
# periodically takes screenshot and saves them to desktopscr/
# the filename contains unix time

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

# wait time in seconds
waittime="60"
# directory to save screenshots to

saveprefix="${LOGDIR}/scr"
mkdir -p ${LOGDIR}/scr
cd ${LOGDIR}

#------------------------------

while true
do
	islocked=true
	if [[ $(gnome-screensaver-command -q) =~ .*inactive.* ]]; then
		islocked=false
	fi

	if ! $islocked
	then
		# take screenshot into file
		T="$(date +%s)"
		fname="${saveprefix}_${T}.png"
		# q is quality. Higher is higher quality
		scrot "$fname"
	else
		echo -e "${red}Screen is locked, waiting ...${reset}"
	fi

	sleep "$waittime"
done
